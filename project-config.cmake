# =============================================================================
# PROJECT CONFIGURATION - Plugin copy settings (Generator defaults)
# =============================================================================
#
# This file defines the default plugin copy settings used when generating
# new projects. Each generated project gets its own copy that you can edit.
#
# =============================================================================
# USER OPTIONS - Edit these values only
# =============================================================================
#
# Paths: "path" or NONE
#
set(USER_COPY_TO_SYSTEM_FOLDERS ON)
set(USER_CUSTOM_VST3_FOLDER_WINDOWS "C:/Users/Guillaume/Dev/Plugins/VST3")
set(USER_CUSTOM_VST3_FOLDER_MACOS "/Volumes/Guillaume/Dev/Plugins/VST3")
set(USER_CUSTOM_VST3_FOLDER_LINUX "/home/guillaume/Dev/Plugins/VST3")
set(USER_CUSTOM_AU_FOLDER_MACOS NONE)

# =============================================================================
# CODE - Do not edit below
# =============================================================================
set(COPY_TO_SYSTEM_FOLDERS ${USER_COPY_TO_SYSTEM_FOLDERS} CACHE BOOL "Copy plugins to system folders after build")
set(CUSTOM_VST3_FOLDER_WINDOWS ${USER_CUSTOM_VST3_FOLDER_WINDOWS} CACHE STRING "Custom VST3 folder (Windows)")
set(CUSTOM_VST3_FOLDER_MACOS ${USER_CUSTOM_VST3_FOLDER_MACOS} CACHE STRING "Custom VST3 folder (macOS)")
set(CUSTOM_VST3_FOLDER_LINUX ${USER_CUSTOM_VST3_FOLDER_LINUX} CACHE STRING "Custom VST3 folder (Linux)")
set(CUSTOM_AU_FOLDER_MACOS ${USER_CUSTOM_AU_FOLDER_MACOS} CACHE STRING "Custom AU folder (macOS)")
