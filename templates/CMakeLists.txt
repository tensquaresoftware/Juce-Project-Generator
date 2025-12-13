cmake_minimum_required(VERSION 3.22)

# Platform-specific configuration
if(APPLE)
    # Force arm64 for Apple Silicon (macOS only)
    set(CMAKE_OSX_ARCHITECTURES "arm64" CACHE STRING "Build architectures for macOS")
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

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Reference JUCE from configuration or environment variable
# Priority: 1) CMake variable JUCE_DIR, 2) Environment variable JUCE_DIR
if("{juceDir}" STREQUAL "")
    # No JUCE_DIR from user-config.py, check environment variable
    if(DEFINED ENV{{JUCE_DIR}})
        add_subdirectory($ENV{{JUCE_DIR}} "${{CMAKE_BINARY_DIR}}/JUCE")
    else()
        message(FATAL_ERROR "JUCE_DIR not set. Please either:\n"
            "  1. Set JUCE_DIR_MACOS/JUCE_DIR_WINDOWS/JUCE_DIR_LINUX in user-config.py before generating the project, or\n"
            "  2. Set JUCE_DIR environment variable, or\n"
            "  3. Configure CMake with: cmake .. -DJUCE_DIR=/path/to/JUCE")
    endif()
else()
    # Use JUCE_DIR from user-config.py (path is already normalized with forward slashes)
    set(JUCE_DIR "{juceDir}" CACHE PATH "Path to JUCE installation")
    add_subdirectory(${{JUCE_DIR}} "${{CMAKE_BINARY_DIR}}/JUCE")
endif()

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

# Platform-specific COPY_PLUGIN_AFTER_BUILD setting
if(APPLE)
    set(COPY_PLUGIN_AFTER_BUILD_VALUE TRUE)
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
# CUSTOM VST3 INSTALLATION (Windows)
# Copy VST3 plugin to custom folder after build for easy testing
# =============================================================================
#
# CONFIGURATION:
# ------------
# To customize the VST3 installation folder, modify the default value below
# or override it when configuring CMake:
#   cmake .. -DCUSTOM_VST3_FOLDER="your/custom/path"
#
# Examples:
#   - Personal folder: "C:/Users/YourName/VST3"
#   - Custom location: "D:/MyPlugins/VST3"
#   - Standard location (requires admin): "C:/Program Files/Common Files/VST3"
#
# Note: Using a personal folder avoids requiring administrator privileges.
#       Configure your DAW to scan this custom folder for VST3 plugins.
#
# =============================================================================

if(WIN32)
    # Define custom VST3 folder (can be overridden via CMake cache)
    if(NOT DEFINED CUSTOM_VST3_FOLDER)
        set(CUSTOM_VST3_FOLDER "{customVst3Folder}" CACHE PATH "Custom VST3 installation folder")
    endif()
    
    # VST3 target name (JUCE appends _VST3)
    set(VST3_TARGET_NAME "{projectName}_VST3")
    
    # Path where JUCE generates the VST3 bundle (using generator expression for CONFIG)
    set(VST3_SOURCE_DIR "${{CMAKE_BINARY_DIR}}/{projectName}_artefacts/$<CONFIG>/VST3/{projectName}.vst3")
    set(VST3_DEST_DIR "${{CUSTOM_VST3_FOLDER}}/{projectName}.vst3")
    
    # Add custom command to copy VST3 plugin after build
    add_custom_command(TARGET ${{VST3_TARGET_NAME}} POST_BUILD
        COMMAND ${{CMAKE_COMMAND}} -E echo "Copying VST3 plugin to custom folder: ${{CUSTOM_VST3_FOLDER}}"
        COMMAND ${{CMAKE_COMMAND}} -E make_directory "${{CUSTOM_VST3_FOLDER}}"
        COMMAND ${{CMAKE_COMMAND}} -E remove_directory "${{VST3_DEST_DIR}}"
        COMMAND ${{CMAKE_COMMAND}} -E copy_directory "${{VST3_SOURCE_DIR}}" "${{VST3_DEST_DIR}}"
        COMMENT "Installing VST3 plugin to custom folder"
        VERBATIM
    )
    
    message(STATUS "VST3 plugin will be copied to: ${{CUSTOM_VST3_FOLDER}}")
endif()