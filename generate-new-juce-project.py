#!/usr/bin/env python3

import os
import sys
import shutil
import re
import unicodedata
import platform
import importlib.util
from pathlib import Path
from typing import Dict, Optional, List, Tuple

kConfigModule = None
kConfigLoadError = None

try:
    scriptDir = Path(__file__).parent
    configPath = scriptDir / "user-config.py"
    if configPath.exists():
        spec = importlib.util.spec_from_file_location("user_config", configPath)
        kConfigModule = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(kConfigModule)
except Exception as e:
    kConfigModule = None
    kConfigLoadError = str(e)

class Color:
    RED    = '\033[0;91m'
    GREEN  = '\033[0;92m'
    BLUE   = '\033[0;96m'
    YELLOW = '\033[1;33m'
    RESET  = '\033[0m'

def waitForEnterToExit() -> None:
    print(f"\n{Color.YELLOW}Press [Enter] to exit...{Color.RESET}")
    try:
        input()
    except (EOFError, KeyboardInterrupt):
        pass

def exitWithError(message: str = "") -> None:
    if message:
        print(message)
    waitForEnterToExit()
    sys.exit(1)

def isPathSeparator(char: str) -> bool:
    return char in ['/', '\\', ':', ' ']

def isNonAsciiChar(char: str) -> bool:
    return ord(char) > 127

def isAccentedChar(char: str) -> bool:
    normalized = unicodedata.normalize('NFD', char)
    return len(normalized) > 1 and unicodedata.category(normalized[1]) == 'Mn'

def findProblematicCharsInPath(path: str) -> List[str]:
    problematicChars = []
    for char in path:
        if isPathSeparator(char):
            continue
        if isNonAsciiChar(char):
            problematicChars.append(char)
    return problematicChars

def hasProblematicChars(path: str) -> Tuple[bool, List[str]]:
    problematicChars = findProblematicCharsInPath(path)
    return len(problematicChars) > 0, problematicChars

def formatProblematicCharsString(problematicChars: List[str]) -> str:
    uniqueChars = list(set(problematicChars))
    charsStr = ', '.join(f"'{c}'" for c in uniqueChars[:10])
    if len(uniqueChars) > 10:
        charsStr += f" ... (and {len(uniqueChars) - 10} more)"
    return charsStr

def buildPathErrorHeader(configFile: str) -> str:
    return f"\n{Color.RED}{'=' * 70}{Color.RESET}\n{Color.RED}❌ ERROR: Invalid path detected in {configFile}{Color.RESET}\n{Color.RED}{'=' * 70}{Color.RESET}\n\n"

def buildPathErrorBody(pathName: str, path: str, charsStr: str) -> str:
    return (
        f"{Color.YELLOW}The parameter '{pathName}' contains problematic characters.{Color.RESET}\n\n"
        f"{Color.YELLOW}Problematic path:{Color.RESET}\n"
        f"  {Color.RED}{path}{Color.RESET}\n\n"
        f"{Color.YELLOW}Detected characters:{Color.RESET} {charsStr}\n\n"
    )

def buildPathErrorExplanation() -> str:
    return (
        f"{Color.YELLOW}Why this restriction?{Color.RESET}\n"
        f"  Paths with accents or special characters cause build errors\n"
        f"  with CMake/Visual Studio on Windows (error MSB8066).\n"
        f"  Generated .vcxproj files then contain incorrectly encoded characters.\n\n"
    )

def buildPathErrorSolution(pathName: str, configFile: str) -> str:
    return (
        f"{Color.YELLOW}Solution:{Color.RESET}\n"
        f"  1. Open the file {configFile}\n"
        f"  2. Modify '{pathName}' to use a path without accents\n"
        f"  3. Examples:\n"
        f"     ❌ \"C:/Users/John/Téléchargements\"\n"
        f"     ✅ \"C:/Users/John/Telechargements\"\n"
        f"     ❌ \"D:/Projets/Été 2024\"\n"
        f"     ✅ \"D:/Projets/Ete 2024\"\n\n"
    )

def buildPathErrorFooter() -> str:
    return f"{Color.RED}The generator stops now to avoid creating a project in the wrong location.{Color.RESET}\n{Color.RED}{'=' * 70}{Color.RESET}\n"

def validatePathNoProblematicChars(path: str, pathName: str, configFile: str = "user-config.py") -> None:
    hasProblematic, problematicChars = hasProblematicChars(path)
    if not hasProblematic:
        return
    
    charsStr = formatProblematicCharsString(problematicChars)
    errorMsg = (
        buildPathErrorHeader(configFile) +
        buildPathErrorBody(pathName, path, charsStr) +
        buildPathErrorExplanation() +
        buildPathErrorSolution(pathName, configFile) +
        buildPathErrorFooter()
    )
    exitWithError(errorMsg)

def showInteractivePathError(destination: str, problematicChars: List[str]) -> None:
    charsStr = formatProblematicCharsString(problematicChars)
    print(f"\n{Color.RED}❌ ERROR: The path contains problematic characters.{Color.RESET}")
    print(f"{Color.YELLOW}   Path: {destination}{Color.RESET}")
    print(f"{Color.YELLOW}   Detected characters: {charsStr}{Color.RESET}")
    print(f"{Color.YELLOW}   Paths with accents cause build errors with CMake/Visual Studio.{Color.RESET}")
    print(f"{Color.YELLOW}   Solution: Use a path without accents (e.g., 'Telechargements' instead of 'Téléchargements'){Color.RESET}\n")

class TemplateLoader:
    def __init__(self, templatesDir: Path):
        self.templatesDir = templatesDir
        if not self.templatesDir.exists():
            raise FileNotFoundError(f"Templates directory not found: {self.templatesDir}")
    
    def loadTemplate(self, templatePath: str) -> str:
        fullPath = self.templatesDir / templatePath
        if not fullPath.exists():
            raise FileNotFoundError(f"Template not found: {templatePath}")
        return fullPath.read_text(encoding='utf-8')

class JuceProjectGenerator:
    kDefaultVersion = "1.0.0"
    kDefaultPluginName = "NewPlugin"
    kValidPluginFormats = {"AU", "VST3", "Standalone"}
    
    def __init__(self, templateLoader: TemplateLoader):
        self.templateLoader = templateLoader
        self.kDefaultDestination = self.loadDefaultDestination()
        self.kDefaultManufacturer = self.loadDefaultManufacturer()
        self.kDefaultManufacturerCode = self.loadDefaultManufacturerCode()
        self.kDefaultPluginCode = self.loadDefaultPluginCode()
        self.customVst3Folder = self.loadCustomVst3Folder()
        self.juceDir = self.loadJuceDir()
        self.initializeProjectFields()
    
    def loadDefaultDestination(self) -> str:
        if kConfigModule and hasattr(kConfigModule, 'DEFAULT_PROJECT_DESTINATION'):
            destination = kConfigModule.DEFAULT_PROJECT_DESTINATION
            if destination and destination != "Default" and destination != "default":
                validatePathNoProblematicChars(destination, "DEFAULT_PROJECT_DESTINATION")
                return destination
        return str(Path.home() / "Desktop")
    
    def loadDefaultManufacturer(self) -> str:
        if kConfigModule and hasattr(kConfigModule, 'DEFAULT_MANUFACTURER_NAME') and kConfigModule.DEFAULT_MANUFACTURER_NAME:
            return kConfigModule.DEFAULT_MANUFACTURER_NAME
        return "My Company"
    
    def loadDefaultManufacturerCode(self) -> str:
        if kConfigModule and hasattr(kConfigModule, 'DEFAULT_MANUFACTURER_CODE') and kConfigModule.DEFAULT_MANUFACTURER_CODE:
            manufacturerCode = kConfigModule.DEFAULT_MANUFACTURER_CODE
            if self.isValidManufacturerCode(manufacturerCode):
                return manufacturerCode
            self.showInvalidManufacturerCodeWarning()
        return "Myco"
    
    def isValidManufacturerCode(self, code: str) -> bool:
        return len(code) == 4 and code.isalpha()
    
    def showInvalidManufacturerCodeWarning(self) -> None:
        print(f"{Color.YELLOW}⚠️  Warning: DEFAULT_MANUFACTURER_CODE in user-config.py is invalid (must be 4 alphabetic chars). Using default.{Color.RESET}")
    
    def loadDefaultPluginCode(self) -> str:
        if kConfigModule and hasattr(kConfigModule, 'DEFAULT_PLUGIN_CODE') and kConfigModule.DEFAULT_PLUGIN_CODE:
            pluginCode = kConfigModule.DEFAULT_PLUGIN_CODE
            if self.isValidPluginCode(pluginCode):
                return pluginCode
            self.showInvalidPluginCodeWarning()
        return "Mypl"
    
    def isValidPluginCode(self, code: str) -> bool:
        return len(code) == 4 and code.isalnum()
    
    def showInvalidPluginCodeWarning(self) -> None:
        print(f"{Color.YELLOW}⚠️  Warning: DEFAULT_PLUGIN_CODE in user-config.py is invalid (must be 4 alphanumeric chars). Using default.{Color.RESET}")
    
    def loadCustomVst3Folder(self) -> str:
        if kConfigModule and hasattr(kConfigModule, 'CUSTOM_VST3_FOLDER_WINDOWS'):
            vst3Path = kConfigModule.CUSTOM_VST3_FOLDER_WINDOWS
            if vst3Path:
                validatePathNoProblematicChars(vst3Path, "CUSTOM_VST3_FOLDER_WINDOWS")
                return Path(vst3Path).as_posix()
        return "C:/Users/YourName/VST3"
    
    def loadJuceDir(self) -> Optional[str]:
        system = platform.system()
        juceDir = None
        
        if kConfigModule:
            if system == "Darwin" and hasattr(kConfigModule, 'JUCE_DIR_MACOS'):
                juceDir = kConfigModule.JUCE_DIR_MACOS
            elif system == "Windows" and hasattr(kConfigModule, 'JUCE_DIR_WINDOWS'):
                juceDir = kConfigModule.JUCE_DIR_WINDOWS
            elif system == "Linux" and hasattr(kConfigModule, 'JUCE_DIR_LINUX'):
                juceDir = kConfigModule.JUCE_DIR_LINUX
        
        if juceDir and juceDir != "":
            normalizedJuceDir = Path(juceDir).as_posix()
            if not Path(normalizedJuceDir).exists():
                self.showJuceDirNotFoundWarning(normalizedJuceDir)
            return normalizedJuceDir
        return None
    
    def showJuceDirNotFoundWarning(self, juceDir: str) -> None:
        print(f"{Color.YELLOW}⚠️  Warning: JUCE_DIR path '{juceDir}' does not exist. Project generation will continue, but CMake configuration may fail.{Color.RESET}")
    
    def initializeProjectFields(self) -> None:
        self.projectName = ""
        self.projectDisplayName = ""
        self.projectVersion = ""
        self.manufacturerName = ""
        self.manufacturerCode = ""
        self.pluginCode = ""
        self.pluginFormats = ""
        self.destinationDir = ""
        self.projectDir = Path()
        self.bundleId = ""
        self.isSynth = "FALSE"
        self.needsMidiInput = "FALSE"
        self.needsMidiOutput = "FALSE"
        self.isMidiEffect = "FALSE"
        self.auMainType = ""
        self.vst3Categories = ""
    
    def printHeader(self) -> None:
        print(f"\n{Color.BLUE}{'=' * 60}{Color.RESET}")
        print(f"{Color.BLUE}  JUCE Project Generator - CMake + Cursor{Color.RESET}")
        print(f"{Color.BLUE}{'=' * 60}{Color.RESET}\n")
        if kConfigLoadError:
            self.showConfigLoadError()
    
    def showConfigLoadError(self) -> None:
        print(f"{Color.YELLOW}⚠️  Warning: Could not load user-config.py:{Color.RESET}")
        print(f"{Color.YELLOW}   Error: {kConfigLoadError}{Color.RESET}")
        print(f"{Color.YELLOW}   Using default values. Please check your user-config.py file.{Color.RESET}\n")
    
    def getValidBooleanInput(self, prompt: str, default: bool = False) -> bool:
        defaultStr = "Y/n" if default else "y/N"
        while True:
            choice = input(f"{prompt} [{defaultStr}]: ").strip()
            if choice == '':
                self.showInvalidBooleanInputError()
                continue
            choiceLower = choice.lower()
            if choiceLower in ['y', 'yes']:
                return True
            elif choiceLower in ['n', 'no']:
                return False
            else:
                self.showInvalidBooleanInputError()
    
    def showInvalidBooleanInputError(self) -> None:
        print(f"{Color.RED}❌ Invalid response. Please enter 'y' or 'n'{Color.RESET}")
    
    def isValidProjectName(self, name: str) -> bool:
        return bool(re.match(r'^[a-zA-Z][a-zA-Z0-9_-]*$', name))
    
    def inputProjectName(self) -> tuple:
        while True:
            techName = input(f"  Technical project name [{self.kDefaultPluginName}]: ").strip() or self.kDefaultPluginName
            if not self.isValidProjectName(techName):
                self.showInvalidProjectNameError()
                continue
            projectDir = Path(self.kDefaultDestination) / techName
            if projectDir.exists():
                if not self.handleExistingProject(techName):
                    continue
            displayName = input(f"  Display name (optional, can include spaces) [{techName}]: ").strip() or techName
            return techName, displayName
    
    def showInvalidProjectNameError(self) -> None:
        print(f"{Color.RED}❌ Technical name must start with a letter and contain only letters, numbers, and underscores{Color.RESET}")
    
    def handleExistingProject(self, techName: str) -> bool:
        print(f"\n{Color.YELLOW}⚠️  A folder named '{techName}' already exists at {self.kDefaultDestination}{Color.RESET}")
        if self.getValidBooleanInput("Overwrite existing folder?"):
            print(f"{Color.YELLOW}Existing folder will be overwritten.{Color.RESET}\n")
            return True
        print(f"{Color.YELLOW}Please choose a different technical name.\n{Color.RESET}")
        return False
    
    def inputManufacturerCode(self) -> str:
        while True:
            code = input(f"  Manufacturer code (4 chars) [{self.kDefaultManufacturerCode}]: ").strip()
            if code == '':
                return self.kDefaultManufacturerCode
            if len(code) == 4 and code.isalpha():
                return code
            print(f"{Color.RED}❌ Must be exactly 4 alphabetic characters{Color.RESET}")
    
    def inputPluginCode(self) -> str:
        while True:
            code = input(f"  Plugin code (4 chars) [{self.kDefaultPluginCode}]: ").strip()
            if code == '':
                return self.kDefaultPluginCode
            if len(code) == 4 and code.isalnum():
                return code
            print(f"{Color.RED}❌ Must be exactly 4 alphanumeric characters{Color.RESET}")
    
    def selectPluginFormats(self) -> str:
        print(f"\n{Color.YELLOW}Select plugin formats:{Color.RESET}")
        formats = ["AU", "VST3", "Standalone"]
        selected = []
        for fmt in formats:
            if self.getValidBooleanInput(f"  Include {fmt}?", default=(fmt == "Standalone")):
                selected.append(fmt)
        if not selected:
            print(f"{Color.RED}❌ At least one format must be selected{Color.RESET}\n")
            return self.selectPluginFormats()
        return " ".join(selected)
    
    def selectDestinationFolder(self) -> str:
        print(f"\n{Color.YELLOW}Finalization:{Color.RESET}")
        while True:
            destination = input(f"  Destination folder [{self.kDefaultDestination}]: ").strip() or self.kDefaultDestination
            hasProblematic, problematicChars = hasProblematicChars(destination)
            if hasProblematic:
                showInteractivePathError(destination, problematicChars)
            else:
                return destination
    
    def generateBundleId(self, manufacturerName: str, projectName: str) -> str:
        manufacturerId = re.sub(r'[^a-zA-Z0-9]', '', manufacturerName)
        if manufacturerId and not manufacturerId[0].isalpha():
            manufacturerId = "Company" + manufacturerId
        projectId = re.sub(r'[^a-zA-Z0-9_-]', '', projectName)
        return f"com.{manufacturerId}.{projectId}"
    
    def configurePluginSettings(self) -> None:
        print(f"\n{Color.YELLOW}Plugin Configuration:{Color.RESET}")
        self.isSynth = "TRUE" if self.getValidBooleanInput("  Is this a synthesizer?") else "FALSE"
        self.needsMidiInput = "TRUE" if self.getValidBooleanInput("  Requires MIDI input?") else "FALSE"
        self.needsMidiOutput = "TRUE" if self.getValidBooleanInput("  Produces MIDI output?") else "FALSE"
        self.isMidiEffect = "TRUE" if self.getValidBooleanInput("  Is this a MIDI effect?") else "FALSE"
        self.updateAuAndVst3Categories()
    
    def updateAuAndVst3Categories(self) -> None:
        isSynth = self.isSynth == "TRUE"
        isMidiEffect = self.isMidiEffect == "TRUE"
        if isSynth:
            self.auMainType = "kAudioUnitType_MusicDevice"
            self.vst3Categories = "Instrument|Synth"
        elif isMidiEffect:
            self.auMainType = "kAudioUnitType_MIDIProcessor"
            self.vst3Categories = "Fx|MIDI"
        else:
            self.auMainType = "kAudioUnitType_Effect"
            self.vst3Categories = "Fx"
    
    def collectProjectInfo(self) -> None:
        print(f"\n{Color.YELLOW}Project Information:{Color.RESET}")
        self.projectName, self.projectDisplayName = self.inputProjectName()
        self.projectDir = Path(self.kDefaultDestination) / self.projectName
        self.projectVersion = input(f"  Project version [{self.kDefaultVersion}]: ").strip() or self.kDefaultVersion
        self.manufacturerName = input(f"  Manufacturer name [{self.kDefaultManufacturer}]: ").strip() or self.kDefaultManufacturer
        self.manufacturerCode = self.inputManufacturerCode()
        self.pluginCode = self.inputPluginCode()
        self.bundleId = self.generateBundleId(self.manufacturerName, self.projectName)
        self.configurePluginSettings()
        self.pluginFormats = self.selectPluginFormats()
        self.destinationDir = self.selectDestinationFolder()
        self.projectDir = Path(self.destinationDir) / self.projectName
    
    def showSummary(self) -> bool:
        print(f"\n{Color.YELLOW}{'=' * 60}{Color.RESET}")
        print(f"{Color.YELLOW}Summary{Color.RESET}")
        print(f"{Color.YELLOW}{'=' * 60}{Color.RESET}")
        print(f"  Technical Name    : {self.projectName}")
        print(f"  Display Name      : {self.projectDisplayName}")
        print(f"  Version           : {self.projectVersion}")
        print(f"  Manufacturer      : {self.manufacturerName}")
        print(f"  Manufacturer Code : {self.manufacturerCode}")
        print(f"  Plugin Code       : {self.pluginCode}")
        print(f"  Bundle ID         : {self.bundleId}")
        print(f"  Is Synth          : {self.isSynth}")
        print(f"  MIDI Input        : {self.needsMidiInput}")
        print(f"  MIDI Output       : {self.needsMidiOutput}")
        print(f"  MIDI Effect       : {self.isMidiEffect}")
        print(f"  Formats           : {self.pluginFormats}")
        print(f"  Destination       : {self.projectDir}")
        print(f"{Color.YELLOW}{'=' * 60}{Color.RESET}\n")
        return self.getValidBooleanInput("Create project?", default=True)
    
    def createProjectStructure(self) -> None:
        print(f"\n{Color.GREEN}📁 Creating project structure...{Color.RESET}")
        if self.projectDir.exists():
            shutil.rmtree(self.projectDir)
        (self.projectDir / "Source").mkdir(parents=True, exist_ok=True)
        (self.projectDir / ".vscode").mkdir(parents=True, exist_ok=True)
    
    def renderTemplate(self, templateContent: str) -> str:
        juceDirValue = self.juceDir if self.juceDir else ""
        return templateContent.format(
            projectName=self.projectName,
            projectDisplayName=self.projectDisplayName,
            projectVersion=self.projectVersion,
            manufacturerName=self.manufacturerName,
            manufacturerCode=self.manufacturerCode,
            pluginCode=self.pluginCode,
            pluginFormats=self.pluginFormats,
            isSynth=self.isSynth,
            needsMidiInput=self.needsMidiInput,
            needsMidiOutput=self.needsMidiOutput,
            isMidiEffect=self.isMidiEffect,
            auMainType=self.auMainType,
            vst3Categories=self.vst3Categories,
            bundleId=self.bundleId,
            customVst3Folder=self.customVst3Folder,
            juceDir=juceDirValue
        )
    
    def generateCMakeLists(self) -> None:
        print(f"{Color.GREEN}📝 Generating CMakeLists.txt...{Color.RESET}")
        templateContent = self.templateLoader.loadTemplate("CMakeLists.txt")
        renderedContent = self.renderTemplate(templateContent)
        self.writeFile("CMakeLists.txt", renderedContent)
    
    def generatePluginProcessor(self) -> None:
        print(f"{Color.GREEN}📝 Generating PluginProcessor.h...{Color.RESET}")
        headerContent = self.templateLoader.loadTemplate("Source/PluginProcessor.h")
        renderedContent = self.renderTemplate(headerContent)
        self.writeFile("Source/PluginProcessor.h", renderedContent)
        print(f"{Color.GREEN}📝 Generating PluginProcessor.cpp...{Color.RESET}")
        cppContent = self.templateLoader.loadTemplate("Source/PluginProcessor.cpp")
        renderedContent = self.renderTemplate(cppContent)
        self.writeFile("Source/PluginProcessor.cpp", renderedContent)
    
    def generatePluginEditor(self) -> None:
        print(f"{Color.GREEN}📝 Generating PluginEditor.h...{Color.RESET}")
        headerContent = self.templateLoader.loadTemplate("Source/PluginEditor.h")
        renderedContent = self.renderTemplate(headerContent)
        self.writeFile("Source/PluginEditor.h", renderedContent)
        print(f"{Color.GREEN}📝 Generating PluginEditor.cpp...{Color.RESET}")
        cppContent = self.templateLoader.loadTemplate("Source/PluginEditor.cpp")
        renderedContent = self.renderTemplate(cppContent)
        self.writeFile("Source/PluginEditor.cpp", renderedContent)
    
    def generatePluginFactory(self) -> None:
        print(f"{Color.GREEN}📝 Generating PluginFactory.cpp...{Color.RESET}")
        content = self.templateLoader.loadTemplate("Source/PluginFactory.cpp")
        renderedContent = self.renderTemplate(content)
        self.writeFile("Source/PluginFactory.cpp", renderedContent)
    
    def getPlatformBuildConfig(self) -> tuple:
        system = platform.system()
        if system == "Darwin":
            return "build-macos", "default-macos"
        elif system == "Windows":
            return "build-windows", "default-windows"
        return "build", "default"
    
    def generateVSCodeSettings(self) -> None:
        print(f"{Color.GREEN}📝 Generating .vscode/settings.json...{Color.RESET}")
        buildDir, presetName = self.getPlatformBuildConfig()
        templateContent = self.templateLoader.loadTemplate(".vscode/settings.json")
        buildPath = Path(buildDir)
        templateContent = templateContent.replace("{buildDirectory}", buildPath.as_posix())
        renderedContent = self.renderTemplate(templateContent)
        self.writeFile(".vscode/settings.json", renderedContent)
    
    def generateVSCodeTasks(self) -> None:
        print(f"{Color.GREEN}📝 Generating .vscode/tasks.json...{Color.RESET}")
        templateContent = self.templateLoader.loadTemplate(".vscode/tasks.json")
        renderedContent = self.renderTemplate(templateContent)
        self.writeFile(".vscode/tasks.json", renderedContent)
    
    def generateVSCodeLaunch(self) -> None:
        print(f"{Color.GREEN}📝 Generating .vscode/launch.json...{Color.RESET}")
        templateContent = self.templateLoader.loadTemplate(".vscode/launch.json")
        renderedContent = self.renderTemplate(templateContent)
        self.writeFile(".vscode/launch.json", renderedContent)
    
    def generateCursorRules(self) -> None:
        print(f"{Color.GREEN}📝 Generating .cursorrules...{Color.RESET}")
        content = self.templateLoader.loadTemplate(".cursorrules")
        self.writeFile(".cursorrules", content)
    
    def generateGitIgnore(self) -> None:
        print(f"{Color.GREEN}📝 Generating .gitignore...{Color.RESET}")
        content = self.templateLoader.loadTemplate(".gitignore")
        self.writeFile(".gitignore", content)
    
    def generateCMakeUserPresets(self) -> None:
        print(f"{Color.GREEN}📝 Generating CMakeUserPresets.json...{Color.RESET}")
        content = self.templateLoader.loadTemplate("CMakeUserPresets.json")
        content = content.replace("{{", "{").replace("}}", "}")
        self.writeFile("CMakeUserPresets.json", content)
    
    def generateConfigureScript(self) -> None:
        print(f"{Color.GREEN}📝 Copying configure-platform.py script...{Color.RESET}")
        scriptPath = Path(__file__).parent / "configure-platform.py"
        if scriptPath.exists():
            shutil.copy2(scriptPath, self.projectDir / "configure-platform.py")
        else:
            print(f"{Color.YELLOW}⚠️  Warning: configure-platform.py not found in template directory{Color.RESET}")
    
    def generateReadme(self) -> None:
        print(f"{Color.GREEN}📝 Generating README.md...{Color.RESET}")
        templateContent = self.templateLoader.loadTemplate("README.md")
        renderedContent = self.renderTemplate(templateContent)
        self.writeFile("README.md", renderedContent)
    
    def getPlatformInfo(self) -> tuple:
        system = platform.system()
        if system == "Darwin":
            return "macOS", "default-macos"
        elif system == "Windows":
            return "Windows", "default-windows"
        return system, "default"
    
    def getOpenCommandForPlatform(self, system: str, projectPathStr: str) -> str:
        if system == "Windows":
            return f"cd \"{projectPathStr}\"; cursor ."
        return f"cd {projectPathStr} && cursor ."
    
    def getBuildDirectoryName(self, platformName: str, system: str) -> str:
        if system == "Windows":
            return "build-windows"
        return f"build-{platformName.lower()}"
    
    def showSuccess(self) -> None:
        system = platform.system()
        platformName, presetName = self.getPlatformInfo()
        print(f"\n{Color.GREEN}{'=' * 60}{Color.RESET}")
        print(f"{Color.GREEN}✅ Project created successfully!{Color.RESET}")
        print(f"{Color.GREEN}{'=' * 60}{Color.RESET}\n")
        print(f"{Color.BLUE}📍 Location:{Color.RESET} {self.projectDir}\n")
        print(f"{Color.YELLOW}Next steps:{Color.RESET}\n")
        print(f"  1. Open project in Cursor:")
        projectPathStr = str(self.projectDir)
        openCommand = self.getOpenCommandForPlatform(system, projectPathStr)
        print(f"     {Color.BLUE}{openCommand}{Color.RESET}\n")
        buildDirName = self.getBuildDirectoryName(platformName, system)
        print(f"  2. Project is automatically configured for {platformName}")
        print(f"     CMake preset: {presetName}")
        print(f"     Build directory: {buildDirName}\n")
        print(f"  3. In Cursor:")
        print(f"     - Select build kit when prompted (CMake Tools will suggest the correct one)")
        print(f"     - Build: {Color.BLUE}Ctrl+Shift+P{Color.RESET} (or {Color.BLUE}Cmd+Shift+P{Color.RESET} on macOS) → \"CMake: Build\"")
        print(f"     - Debug: Press {Color.BLUE}F5{Color.RESET} to start debugging\n")
        if system == "Windows":
            print(f"  {Color.YELLOW}Note:{Color.RESET} If you open this project on macOS later, run:")
            print(f"     {Color.BLUE}python configure-platform.py{Color.RESET}\n")
        elif system == "Darwin":
            print(f"  {Color.YELLOW}Note:{Color.RESET} If you open this project on Windows later, run:")
            print(f"     {Color.BLUE}python configure-platform.py{Color.RESET}\n")
        print(f"{Color.GREEN}{'=' * 60}{Color.RESET}\n")
        waitForEnterToExit()
    
    def writeFile(self, relativePath: str, content: str) -> None:
        filePath = self.projectDir / relativePath
        filePath.parent.mkdir(parents=True, exist_ok=True)
        filePath.write_text(content, encoding='utf-8')
    
    def generate(self) -> None:
        self.printHeader()
        self.collectProjectInfo()
        if not self.showSummary():
            print(f"{Color.RED}❌ Project creation cancelled{Color.RESET}\n")
            sys.exit(0)
        self.createProjectStructure()
        self.generateCMakeLists()
        self.generatePluginProcessor()
        self.generatePluginEditor()
        self.generatePluginFactory()
        self.generateVSCodeSettings()
        self.generateVSCodeTasks()
        self.generateVSCodeLaunch()
        self.generateCursorRules()
        self.generateGitIgnore()
        self.generateCMakeUserPresets()
        self.generateConfigureScript()
        self.generateReadme()
        self.showSuccess()

def main():
    try:
        scriptDir = Path(__file__).parent
        templatesDir = scriptDir / "templates"
        templateLoader = TemplateLoader(templatesDir)
        generator = JuceProjectGenerator(templateLoader)
        generator.generate()
    except KeyboardInterrupt:
        exitWithError(f"\n{Color.RED}❌ Operation cancelled by user{Color.RESET}\n")
    except Exception as e:
        exitWithError(f"\n{Color.RED}❌ Error: {e}{Color.RESET}\n")

if __name__ == "__main__":
    main()
