# =============================================================================
# PROJECT CONFIGURATION - Plugin copy settings (Generator defaults)
# =============================================================================
#
# This file defines the default plugin copy settings used when generating
# new projects. It is read by the generator and copied into each new project.
#
# Edit this file to customize defaults for new projects. Generated projects
# get their own project-config.cmake that you can edit per-project.
#
# =============================================================================
# COPY TO SYSTEM FOLDERS (macOS AU & VST3)
# =============================================================================
#
# ON  = Copy AU to ~/Library/Audio/Plug-Ins/Components/
#       Copy VST3 to ~/Library/Audio/Plug-Ins/VST3/ (macOS only)
# OFF = No copy to system folders
#
set(COPY_TO_SYSTEM_FOLDERS ON CACHE BOOL "Copy plugins to system folders after build")

# =============================================================================
# CUSTOM VST3 FOLDERS (per platform)
# =============================================================================
#
# Set to "" to disable copy to a custom folder for that platform.
# Set to a path to enable copy (e.g. "/Users/username/Plugins/VST3")
#
set(CUSTOM_VST3_FOLDER_WINDOWS "C:/Users/Guillaume/Dev/Plugins/VST3" CACHE PATH "Custom VST3 folder (Windows), empty to disable")
set(CUSTOM_VST3_FOLDER_MACOS "/Volumes/Guillaume/Dev/Plugins/VST3" CACHE PATH "Custom VST3 folder (macOS), empty to disable")
set(CUSTOM_VST3_FOLDER_LINUX "/home/guillaume/Dev/Plugins/VST3" CACHE PATH "Custom VST3 folder (Linux), empty to disable")

# =============================================================================
# CUSTOM AU FOLDER (macOS only)
# =============================================================================
#
# Set to "" to disable copy to a custom AU folder.
# Set to a path to enable copy (e.g. "/Users/username/Plugins/AU")
#
set(CUSTOM_AU_FOLDER_MACOS "" CACHE PATH "Custom AU folder (macOS), empty to disable")
