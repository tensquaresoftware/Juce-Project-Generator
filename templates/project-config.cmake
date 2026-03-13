# =============================================================================
# PROJECT CONFIGURATION - Plugin copy settings
# =============================================================================
#
# Edit this file to customize where plugins are copied after each build.
# These values are used by CMakeLists.txt. You can also override via:
#   cmake .. -DCOPY_TO_SYSTEM_FOLDERS=OFF -DCUSTOM_VST3_FOLDER_MACOS="/path"
#
# =============================================================================
# COPY TO SYSTEM FOLDERS (macOS AU & VST3)
# =============================================================================
#
# ON  = Copy AU to ~/Library/Audio/Plug-Ins/Components/
#       Copy VST3 to ~/Library/Audio/Plug-Ins/VST3/ (macOS only)
# OFF = No copy to system folders
#
set(COPY_TO_SYSTEM_FOLDERS {copyToSystemFolders} CACHE BOOL "Copy plugins to system folders after build")

# =============================================================================
# CUSTOM VST3 FOLDERS (per platform)
# =============================================================================
#
# Set to "" to disable copy to a custom folder for that platform.
# Set to a path to enable copy (e.g. "/Users/username/Plugins/VST3")
#
set(CUSTOM_VST3_FOLDER_WINDOWS "{customVst3FolderWindows}" CACHE PATH "Custom VST3 folder (Windows), empty to disable")
set(CUSTOM_VST3_FOLDER_MACOS "{customVst3FolderMacOS}" CACHE PATH "Custom VST3 folder (macOS), empty to disable")
set(CUSTOM_VST3_FOLDER_LINUX "{customVst3FolderLinux}" CACHE PATH "Custom VST3 folder (Linux), empty to disable")

# =============================================================================
# CUSTOM AU FOLDER (macOS only)
# =============================================================================
#
# Set to "" to disable copy to a custom AU folder.
# Set to a path to enable copy (e.g. "/Users/username/Plugins/AU")
#
set(CUSTOM_AU_FOLDER_MACOS "{customAuFolderMacOS}" CACHE PATH "Custom AU folder (macOS), empty to disable")
