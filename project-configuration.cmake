# ==============================================================================
# PROJECT CONFIGURATION - Plugin copy settings (Generator defaults)
# ==============================================================================
#
# This file defines the default plugin copy settings used when generating
# new projects. Each generated project gets its own copy that you can edit.

# ==============================================================================
# USER OPTIONS - Edit these values only
# ==============================================================================
#
# COPY_TO_SYSTEM_FOLDERS: ON/OFF
#   When ON: copies plugins to system folders where DAWs look by default.
#   - macOS: AU → ~/Library/Audio/Plug-Ins/Components/, VST3 → ~/Library/Audio/Plug-Ins/VST3/
#   - Windows: VST3 → %LOCALAPPDATA%\Programs\Common\VST3\
#   - Linux: VST3 → ~/.vst3/
#
# COPY_TO_ARTEFACTS_DIR: ON/OFF
#   When ON: copies build outputs (AU, VST3, Standalone) to a central custom folder
#   (ARTEFACTS_DIR_WINDOWS/MACOS/LINUX, injected at generation from generator-configuration.py).
#   Organized by platform and architecture (macOS: ARM/Intel/Intel-Rosetta/Universal).
#
# ==============================================================================

set(USER_COPY_TO_SYSTEM_FOLDERS OFF)
set(USER_COPY_TO_ARTEFACTS_DIR ON)

# ==============================================================================
# CODE - Do not edit below
# ==============================================================================

set(COPY_TO_SYSTEM_FOLDERS ${USER_COPY_TO_SYSTEM_FOLDERS} CACHE BOOL "Copy plugins to system folders after build (all OS)")
set(COPY_TO_ARTEFACTS_DIR ${USER_COPY_TO_ARTEFACTS_DIR} CACHE BOOL "Copy build outputs to central artefacts folder (organized by platform/architecture)")

# Central artefacts directories (per OS) - defined in generator-configuration.py
set(ARTEFACTS_DIR_WINDOWS "C:/Users/Guillaume/Dev/JUCE/Artefacts")
set(ARTEFACTS_DIR_MACOS   "/Volumes/Guillaume/Dev/JUCE/Artefacts")
set(ARTEFACTS_DIR_LINUX   "/home/guillaume/Dev/JUCE/Artefacts")
