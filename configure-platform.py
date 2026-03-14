#!/usr/bin/env python3
"""
Platform Configuration Script for JUCE Projects
Automatically configures .vscode/settings.json based on the current platform.
Run this script if you open the project on a different platform than where it was generated.

On macOS: interactive menu to choose ARM, Intel, or Universal. Use --arm, --intel, --intel-rosetta,
--universal to skip the prompt. Intel on Apple Silicon routes to Intel-Rosetta automatically.
"""

import sys
import json
import platform
from pathlib import Path

# macOS configuration options
MACOS_ARM = ("Builds/macOS/ARM", "default-macos-arm64", "macOS (Apple Silicon)")
MACOS_INTEL = ("Builds/macOS/Intel", "default-macos-x86_64", "macOS (Intel)")
MACOS_INTEL_ROSETTA = ("Builds/macOS/Intel-Rosetta", "default-macos-x86_64-rosetta", "macOS (Intel-Rosetta)")
MACOS_UNIVERSAL = ("Builds/macOS/Universal", "default-macos-universal", "macOS (Universal)")


def getScriptDirectory():
    return Path(__file__).parent


def getSettingsFilePath(scriptDir):
    return scriptDir / ".vscode" / "settings.json"


def getLaunchFilePath(scriptDir):
    return scriptDir / ".vscode" / "launch.json"


def getTasksFilePath(scriptDir):
    return scriptDir / ".vscode" / "tasks.json"


def ensureSettingsFileExists(settingsFile):
    if not settingsFile.exists():
        print("❌ Error: .vscode/settings.json not found.")
        print("   Make sure you run this script from the project root directory.")
        sys.exit(1)


def parseMacOSConfigFromArgs():
    """Return (buildDir, presetName, platformName) or None if no macOS preset arg."""
    arch = platform.machine()
    for arg in sys.argv[1:]:
        if arg in ("--arm", "-a"):
            return MACOS_ARM
        if arg in ("--intel", "-i"):
            return _resolveIntelConfig(arch)
        if arg in ("--intel-rosetta",):
            if arch != "arm64":
                print("⚠️  Warning: --intel-rosetta is for Apple Silicon only. You are on Mac Intel.")
                print("   Configuring for Intel (native) instead.")
            return MACOS_INTEL_ROSETTA if arch == "arm64" else MACOS_INTEL
        if arg in ("--universal", "-u"):
            return MACOS_UNIVERSAL
    return None


def _resolveIntelConfig(arch):
    """Intel on arm64 → Intel-Rosetta; Intel on x86_64 → Intel (native)."""
    if arch == "arm64":
        return MACOS_INTEL_ROSETTA
    return MACOS_INTEL


def promptMacOSConfig():
    """Interactive prompt for macOS. Returns (buildDir, presetName, platformName)."""
    arch = platform.machine()
    default_choice = "1" if arch == "arm64" else "2"
    print("\nConfigure platform for this project:\n")
    print("  [1] ARM       > Builds/macOS/ARM (Apple Silicon native)")
    if arch == "arm64":
        print("  [2] Intel     > Builds/macOS/Intel-Rosetta (x86_64 on Apple Silicon)")
    else:
        print("  [2] Intel     > Builds/macOS/Intel (Mac Intel native)")
    print("  [3] Universal > Builds/macOS/Universal (Apple Silicon + Intel)\n")
    while True:
        try:
            choice = input(f"Choice [{default_choice}]: ").strip() or default_choice
        except (EOFError, KeyboardInterrupt):
            print()
            sys.exit(0)
        if choice == "1":
            return MACOS_ARM
        if choice == "2":
            return _resolveIntelConfig(arch)
        if choice == "3":
            return MACOS_UNIVERSAL
        print("❌ Invalid choice. Enter 1, 2, or 3.")


def getPlatformConfig(interactive_macos):
    """Return (buildDir, presetName, platformName). On macOS with interactive_macos, show prompt."""
    system = platform.system()
    if system == "Darwin":
        config = parseMacOSConfigFromArgs()
        if config is not None:
            return config
        if interactive_macos:
            return promptMacOSConfig()
        arch = platform.machine()
        return MACOS_ARM if arch == "arm64" else MACOS_INTEL
    if system == "Windows":
        return "Builds/Windows", "default-windows", "Windows"
    if system == "Linux":
        return "Builds/Linux", "default-linux", "Linux"
    return MACOS_ARM[0], "default", system


def loadSettingsFromFile(settingsFile):
    try:
        with open(settingsFile, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {settingsFile}: {e}")
        sys.exit(1)


def normalizeBuildDirectoryPath(buildDir):
    buildPath = Path(buildDir)
    return buildPath.as_posix()


def updateSettingsForPlatform(settings, buildDir, presetName):
    normalizedBuildDir = normalizeBuildDirectoryPath(buildDir)
    settings["cmake.buildDirectory"] = f"${{workspaceFolder}}/{normalizedBuildDir}"
    if "cmake.configurePreset" in settings:
        settings["cmake.configurePreset"] = presetName


def writeSettingsToFile(settingsFile, settings):
    try:
        with open(settingsFile, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"❌ Error writing settings file: {e}")
        sys.exit(1)


def extractProjectNameFromLaunch(launch):
    """Extract project name from launch.json paths."""
    for config in launch.get("configurations", []):
        prog = config.get("program", "")
        if "_artefacts" in prog:
            try:
                parts = prog.split("/")
                for p in parts:
                    if "_artefacts" in p:
                        return p.replace("_artefacts", "")
            except Exception:
                pass
    return None


def updateLaunchJson(launchFile, buildDir, projectName):
    """Update launch.json with the correct build directory paths."""
    if not launchFile.exists():
        return
    try:
        with open(launchFile, 'r', encoding='utf-8') as f:
            launch = json.load(f)
    except json.JSONDecodeError:
        return
    normalizedBuildDir = normalizeBuildDirectoryPath(buildDir)
    buildDirWin = "Builds/Windows"
    buildDirMacArm = "Builds/macOS/ARM"
    system = platform.system()
    modified = False
    for config in launch.get("configurations", []):
        if "Standalone" not in config.get("program", "") and "Standalone" not in config.get("osx", {}).get("program", ""):
            continue
        if system == "Darwin":
            newMacPath = f"${{workspaceFolder}}/{normalizedBuildDir}/{projectName}_artefacts/Debug/Standalone/{projectName}.app/Contents/MacOS/{projectName}"
            config["program"] = newMacPath
            if "osx" in config:
                config["osx"]["program"] = newMacPath
            if "windows" in config:
                config["windows"]["program"] = f"${{workspaceFolder}}/{buildDirWin}/{projectName}_artefacts/Debug/Standalone/{projectName}.exe"
        elif system == "Windows":
            newWinPath = f"${{workspaceFolder}}/{buildDirWin}/{projectName}_artefacts/Debug/Standalone/{projectName}.exe"
            config["program"] = newWinPath
            if "windows" in config:
                config["windows"]["program"] = newWinPath
            if "osx" in config:
                config["osx"]["program"] = f"${{workspaceFolder}}/{buildDirMacArm}/{projectName}_artefacts/Debug/Standalone/{projectName}.app/Contents/MacOS/{projectName}"
        modified = True
    if modified:
        try:
            with open(launchFile, 'w', encoding='utf-8') as f:
                json.dump(launch, f, indent=4, ensure_ascii=False)
        except Exception:
            pass


def updateTasksJson(tasksFile, buildDir):
    """Update tasks.json with the correct build directory paths."""
    if not tasksFile.exists():
        return
    try:
        with open(tasksFile, 'r', encoding='utf-8') as f:
            tasks = json.load(f)
    except json.JSONDecodeError:
        return
    normalizedBuildDir = normalizeBuildDirectoryPath(buildDir)
    buildDirWin = "Builds/Windows"
    buildDirLinux = "Builds/Linux"
    system = platform.system()
    for task in tasks.get("tasks", []):
        if system == "Darwin":
            targetDir = normalizedBuildDir
        elif system == "Windows":
            targetDir = buildDirWin
        else:
            targetDir = buildDirLinux
        args = task.get("args", [])
        if "-B" in args:
            idx = args.index("-B")
            if idx + 1 < len(args):
                args[idx + 1] = targetDir
        if "--build" in args:
            idx = args.index("--build")
            if idx + 1 < len(args):
                args[idx + 1] = targetDir
        if "osx" in task and system == "Darwin":
            osxArgs = task["osx"].get("args", [])
            if "-B" in osxArgs:
                idx = osxArgs.index("-B")
                if idx + 1 < len(osxArgs):
                    osxArgs[idx + 1] = normalizedBuildDir
            if "--build" in osxArgs:
                idx = osxArgs.index("--build")
                if idx + 1 < len(osxArgs):
                    osxArgs[idx + 1] = normalizedBuildDir
            task["osx"]["args"] = osxArgs
        if "windows" in task and system == "Windows":
            winArgs = task["windows"].get("args", [])
            if "-B" in winArgs:
                idx = winArgs.index("-B")
                if idx + 1 < len(winArgs):
                    winArgs[idx + 1] = buildDirWin
            if "--build" in winArgs:
                idx = winArgs.index("--build")
                if idx + 1 < len(winArgs):
                    winArgs[idx + 1] = buildDirWin
            task["windows"]["args"] = winArgs
        if "linux" in task and system == "Linux":
            linuxArgs = task["linux"].get("args", [])
            if "-B" in linuxArgs:
                idx = linuxArgs.index("-B")
                if idx + 1 < len(linuxArgs):
                    linuxArgs[idx + 1] = buildDirLinux
            if "--build" in linuxArgs:
                idx = linuxArgs.index("--build")
                if idx + 1 < len(linuxArgs):
                    linuxArgs[idx + 1] = buildDirLinux
            task["linux"]["args"] = linuxArgs
        if "Clean" in task.get("label", ""):
            if "args" in task:
                if system == "Windows":
                    task["args"] = ["-Command", "Remove-Item -Recurse -Force Builds -ErrorAction SilentlyContinue"]
                else:
                    task["args"] = ["-rf", "Builds"]
            if "windows" in task:
                task["windows"]["args"] = ["-Command", "Remove-Item -Recurse -Force Builds -ErrorAction SilentlyContinue"]
    try:
        with open(tasksFile, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=4, ensure_ascii=False)
    except Exception:
        pass


def displaySuccessMessage(platformName, buildDir, presetName):
    print(f"✅ Successfully configured for {platformName}")
    print(f"   Build directory: {buildDir}")
    print(f"   CMake preset: {presetName}")
    if "Intel-Rosetta" in platformName:
        print(f"   (x86_64 cross-compiled on Apple Silicon)")
    elif platformName == "macOS (Intel)":
        print(f"   (x86_64 native on Mac Intel)")
    print(f"\n   You can now open the project in Cursor and build directly!")


def waitForEnterToExit():
    """Keep terminal open when script is double-clicked."""
    print("\nPress [Enter] to exit...")
    try:
        input()
    except (EOFError, KeyboardInterrupt):
        pass


def configurePlatform():
    scriptDir = getScriptDirectory()
    settingsFile = getSettingsFilePath(scriptDir)
    ensureSettingsFileExists(settingsFile)

    system = platform.system()
    interactive_macos = system == "Darwin" and parseMacOSConfigFromArgs() is None

    buildDir, presetName, platformName = getPlatformConfig(interactive_macos)

    settings = loadSettingsFromFile(settingsFile)
    updateSettingsForPlatform(settings, buildDir, presetName)
    writeSettingsToFile(settingsFile, settings)

    launchFile = getLaunchFilePath(scriptDir)
    tasksFile = getTasksFilePath(scriptDir)
    if launchFile.exists():
        try:
            with open(launchFile, 'r', encoding='utf-8') as f:
                launch = json.load(f)
            projectName = extractProjectNameFromLaunch(launch)
            if projectName:
                updateLaunchJson(launchFile, buildDir, projectName)
        except Exception:
            pass
    updateTasksJson(tasksFile, buildDir)

    displaySuccessMessage(platformName, buildDir, presetName)

    if interactive_macos:
        waitForEnterToExit()


if __name__ == "__main__":
    configurePlatform()
