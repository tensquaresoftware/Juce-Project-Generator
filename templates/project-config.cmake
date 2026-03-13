# =============================================================================
# PROJECT CONFIGURATION - Plugin copy settings
# =============================================================================
#
# Edit the USER OPTIONS section below. Do not modify the CODE section.
# Override at configure: cmake .. -DUSER_CUSTOM_VST3_FOLDER_MACOS="/path"
#
# =============================================================================
# USER OPTIONS - Edit these values only
# =============================================================================
#
# Paths: "path" or NONE
#
# --- System ---
set(USER_COPY_TO_SYSTEM_FOLDERS {copyToSystemFolders})

# --- VST3 ---
set(USER_CUSTOM_VST3_FOLDER_WINDOWS "{customVst3FolderWindows}")
set(USER_CUSTOM_VST3_FOLDER_MACOS "{customVst3FolderMacOS}")
set(USER_CUSTOM_VST3_FOLDER_LINUX "{customVst3FolderLinux}")

# --- Standalone ---
set(USER_CUSTOM_STANDALONE_FOLDER_WINDOWS "{customStandaloneFolderWindows}")
set(USER_CUSTOM_STANDALONE_FOLDER_MACOS "{customStandaloneFolderMacOS}")
set(USER_CUSTOM_STANDALONE_FOLDER_LINUX "{customStandaloneFolderLinux}")

# --- AU (macOS only) ---
set(USER_CUSTOM_AU_FOLDER_MACOS "{customAuFolderMacOS}")

# =============================================================================
# CODE - Do not edit below
# =============================================================================
set(COPY_TO_SYSTEM_FOLDERS ${{USER_COPY_TO_SYSTEM_FOLDERS}} CACHE BOOL "Copy plugins to system folders after build")
set(CUSTOM_VST3_FOLDER_WINDOWS ${{USER_CUSTOM_VST3_FOLDER_WINDOWS}} CACHE STRING "Custom VST3 folder (Windows)")
set(CUSTOM_VST3_FOLDER_MACOS ${{USER_CUSTOM_VST3_FOLDER_MACOS}} CACHE STRING "Custom VST3 folder (macOS)")
set(CUSTOM_VST3_FOLDER_LINUX ${{USER_CUSTOM_VST3_FOLDER_LINUX}} CACHE STRING "Custom VST3 folder (Linux)")
set(CUSTOM_STANDALONE_FOLDER_WINDOWS ${{USER_CUSTOM_STANDALONE_FOLDER_WINDOWS}} CACHE STRING "Custom Standalone folder (Windows)")
set(CUSTOM_STANDALONE_FOLDER_MACOS ${{USER_CUSTOM_STANDALONE_FOLDER_MACOS}} CACHE STRING "Custom Standalone folder (macOS)")
set(CUSTOM_STANDALONE_FOLDER_LINUX ${{USER_CUSTOM_STANDALONE_FOLDER_LINUX}} CACHE STRING "Custom Standalone folder (Linux)")
set(CUSTOM_AU_FOLDER_MACOS ${{USER_CUSTOM_AU_FOLDER_MACOS}} CACHE STRING "Custom AU folder (macOS)")
