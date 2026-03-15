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

BUILD_DIR_MACOS_ARM = "Builds/macOS/ARM"
BUILD_DIR_MACOS_INTEL = "Builds/macOS/Intel"
BUILD_DIR_MACOS_INTEL_ROSETTA = "Builds/macOS/Intel-Rosetta"
BUILD_DIR_MACOS_UNIVERSAL = "Builds/macOS/Universal"
BUILD_DIR_WINDOWS = "Builds/Windows"
BUILD_DIR_LINUX = "Builds/Linux"

PRESET_MACOS_ARM = "default-macos-arm64"
PRESET_MACOS_INTEL = "default-macos-x86_64"
PRESET_MACOS_INTEL_ROSETTA = "default-macos-x86_64-rosetta"
PRESET_MACOS_UNIVERSAL = "default-macos-universal"
PRESET_WINDOWS = "default-windows"
PRESET_LINUX = "default-linux"

VSCODE_DIR = ".vscode"
VSCODE_SETTINGS_PATH = ".vscode/settings.json"
VSCODE_LAUNCH_PATH = ".vscode/launch.json"
VSCODE_TASKS_PATH = ".vscode/tasks.json"
WORKSPACE_FOLDER_PLACEHOLDER = "${workspaceFolder}"
STANDALONE_ARTEFACTS_SUFFIX = "_artefacts/Debug/Standalone"
CONFIG_DEBUG = "Debug"

MACOS_ARM = (BUILD_DIR_MACOS_ARM, PRESET_MACOS_ARM, "macOS (Apple Silicon)")
MACOS_INTEL = (BUILD_DIR_MACOS_INTEL, PRESET_MACOS_INTEL, "macOS (Intel)")
MACOS_INTEL_ROSETTA = (BUILD_DIR_MACOS_INTEL_ROSETTA, PRESET_MACOS_INTEL_ROSETTA, "macOS (Intel-Rosetta)")
MACOS_UNIVERSAL = (BUILD_DIR_MACOS_UNIVERSAL, PRESET_MACOS_UNIVERSAL, "macOS (Universal)")


def getScriptDirectory():
    return Path(__file__).parent


def getSettingsFilePath(scriptDir):
    return scriptDir / VSCODE_SETTINGS_PATH


def getLaunchFilePath(scriptDir):
    return scriptDir / VSCODE_LAUNCH_PATH


def getTasksFilePath(scriptDir):
    return scriptDir / VSCODE_TASKS_PATH


def ensureSettingsFileExists(settingsFile):
    if not settingsFile.exists():
        print("❌ Error: .vscode/settings.json not found.")
        print("   Make sure you run this script from the project root directory.")
        sys.exit(1)


def _loadJsonFile(path: Path) -> dict:
    """Load and parse JSON file. Exit on error."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {path}: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading {path}: {e}")
        sys.exit(1)


def _loadJsonFileSafe(path: Path) -> dict | None:
    """Load and parse JSON file. Return None on error."""
    if not path.exists():
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, Exception):
        return None


def _writeJsonFile(path: Path, data: dict) -> None:
    """Write JSON file with indent 4. Exit on error."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"❌ Error writing {path}: {e}")
        sys.exit(1)


def _writeJsonFileSafe(path: Path, data: dict) -> bool:
    """Write JSON file with indent 4. Return False on error."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception:
        return False


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
    defaultChoice = "1" if arch == "arm64" else "2"
    print("\nConfigure platform for this project:\n")
    print("  [1] ARM       > Builds/macOS/ARM (Apple Silicon native)")
    if arch == "arm64":
        print("  [2] Intel     > Builds/macOS/Intel-Rosetta (x86_64 on Apple Silicon)")
    else:
        print("  [2] Intel     > Builds/macOS/Intel (Mac Intel native)")
    print("  [3] Universal > Builds/macOS/Universal (Apple Silicon + Intel)\n")
    while True:
        try:
            choice = input(f"Choice [{defaultChoice}]: ").strip() or defaultChoice
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


def getPlatformConfig(interactiveMacos):
    """Return (buildDir, presetName, platformName). On macOS with interactiveMacos, show prompt."""
    system = platform.system()
    if system == "Darwin":
        config = parseMacOSConfigFromArgs()
        if config is not None:
            return config
        if interactiveMacos:
            return promptMacOSConfig()
        arch = platform.machine()
        return MACOS_ARM if arch == "arm64" else MACOS_INTEL
    if system == "Windows":
        return BUILD_DIR_WINDOWS, PRESET_WINDOWS, "Windows"
    if system == "Linux":
        return BUILD_DIR_LINUX, PRESET_LINUX, "Linux"
    return MACOS_ARM[0], "default", system


def loadSettingsFromFile(settingsFile):
    return _loadJsonFile(settingsFile)


def normalizeBuildDirectoryPath(buildDir):
    buildPath = Path(buildDir)
    return buildPath.as_posix()


def updateSettingsForPlatform(settings, buildDir, presetName):
    normalizedBuildDir = normalizeBuildDirectoryPath(buildDir)
    settings["cmake.buildDirectory"] = f"{WORKSPACE_FOLDER_PLACEHOLDER}/{normalizedBuildDir}"
    if "cmake.configurePreset" in settings:
        settings["cmake.configurePreset"] = presetName


def writeSettingsToFile(settingsFile, settings):
    _writeJsonFile(settingsFile, settings)


def _buildStandalonePathMacos(workspacePrefix: str, buildDir: str, projectName: str) -> str:
    """Build macOS standalone path for launch.json."""
    normalizedBuildDir = normalizeBuildDirectoryPath(buildDir)
    return f"{workspacePrefix}/{normalizedBuildDir}/{projectName}{STANDALONE_ARTEFACTS_SUFFIX}/{projectName}.app/Contents/MacOS/{projectName}"


def _buildStandalonePathWindows(workspacePrefix: str, buildDir: str, projectName: str) -> str:
    """Build Windows standalone path for launch.json."""
    normalizedBuildDir = normalizeBuildDirectoryPath(buildDir)
    return f"{workspacePrefix}/{normalizedBuildDir}/{projectName}{STANDALONE_ARTEFACTS_SUFFIX}/{projectName}.exe"


def extractProjectNameFromLaunch(launch):
    """Extract project name from launch.json paths."""
    for config in launch.get("configurations", []):
        prog = config.get("program", "")
        if STANDALONE_ARTEFACTS_SUFFIX not in prog:
            continue
        normalized = Path(prog).as_posix()
        parts = normalized.split("/")
        for part in parts:
            if STANDALONE_ARTEFACTS_SUFFIX in part:
                return part.replace(STANDALONE_ARTEFACTS_SUFFIX, "")
    return None


def _isStandaloneConfig(config: dict) -> bool:
    """Check if config is for Standalone build."""
    if "Standalone" in config.get("program", ""):
        return True
    if "osx" in config and "Standalone" in config["osx"].get("program", ""):
        return True
    return False


def _updateStandaloneConfigPaths(config: dict, system: str, normalizedBuildDir: str, projectName: str) -> None:
    """Update program paths in a Standalone config for current platform."""
    if system == "Darwin":
        newMacPath = _buildStandalonePathMacos(WORKSPACE_FOLDER_PLACEHOLDER, normalizedBuildDir, projectName)
        config["program"] = newMacPath
        if "osx" in config:
            config["osx"]["program"] = newMacPath
        if "windows" in config:
            config["windows"]["program"] = _buildStandalonePathWindows(WORKSPACE_FOLDER_PLACEHOLDER, BUILD_DIR_WINDOWS, projectName)
    elif system == "Windows":
        newWinPath = _buildStandalonePathWindows(WORKSPACE_FOLDER_PLACEHOLDER, BUILD_DIR_WINDOWS, projectName)
        config["program"] = newWinPath
        if "windows" in config:
            config["windows"]["program"] = newWinPath
        if "osx" in config:
            config["osx"]["program"] = _buildStandalonePathMacos(WORKSPACE_FOLDER_PLACEHOLDER, BUILD_DIR_MACOS_ARM, projectName)


def updateLaunchJson(launchFile, buildDir, projectName):
    """Update launch.json with the correct build directory paths."""
    launch = _loadJsonFileSafe(launchFile)
    if launch is None:
        return
    normalizedBuildDir = normalizeBuildDirectoryPath(buildDir)
    system = platform.system()
    modified = False
    for config in launch.get("configurations", []):
        if not _isStandaloneConfig(config):
            continue
        _updateStandaloneConfigPaths(config, system, normalizedBuildDir, projectName)
        modified = True
    if modified:
        _writeJsonFileSafe(launchFile, launch)


def _updateArgsBuildDir(args, targetDir):
    """Update -B and --build in args list in-place."""
    for flag in ("-B", "--build"):
        if flag in args:
            idx = args.index(flag)
            if idx + 1 < len(args):
                args[idx + 1] = targetDir


def _getTargetDirForSystem(system, normalizedBuildDir):
    """Return the build directory path for the current platform."""
    if system == "Darwin":
        return normalizedBuildDir
    if system == "Windows":
        return BUILD_DIR_WINDOWS
    return BUILD_DIR_LINUX


def _getCleanTaskArgs(system):
    """Return args for the Clean task based on platform."""
    if system == "Windows":
        return ["-Command", "Remove-Item -Recurse -Force Builds -ErrorAction SilentlyContinue"]
    return ["-rf", "Builds"]


def _updateTaskBuildDirs(task, system, normalizedBuildDir):
    """Update build dirs in a single task's args and platform-specific args."""
    targetDir = _getTargetDirForSystem(system, normalizedBuildDir)
    args = task.get("args", [])
    _updateArgsBuildDir(args, targetDir)
    if "osx" in task and system == "Darwin":
        osxArgs = task["osx"].get("args", [])
        _updateArgsBuildDir(osxArgs, normalizedBuildDir)
        task["osx"]["args"] = osxArgs
    if "windows" in task and system == "Windows":
        winArgs = task["windows"].get("args", [])
        _updateArgsBuildDir(winArgs, BUILD_DIR_WINDOWS)
        task["windows"]["args"] = winArgs
    if "linux" in task and system == "Linux":
        linuxArgs = task["linux"].get("args", [])
        _updateArgsBuildDir(linuxArgs, BUILD_DIR_LINUX)
        task["linux"]["args"] = linuxArgs


def _updateCleanTask(task, system):
    """Update Clean task args for the current platform."""
    if "Clean" not in task.get("label", ""):
        return
    cleanArgs = _getCleanTaskArgs(system)
    if "args" in task:
        task["args"] = cleanArgs
    if "windows" in task:
        task["windows"]["args"] = _getCleanTaskArgs("Windows")


def updateTasksJson(tasksFile, buildDir):
    """Update tasks.json with the correct build directory paths."""
    tasks = _loadJsonFileSafe(tasksFile)
    if tasks is None:
        return
    normalizedBuildDir = normalizeBuildDirectoryPath(buildDir)
    system = platform.system()
    for task in tasks.get("tasks", []):
        _updateTaskBuildDirs(task, system, normalizedBuildDir)
        _updateCleanTask(task, system)
    _writeJsonFileSafe(tasksFile, tasks)


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
    interactiveMacos = system == "Darwin" and parseMacOSConfigFromArgs() is None

    buildDir, presetName, platformName = getPlatformConfig(interactiveMacos)

    settings = loadSettingsFromFile(settingsFile)
    updateSettingsForPlatform(settings, buildDir, presetName)
    writeSettingsToFile(settingsFile, settings)

    launchFile = getLaunchFilePath(scriptDir)
    tasksFile = getTasksFilePath(scriptDir)
    
    launch = _loadJsonFileSafe(launchFile)
    if launch:
        projectName = extractProjectNameFromLaunch(launch)
        if projectName:
            updateLaunchJson(launchFile, buildDir, projectName)
    
    updateTasksJson(tasksFile, buildDir)

    displaySuccessMessage(platformName, buildDir, presetName)

    if interactiveMacos:
        waitForEnterToExit()


if __name__ == "__main__":
    configurePlatform()
