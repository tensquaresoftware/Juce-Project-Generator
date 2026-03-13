#!/usr/bin/env python3
"""
User Configuration file for JUCE Project Generator
===============================================================================

This file contains user-specific configuration constants that can be customized
for your development environment. Modify the values below to match your setup.

IMPORTANT: Before sharing this generator with others, make sure to:
1. Update the default paths below to generic/example values
2. Add clear comments explaining what each constant does
3. Document how users should customize these values
"""

# =============================================================================
# JUCE INSTALLATION PATH
# =============================================================================
#
# Path to your JUCE installation directory.
# Used only for validation when generating (warns if the path does not exist).
# These values are NOT written into generated projects.
#
# Generated projects use the JUCE_DIR environment variable instead. Set it once
# per machine so the same project can be built on macOS, Windows, and Linux
# without machine-specific paths in Git.
#
# Platform-specific examples:
#   - macOS: "/Applications/JUCE"
#   - Windows: "C:/JUCE" or "C:/Program Files/JUCE"
#   - Linux: "/usr/local/JUCE" or "/opt/JUCE"
#
JUCE_DIR_WINDOWS = "C:/Program Files/JUCE"
JUCE_DIR_MACOS   = "/Applications/JUCE"
JUCE_DIR_LINUX   = "/home/guillaume/Dev/JUCE"

# =============================================================================
# DEFAULT MANUFACTURER INFORMATION
# =============================================================================
#
# Default manufacturer name and code used when generating new projects.
# These values will be used as defaults in the project generator prompts.
# You can still override them when generating a project.
#
# Manufacturer Name: Full name of your company/manufacturer
#   Examples: "My Company", "Acme Audio"
#
# Manufacturer Code: 4-letter code (must be exactly 4 alphabetic characters)
#   Examples: "Myco", "MyCo", "Acme"
#   This code is used internally by JUCE for plugin identification.
#
# Plugin Code: 4-character code (must be exactly 4 alphanumeric characters)
#   Examples: "Mypl", "Plg1", "Fx01"
#   This code uniquely identifies your plugin and must be unique for each plugin.
#   It's used internally by JUCE for plugin identification.
#
DEFAULT_MANUFACTURER_NAME = "Ten Square Software"
DEFAULT_MANUFACTURER_CODE = "Tssf"
DEFAULT_PLUGIN_CODE       = "Tssp"

# =============================================================================
# DEFAULT PROJECT DESTINATION
# =============================================================================
#
# ⚠️ IMPORTANT - PATH RESTRICTIONS:
# -----------------------------------------------------------------------------
# Paths MUST NOT contain accented characters (é, à, è, ç, etc.) or special
# Unicode characters. Only ASCII characters (0-127) are allowed.
#
# This restriction exists because CMake and Visual Studio on Windows have
# known compatibility issues with Unicode paths, causing build errors (MSB8066)
# with malformed characters in generated .vcxproj files.
#
# Examples:
#   ❌ "C:/Users/John/Téléchargements"  (contains é)
#   ✅ "C:/Users/John/Telechargements"  (no accents)
#   ❌ "D:/Projets/Été 2024"            (contains é and É)
#   ✅ "D:/Projets/Ete 2024"            (no accents)
#
# The generator will STRICTLY validate this path and refuse to proceed if
# problematic characters are detected.
#
#
# Default folder where new projects will be created.
# This is used as the default value in the project generator prompt.
#
# Examples:
#   - Desktop: "Default" (uses system Desktop folder, works on Windows even if displayed as "Bureau")
#   - Documents: str(Path.home() / "Documents" / "Projects")
#   - Custom: "D:/Projects/JUCE"
#
# Note: The generator will prompt for confirmation, so this is just a default.
# "Default" = use user's Desktop (system folder, resolves correctly on Windows)
#
DEFAULT_PROJECT_DESTINATION = "Default"

# =============================================================================
# CUSTOM VST3 INSTALLATION FOLDER (all platforms)
# =============================================================================
#
# ⚠️ IMPORTANT - PATH RESTRICTIONS:
# -----------------------------------------------------------------------------
# Same restrictions as DEFAULT_PROJECT_DESTINATION - paths MUST NOT contain
# accented characters or special Unicode characters. Only ASCII characters
# (0-127) are allowed.
#
# The generator will STRICTLY validate these paths and refuse to proceed if
# problematic characters are detected.
#
# Default folder where VST3 plugins will be automatically copied after build.
# This allows easy testing in your DAW without requiring admin privileges.
# Each platform uses its own path when building.
#
# Examples:
#   - Windows:  "C:/Users/YourName/VST3"
#   - macOS:    "/Users/username/Plugins/VST3"
#   - Linux:    "/home/username/Plugins/VST3"
#
# Users can override when configuring CMake:
#   cmake .. -DCUSTOM_VST3_FOLDER="your/custom/path"
#
CUSTOM_VST3_FOLDER_WINDOWS = "C:/Users/Guillaume/Dev/Plugins/VST3"
CUSTOM_VST3_FOLDER_MACOS   = "/Volumes/Guillaume/Dev/Plugins/VST3"
CUSTOM_VST3_FOLDER_LINUX   = "/home/guillaume/Dev/Plugins/VST3"

# =============================================================================
# ADDITIONAL CONFIGURATION
# =============================================================================
#
# Add any other user-specific constants here as needed.
# For example:
#   - Build tool preferences
#   - etc.
#


# =============================================================================
# END OF FILE
# =============================================================================