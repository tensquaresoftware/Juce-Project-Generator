cmake_minimum_required(VERSION 3.22)

# Platform-specific configuration
if(APPLE)
    # Architecture is set per-preset in CMakeUserPresets.json (arm64 for Apple Silicon, x86_64 for Intel)
    if(NOT CMAKE_OSX_ARCHITECTURES)
        set(CMAKE_OSX_ARCHITECTURES "arm64" CACHE STRING "Build architectures for macOS (arm64 or x86_64)")
    endif()
    # Use Ninja generator on macOS if not specified
    if(NOT CMAKE_GENERATOR)
        find_program(NINJA_EXE ninja)
        if(NINJA_EXE)
            set(CMAKE_GENERATOR "Ninja" CACHE INTERNAL "")
        endif()
    endif()
elseif(WIN32)
    # Use Visual Studio generator on Windows if not specified
    if(NOT CMAKE_GENERATOR)
        set(CMAKE_GENERATOR "Visual Studio 17 2022" CACHE INTERNAL "")
    endif()
endif()

project({projectName} VERSION {projectVersion})

# Plugin copy configuration (edit project-config.cmake to customize)
include(project-config.cmake)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Reference JUCE: priority cache (preset/-D), then ENV, then platform default
# Portable logic - works on any platform regardless of where the project was generated
set(JUCE_DIR_CANDIDATE "")
if(DEFINED JUCE_DIR AND NOT JUCE_DIR STREQUAL "" AND EXISTS "${{JUCE_DIR}}")
    set(JUCE_DIR_CANDIDATE "${{JUCE_DIR}}")
elseif(DEFINED ENV{{JUCE_DIR}} AND NOT "$ENV{{JUCE_DIR}}" STREQUAL "")
    set(JUCE_DIR_CANDIDATE "$ENV{{JUCE_DIR}}")
elseif(APPLE AND EXISTS "/Applications/JUCE")
    set(JUCE_DIR_CANDIDATE "/Applications/JUCE")
elseif(WIN32 AND EXISTS "C:/Program Files/JUCE")
    set(JUCE_DIR_CANDIDATE "C:/Program Files/JUCE")
elseif(UNIX AND EXISTS "/usr/local/JUCE")
    set(JUCE_DIR_CANDIDATE "/usr/local/JUCE")
endif()

if(JUCE_DIR_CANDIDATE STREQUAL "")
    message(FATAL_ERROR "JUCE not found. Set JUCE_DIR (e.g. export JUCE_DIR=/Applications/JUCE) or use -DJUCE_DIR=/path/to/JUCE")
endif()

set(JUCE_DIR "${{JUCE_DIR_CANDIDATE}}" CACHE PATH "Path to JUCE installation" FORCE)

if(NOT EXISTS "${{JUCE_DIR}}")
    message(FATAL_ERROR "JUCE not found at ${{JUCE_DIR}}. Check JUCE_DIR path.")
endif()

add_subdirectory(${{JUCE_DIR}} "${{CMAKE_BINARY_DIR}}/JUCE")

# ============================================================================
# SOURCE FILES
# Add your new .cpp files here (keep them sorted alphabetically for clarity)
# ============================================================================

set(PLUGIN_SOURCES
    # Core
    Source/PluginProcessor.cpp
    Source/PluginEditor.cpp
    Source/PluginFactory.cpp
    
    # Add your new source files below
)

# =============================================================================
# PLUGIN CONFIGURATION
# =============================================================================

# Platform-specific plugin formats (filter out AU on Windows)
set(PLUGIN_FORMATS_LIST {pluginFormats})
if(NOT APPLE)
    # Remove AU from formats on non-Apple platforms
    string(REPLACE "AU " "" PLUGIN_FORMATS_LIST "${{PLUGIN_FORMATS_LIST}}")
    string(REPLACE " AU" "" PLUGIN_FORMATS_LIST "${{PLUGIN_FORMATS_LIST}}")
    string(REPLACE "AU" "" PLUGIN_FORMATS_LIST "${{PLUGIN_FORMATS_LIST}}")
    string(STRIP "${{PLUGIN_FORMATS_LIST}}" PLUGIN_FORMATS_LIST)
endif()

# COPY_PLUGIN_AFTER_BUILD: copy to system folders on macOS (AU: Components, VST3: VST3)
# Controlled by COPY_TO_SYSTEM_FOLDERS in project-config.cmake (macOS only)
if(APPLE)
    set(COPY_PLUGIN_AFTER_BUILD_VALUE ${{COPY_TO_SYSTEM_FOLDERS}})
else()
    set(COPY_PLUGIN_AFTER_BUILD_VALUE FALSE)
endif()

juce_add_plugin({projectName}
    COMPANY_NAME "{manufacturerName}"
    BUNDLE_ID "{bundleId}"
    PLUGIN_MANUFACTURER_CODE {manufacturerCode}
    PLUGIN_CODE {pluginCode}
    FORMATS ${{PLUGIN_FORMATS_LIST}}
    PRODUCT_NAME "{projectName}"
	PLUGIN_NAME "{projectDisplayName}"
    IS_SYNTH {isSynth}
    NEEDS_MIDI_INPUT {needsMidiInput}
    NEEDS_MIDI_OUTPUT {needsMidiOutput}
    IS_MIDI_EFFECT {isMidiEffect}
    EDITOR_WANTS_KEYBOARD_FOCUS FALSE
    COPY_PLUGIN_AFTER_BUILD ${{COPY_PLUGIN_AFTER_BUILD_VALUE}}
    VST3_CATEGORIES {vst3Categories}
    AU_MAIN_TYPE {auMainType}
)

target_sources({projectName} PRIVATE ${{PLUGIN_SOURCES}})

target_link_libraries({projectName}
    PRIVATE
        juce::juce_audio_utils
        juce::juce_dsp
    PUBLIC
        juce::juce_recommended_config_flags
        juce::juce_recommended_lto_flags
        juce::juce_recommended_warning_flags
)

target_compile_definitions({projectName}
    PUBLIC
        JUCE_WEB_BROWSER=0
        JUCE_USE_CURL=0
        JUCE_VST3_CAN_REPLACE_VST2=0
        JUCE_DISPLAY_SPLASH_SCREEN=0
        JUCE_REPORT_APP_USAGE=0
)

# =============================================================================
# CUSTOM VST3 INSTALLATION (all platforms)
# Copy VST3 plugin to custom folder after build for easy testing
# =============================================================================
#
# Paths are defined in project-config.cmake. Set to NONE or "" to disable.
#
# =============================================================================

set(VST3_TARGET_NAME "{projectName}_VST3")
set(VST3_SOURCE_DIR "${{CMAKE_BINARY_DIR}}/{projectName}_artefacts/$<CONFIG>/VST3/{projectName}.vst3")

if(WIN32)
    set(CUSTOM_VST3_FOLDER "${{CUSTOM_VST3_FOLDER_WINDOWS}}")
elseif(APPLE)
    set(CUSTOM_VST3_FOLDER "${{CUSTOM_VST3_FOLDER_MACOS}}")
else()
    set(CUSTOM_VST3_FOLDER "${{CUSTOM_VST3_FOLDER_LINUX}}")
endif()

if(CUSTOM_VST3_FOLDER AND NOT CUSTOM_VST3_FOLDER STREQUAL "NONE")
    set(VST3_DEST_DIR "${{CUSTOM_VST3_FOLDER}}/{projectName}.vst3")
    add_custom_command(TARGET ${{VST3_TARGET_NAME}} POST_BUILD
        COMMAND ${{CMAKE_COMMAND}} -E echo "Copying VST3 plugin to custom folder: ${{CUSTOM_VST3_FOLDER}}"
        COMMAND ${{CMAKE_COMMAND}} -E make_directory "${{CUSTOM_VST3_FOLDER}}"
        COMMAND ${{CMAKE_COMMAND}} -E remove_directory "${{VST3_DEST_DIR}}"
        COMMAND ${{CMAKE_COMMAND}} -E copy_directory "${{VST3_SOURCE_DIR}}" "${{VST3_DEST_DIR}}"
        COMMENT "Installing VST3 plugin to custom folder"
        VERBATIM
    )
    message(STATUS "VST3 plugin will be copied to: ${{CUSTOM_VST3_FOLDER}}")
else()
    message(STATUS "VST3 custom folder disabled (set in project-config.cmake)")
endif()

# =============================================================================
# CUSTOM AU INSTALLATION (macOS only)
# Copy AU plugin to custom folder after build for easy testing
# =============================================================================
#
# Path is defined in project-config.cmake. Set to NONE or "" to disable.
#
# =============================================================================

if(APPLE AND CUSTOM_AU_FOLDER_MACOS AND NOT CUSTOM_AU_FOLDER_MACOS STREQUAL "NONE")
    set(AU_TARGET_NAME "{projectName}_AU")
    set(AU_SOURCE_DIR "${{CMAKE_BINARY_DIR}}/{projectName}_artefacts/$<CONFIG>/AU/{projectName}.component")
    set(AU_DEST_DIR "${{CUSTOM_AU_FOLDER_MACOS}}/{projectName}.component")
    add_custom_command(TARGET ${{AU_TARGET_NAME}} POST_BUILD
        COMMAND ${{CMAKE_COMMAND}} -E echo "Copying AU plugin to custom folder: ${{CUSTOM_AU_FOLDER_MACOS}}"
        COMMAND ${{CMAKE_COMMAND}} -E make_directory "${{CUSTOM_AU_FOLDER_MACOS}}"
        COMMAND ${{CMAKE_COMMAND}} -E remove_directory "${{AU_DEST_DIR}}"
        COMMAND ${{CMAKE_COMMAND}} -E copy_directory "${{AU_SOURCE_DIR}}" "${{AU_DEST_DIR}}"
        COMMENT "Installing AU plugin to custom folder"
        VERBATIM
    )
    message(STATUS "AU plugin will be copied to: ${{CUSTOM_AU_FOLDER_MACOS}}")
elseif(APPLE)
    message(STATUS "AU custom folder disabled (set in project-config.cmake)")
endif()