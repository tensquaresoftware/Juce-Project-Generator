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
#   When ON (macOS only): copies AU to ~/Library/Audio/Plug-Ins/Components/,
#   VST3 to ~/Library/Audio/Plug-Ins/VST3/. No effect on Windows/Linux.
#
# COPY_TO_PROJECT_FOLDERS: ON/OFF
#   When ON: copies build outputs (AU, VST3, Standalone) to project_root/Artefacts/,
#   organized by platform and architecture (macOS: ARM/Intel/Intel-Rosetta/Universal,
#   Windows, Linux). No path to configure.
#
# ==============================================================================

set(USER_COPY_TO_SYSTEM_FOLDERS ON)
set(USER_COPY_TO_PROJECT_FOLDERS ON)

# ==============================================================================
# CODE - Do not edit below
# ==============================================================================

set(COPY_TO_SYSTEM_FOLDERS ${USER_COPY_TO_SYSTEM_FOLDERS} CACHE BOOL "Copy plugins to system folders after build (macOS only)")
set(COPY_TO_PROJECT_FOLDERS ${USER_COPY_TO_PROJECT_FOLDERS} CACHE BOOL "Copy build outputs to project Artefacts/ folder (organized by platform/architecture)")
