# =============================================================================
# PROJECT CONFIGURATION - Plugin copy settings
# =============================================================================
#
# Edit the USER OPTIONS section below. Do not modify the CODE section.
# Override at configure: cmake .. -DUSER_COPY_TO_PROJECT_FOLDERS=ON
#
# =============================================================================
# USER OPTIONS - Edit these values only
# =============================================================================
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
# =============================================================================

set(USER_COPY_TO_SYSTEM_FOLDERS {copyToSystemFolders})
set(USER_COPY_TO_PROJECT_FOLDERS {copyToProjectFolders})

# =============================================================================
# CODE - Do not edit below
# =============================================================================
set(COPY_TO_SYSTEM_FOLDERS ${{USER_COPY_TO_SYSTEM_FOLDERS}} CACHE BOOL "Copy plugins to system folders after build (macOS only)")
set(COPY_TO_PROJECT_FOLDERS ${{USER_COPY_TO_PROJECT_FOLDERS}} CACHE BOOL "Copy build outputs to project Artefacts/ folder (organized by platform/architecture)")
