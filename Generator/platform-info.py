#!/usr/bin/env python3
"""
PlatformInfo: provides build directory, CMake preset, and display name for current platform.
Single responsibility: platform detection and build configuration.
"""

import platform

# Order: Windows, macOS, Linux (for consistent presentation)
BUILD_DIR_WINDOWS = "Builds/Windows"
BUILD_DIR_MACOS_ARM = "Builds/macOS/ARM"
BUILD_DIR_MACOS_INTEL = "Builds/macOS/Intel"
BUILD_DIR_MACOS_INTEL_ROSETTA = "Builds/macOS/Intel-Rosetta"
BUILD_DIR_MACOS_UNIVERSAL = "Builds/macOS/Universal"
BUILD_DIR_LINUX = "Builds/Linux"

PRESET_WINDOWS = "default-windows"
PRESET_MACOS_ARM = "default-macos-arm64"
PRESET_MACOS_INTEL = "default-macos-x86_64"
PRESET_MACOS_INTEL_ROSETTA = "default-macos-x86_64-rosetta"
PRESET_MACOS_UNIVERSAL = "default-macos-universal"
PRESET_LINUX = "default-linux"

PLATFORM_NAME_WINDOWS = "Windows"
PLATFORM_NAME_MACOS_ARM = "macOS (Apple Silicon)"
PLATFORM_NAME_MACOS_INTEL = "macOS (Intel)"
PLATFORM_NAME_LINUX = "Linux"


def _getPlatformContext() -> tuple[str, str]:
    """Return (system, arch) where arch is empty if not Darwin."""
    system = platform.system()
    arch = platform.machine() if system == "Darwin" else ""
    return system, arch


def getBuildDirectory() -> str:
    """Return build directory path for current platform (e.g. Builds/macOS/ARM)."""
    system, arch = _getPlatformContext()
    if system == "Darwin":
        return BUILD_DIR_MACOS_ARM if arch == "arm64" else BUILD_DIR_MACOS_INTEL
    if system == "Windows":
        return BUILD_DIR_WINDOWS
    if system == "Linux":
        return BUILD_DIR_LINUX
    return BUILD_DIR_MACOS_ARM


def getBuildDirMacOS() -> str:
    """Return macOS build dir (ARM or Intel) based on current machine."""
    return getBuildDirectory() if platform.system() == "Darwin" else BUILD_DIR_MACOS_ARM


def getPlatformPreset() -> str:
    """Return CMake preset name for current platform."""
    system, arch = _getPlatformContext()
    if system == "Darwin":
        return PRESET_MACOS_ARM if arch == "arm64" else PRESET_MACOS_INTEL
    if system == "Windows":
        return PRESET_WINDOWS
    if system == "Linux":
        return PRESET_LINUX
    return "default"


def getPlatformDisplayName() -> str:
    """Return human-readable platform name (e.g. macOS (Apple Silicon))."""
    system, arch = _getPlatformContext()
    if system == "Darwin":
        return PLATFORM_NAME_MACOS_ARM if arch == "arm64" else PLATFORM_NAME_MACOS_INTEL
    if system == "Windows":
        return PLATFORM_NAME_WINDOWS
    if system == "Linux":
        return PLATFORM_NAME_LINUX
    return system


def getPlatformBuildConfig() -> tuple:
    """Return (buildDir, presetName) for current platform."""
    return getBuildDirectory(), getPlatformPreset()
