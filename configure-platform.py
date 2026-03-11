#!/usr/bin/env python3
"""
Platform Configuration Script for JUCE Projects
Automatically configures .vscode/settings.json based on the current platform.
Run this script if you open the project on a different platform than where it was generated.
"""

import os
import sys
import json
import platform
from pathlib import Path

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

def detectCurrentPlatform():
    system = platform.system()
    if system == "Darwin":
        arch = platform.machine()
        if arch == "arm64":
            return "Builds/macOS/ARM", "default-macos-arm64", "macOS (Apple Silicon)"
        else:
            return "Builds/macOS/Intel", "default-macos-x86_64", "macOS (Intel)"
    elif system == "Windows":
        return "Builds/Windows", "default-windows", "Windows"
    elif system == "Linux":
        return "Builds/Linux", "default-linux", "Linux"
    return "Builds/macOS/ARM", "default", system

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
                # Format: ${workspaceFolder}/Builds/.../ProjectName_artefacts/...
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
    print(f"\n   You can now open the project in Cursor and build directly!")

def configurePlatform():
    scriptDir = getScriptDirectory()
    settingsFile = getSettingsFilePath(scriptDir)
    ensureSettingsFileExists(settingsFile)
    
    buildDir, presetName, platformName = detectCurrentPlatform()
    settings = loadSettingsFromFile(settingsFile)
    updateSettingsForPlatform(settings, buildDir, presetName)
    writeSettingsToFile(settingsFile, settings)
    
    # Update launch.json and tasks.json
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

if __name__ == "__main__":
    configurePlatform()
