# ==============================================================================
# PROJECT CONFIGURATION - Plugin copy settings (Generator defaults)
# ==============================================================================
#
# This file defines the default plugin copy settings used when generating
# new projects. Each generated project gets its own copy that you can edit.

# ==============================================================================
# USER OPTIONS - Edit these values only (Paths: "path" or NONE)
# ==============================================================================

# --- System ---
set(USER_COPY_TO_SYSTEM_FOLDERS ON)

# --- VST3 Plugin ---
set(USER_CUSTOM_VST3_FOLDER_WINDOWS "C:/Users/Guillaume/Dev/Plugins/VST3")
set(USER_CUSTOM_VST3_FOLDER_MACOS "/Volumes/Guillaume/Dev/Plugins/VST3")
set(USER_CUSTOM_VST3_FOLDER_LINUX "/home/guillaume/Dev/Plugins/VST3")

# --- AU Plugin (macOS only) ---
set(USER_CUSTOM_AU_FOLDER_MACOS "/Volumes/Guillaume/Dev/Plugins/AU")

# --- Standalone Application ---
set(USER_CUSTOM_STANDALONE_FOLDER_WINDOWS "C:/Users/Guillaume/Dev/Plugins/Standalone")
set(USER_CUSTOM_STANDALONE_FOLDER_MACOS "/Volumes/Guillaume/Dev/Plugins/Standalone")
set(USER_CUSTOM_STANDALONE_FOLDER_LINUX "/home/guillaume/Dev/Plugins/Standalone")


# ==============================================================================
# CODE - Do not edit below
# ==============================================================================

# --- System ---
set(COPY_TO_SYSTEM_FOLDERS ${USER_COPY_TO_SYSTEM_FOLDERS} CACHE BOOL "Copy plugins to system folders after build")

# --- VST3 Plugin ---
set(CUSTOM_VST3_FOLDER_WINDOWS ${USER_CUSTOM_VST3_FOLDER_WINDOWS} CACHE STRING "Custom VST3 folder (Windows)")
set(CUSTOM_VST3_FOLDER_MACOS ${USER_CUSTOM_VST3_FOLDER_MACOS} CACHE STRING "Custom VST3 folder (macOS)")
set(CUSTOM_VST3_FOLDER_LINUX ${USER_CUSTOM_VST3_FOLDER_LINUX} CACHE STRING "Custom VST3 folder (Linux)")

# --- AU Plugin (macOS only) ---
set(CUSTOM_AU_FOLDER_MACOS ${USER_CUSTOM_AU_FOLDER_MACOS} CACHE STRING "Custom AU folder (macOS)")

# --- Standalone Application ---
set(CUSTOM_STANDALONE_FOLDER_WINDOWS ${USER_CUSTOM_STANDALONE_FOLDER_WINDOWS} CACHE STRING "Custom Standalone folder (Windows)")
set(CUSTOM_STANDALONE_FOLDER_MACOS ${USER_CUSTOM_STANDALONE_FOLDER_MACOS} CACHE STRING "Custom Standalone folder (macOS)")
set(CUSTOM_STANDALONE_FOLDER_LINUX ${USER_CUSTOM_STANDALONE_FOLDER_LINUX} CACHE STRING "Custom Standalone folder (Linux)")
