# JUCE Project Generator for CMake + Cursor

A Python-based project generator that creates complete JUCE plugin projects with CMake build system, optimized for development in Cursor (or VS Code).

---

**Author:** Guillaume DUPONT  
**Organization:** Ten Square Software  
**Revision date:** 2026-03-17

---

## Features

- ✅ Complete JUCE plugin project structure
- ✅ CMake build system configuration
- ✅ Platform-specific settings (macOS Apple Silicon/Intel/Intel-Rosetta/Universal Binary, Windows, Linux)
- ✅ Cross-platform path normalization (automatic handling of Windows/macOS path differences)
- ✅ Cursor/VS Code integration (tasks, launch configs, settings)
- ✅ **Smart build artefact management:**
  - **System folders**: copies plugins where DAWs look by default (macOS: `~/Library/Audio/Plug-Ins/`, Windows: `%LOCALAPPDATA%\Programs\Common\VST3\`, Linux: `~/.vst3/`)
  - **Central custom folder**: one organized location for all your projects' plugins (paths per OS, configured once in `generator-configuration.py`, injected at generation)
- ✅ Support for AU, VST3, and Standalone formats
- ✅ Configurable via `generator-configuration.py` and `project-configuration.cmake` for easy customization
- ✅ Customizable default manufacturer and plugin codes
- ✅ **Portable workflow**: projects use `JUCE_DIR` from the environment—no machine-specific paths in Git; ideal for GitHub and multi-machine (macOS / Windows / Linux) development

## Quick Start

### Prerequisites

- Python 3.7+
- JUCE 8 installed
- CMake 3.22+
- Ninja (required on Linux; on macOS/Windows, Ninja or platform generator)
- Cursor or VS Code

### Platform-specific prerequisites (Linux)

- CMake 3.22+ (3.27+ recommended)
- Ninja (`sudo apt install ninja-build`)
- GCC, GDB, build-essential
- **JUCE_DIR**: Must be set in your environment (see [Portable workflow](#portable-workflow-github-multi-machine) below).

### Setup

1. **Set `JUCE_DIR` in your environment** (required for building):
   
   Generated projects use `${env:JUCE_DIR}` everywhere (tasks and CMake Tools). Configure it once per machine so that the same project builds on macOS, Windows, and Linux without any path in Git.
   
   - **macOS** (e.g. `~/.zshrc`): `export JUCE_DIR="/Applications/JUCE"`
   - **Windows** (cmd): `setx JUCE_DIR "C:\Path\To\JUCE"` then restart the terminal; or set it in System → Environment variables.
   - **Linux** (e.g. `~/.bashrc`): `export JUCE_DIR="/home/username/Dev/JUCE"`
   
   Restart Cursor (or at least the integrated terminal) after changing the environment.

2. **Configure your environment** (optional, for the generator only):
   
   - Copy `generator-configuration.py` and `project-configuration.cmake` and customize them (see Configuration section below). The `JUCE_DIR_*` options in `generator-configuration.py` are only used for **validation** when generating; they are not written into generated projects.

3. **Run the generator** (see [Using the generator](#using-the-generator) below for detailed examples).

4. **Follow the interactive prompts** to create your project.

---

## Using the generator

You can run the generator in two ways: from an **IDE** (Cursor, Visual Studio, CLion, etc.) or from the **Terminal**. Both produce the same result. Choose what you are most comfortable with.

### Option A: From Cursor (IDE) — for beginners

If you prefer to work entirely in Cursor and avoid the command line:

1. **Open the generator folder in Cursor**
   - File → Open Folder (or `Cmd+O` on macOS, `Ctrl+O` on Windows/Linux)
   - Select the folder that contains `generate-new-project.py` (e.g. `Juce-Project-Generator`)

2. **Open the integrated terminal**
   - View → Terminal (or `` Ctrl+` `` / `` Cmd+` ``)
   - You should see a prompt in the generator folder.

3. **Run the generator**
   - Type: `python3 generate-new-project.py` (or `python generate-new-project.py` on Windows)
   - Press **Enter**.

4. **Answer the questions**
   - The generator will ask you for: project name, display name, version, manufacturer, plugin codes, formats (AU, VST3, Standalone), and destination folder.
   - You can press **Enter** to accept the value in square brackets (e.g. `[Y/n]` → Enter = Yes).
   - At the end, confirm with **Y** to create the project.

5. **Open the new project**
   - The generator prints a command like: `cd /path/to/YourProject && cursor .`
   - Copy that line into the terminal and press Enter, or use File → Open Folder and select the project folder.

6. **Choose your build configuration**
   - Cursor will ask you to select a **CMake preset** (e.g. "macOS Apple Silicon", "macOS Universal", "Windows x64").
   - Choose the one that matches your machine and what you want to build.
   - Then press **Cmd+Shift+B** (macOS) or **Ctrl+Shift+B** (Windows/Linux) to build.

That’s it. No need to run any other script or edit config files for a normal workflow.

---

### Option B: From the Terminal — for command-line users

If you prefer the command line or want to automate things (e.g. scripts, CI):

1. **Open a terminal** (Terminal.app on macOS, PowerShell or Command Prompt on Windows, or your usual terminal on Linux).

2. **Go to the generator folder**
   ```bash
   cd /path/to/Juce-Project-Generator
   ```
   (Replace `/path/to/Juce-Project-Generator` with the real path, e.g. `~/Dev/Tools/JUCE/Scripts/Juce-Project-Generator`.)

3. **Run the generator**
   ```bash
   python3 generate-new-project.py
   ```
   On Windows you can use:
   ```bash
   python generate-new-project.py
   ```

4. **Answer the prompts**
   - Same questions as in the IDE: project name, display name, version, manufacturer, plugin codes, formats, destination.
   - Use **Enter** to accept defaults where applicable.
   - Type **y** and Enter at the end to create the project.

5. **Build the generated project from the terminal** (optional)
   - Go to the project folder:
     ```bash
     cd /path/to/YourProject
     ```
   - Configure with a preset (example for macOS Universal):
     ```bash
     cmake --preset default-macos-universal
     ```
   - Build:
     ```bash
     cmake --build --preset default-macos-universal
     ```
   - Other examples:
     - **macOS Apple Silicon:** `cmake --preset default-macos-arm64` then `cmake --build --preset default-macos-arm64`
     - **Windows:** `cmake --preset default-windows` then `cmake --build --preset default-windows`
     - **Linux:** `cmake --preset default-linux` then `cmake --build --preset default-linux`

To see all presets available on your machine:
```bash
cmake --list-presets
```

---

## Configuration

The generator uses two configuration files (both in the generator directory):

- **`generator-configuration.py`**: Generator-specific settings (defaults for prompts, JUCE validation)
- **`project-configuration.cmake`**: Build artefact copy settings used as defaults when creating new projects. Each generated project gets its own copy of this file at the project root, which you can edit afterward to customize where AU, VST3, and Standalone are copied after each build.

### Setup

1. **Create or Edit `generator-configuration.py`**:
   
   The `generator-configuration.py` file should be located in the same directory as `generate-new-project.py`.
   
   If the file doesn't exist, the generator will use default values. You can create it by copying the example below.

2. **Create or Edit `project-configuration.cmake`** (in the generator directory):
   
   This file defines default build artefact copy options for new projects (system folders and central artefacts folder). Edit it to match your workflow. If it doesn't exist, the generator uses built-in defaults.

3. **Configure Your Settings**:
   
   Edit `generator-configuration.py` and `project-configuration.cmake` to match your environment.

### Configuration Options

#### `JUCE_DIR_MACOS`, `JUCE_DIR_WINDOWS`, `JUCE_DIR_LINUX`

**Purpose**: Optional. Used **only for validation** when generating (warns if the path doesn't exist). These values are **not** written into generated projects.

**Why**: Generated projects use `${env:JUCE_DIR}` in `.vscode/settings.json` and in the CMake: Configure task. So the same repo can be cloned on macOS, Windows, and Linux; on each machine you set `JUCE_DIR` in the environment once, and the project builds without any machine-specific paths in Git.

**Examples** (for validation only):

- macOS: `JUCE_DIR_MACOS = "/Applications/JUCE"`
- Windows: `JUCE_DIR_WINDOWS = "C:/JUCE"` or `"C:/Program Files/JUCE"`
- Linux: `JUCE_DIR_LINUX = "/home/username/Dev/JUCE"` or `"/opt/JUCE"`

**Note**: If set to `None`, the generator skips path validation. **Building** always requires `JUCE_DIR` to be set in your shell/IDE environment on each machine (see [Portable workflow](#portable-workflow-github-multi-machine)).

#### `project-configuration.cmake` (in generator directory)

**Purpose**: Defines default build artefact copy settings for new projects. The generator reads this file and copies its values into each generated project.

**Structure**: Edit only the **USER OPTIONS** section at the top. The **CODE** section below must not be modified.

**Example** (excerpt):

```cmake
# USER OPTIONS - Edit these values only
set(USER_COPY_TO_SYSTEM_FOLDERS ON)
set(USER_COPY_TO_ARTEFACTS_DIR ON)

# CODE - Do not edit below
set(COPY_TO_SYSTEM_FOLDERS ${USER_COPY_TO_SYSTEM_FOLDERS} CACHE BOOL "...")
set(COPY_TO_ARTEFACTS_DIR ${USER_COPY_TO_ARTEFACTS_DIR} CACHE BOOL "...")
# Central artefacts directories (per OS) - injected at generation
set(ARTEFACTS_DIR_WINDOWS "C:/Users/Guillaume/Dev/JUCE/Artefacts")
set(ARTEFACTS_DIR_MACOS   "/Volumes/Guillaume/Dev/JUCE/Artefacts")
set(ARTEFACTS_DIR_LINUX   "/home/guillaume/Dev/JUCE/Artefacts")
```

- **`USER_COPY_TO_SYSTEM_FOLDERS`**: `ON` or `OFF` — when ON, copies plugins to system folders where DAWs look by default:
  - macOS: AU → `~/Library/Audio/Plug-Ins/Components/`, VST3 → `~/Library/Audio/Plug-Ins/VST3/`
  - Windows: VST3 → `%LOCALAPPDATA%\Programs\Common\VST3\`
  - Linux: VST3 → `~/.vst3/`
- **`USER_COPY_TO_ARTEFACTS_DIR`**: `ON` or `OFF` — when ON, copies build outputs (AU, VST3, Standalone) to a central custom folder (paths `ARTEFACTS_DIR_*` injected from `generator-configuration.py`), organized by platform and architecture (macOS: ARM/Intel/Intel-Rosetta/Universal).

#### `ARTEFACTS_DIR_WINDOWS`, `ARTEFACTS_DIR_MACOS`, `ARTEFACTS_DIR_LINUX`

**Purpose**: Defines the central custom folder where all projects' build outputs (plugins and Standalone) are copied (per OS). These paths are injected into generated projects at generation time.

**Structure**:
- Windows: `ARTEFACTS_DIR_WINDOWS/Windows/VST3/`, `/Standalone/`
- macOS: `ARTEFACTS_DIR_MACOS/macOS/{ARM|Intel|Intel-Rosetta|Universal}/AU/`, `/VST3/`, `/Standalone/`
- Linux: `ARTEFACTS_DIR_LINUX/Linux/VST3/`, `/Standalone/` (CLAP/ for future)

**Examples**:
- Windows: `ARTEFACTS_DIR_WINDOWS = "C:/Users/Guillaume/Dev/JUCE/Artefacts"`
- macOS: `ARTEFACTS_DIR_MACOS = "/Volumes/Guillaume/Dev/JUCE/Artefacts"`
- Linux: `ARTEFACTS_DIR_LINUX = "/home/guillaume/Dev/JUCE/Artefacts"`

**Note**: These paths are injected at generation. On a different machine (e.g. after cloning from GitHub), either edit `project-configuration.cmake` in the generated project to update `ARTEFACTS_DIR_*`, or regenerate the project with your local `generator-configuration.py`.

#### `DEFAULT_PROJECT_DIR_WINDOWS`, `DEFAULT_PROJECT_DIR_MACOS`, `DEFAULT_PROJECT_DIR_LINUX`

**Purpose**: Sets the default folder where new projects will be created (per OS). The generator selects the appropriate path based on the current OS.

**Default**: If not set or set to `"Default"`, projects will be created on your Desktop.

**Examples**:

- Desktop: `"Default"` (uses system Desktop folder, works correctly on Windows even if displayed as "Bureau")
- Documents: `str(Path.home() / "Documents" / "Projects")`
- Custom: `"D:/Projects/JUCE"`

**Note**: The generator will always prompt for confirmation, so this is just a default suggestion.

**Important**: On Windows, use `"Default"` instead of a hardcoded path like `"C:/Users/YourName/Bureau"`. The system Desktop folder is internally named "Desktop" and using `"Default"` ensures it resolves correctly regardless of your Windows language settings.

**⚠️ IMPORTANT - Path Restrictions**:

- **NO ACCENTED CHARACTERS**: Paths must NOT contain accented characters (é, à, è, ç, etc.)
- **NO SPECIAL UNICODE**: Only ASCII characters (0-127) are allowed in paths
- **Why**: CMake and Visual Studio on Windows have known issues with Unicode paths, causing build errors (MSB8066) with malformed characters in generated `.vcxproj` files
- **Examples**:
  - ❌ `"C:/Users/John/Téléchargements"` (contains é)
  - ✅ `"C:/Users/John/Telechargements"` (no accents)
  - ❌ `"D:/Projets/Été 2024"` (contains é and É)
  - ✅ `"D:/Projets/Ete 2024"` (no accents)

The generator will **strictly validate** all paths and **stop immediately** with a clear error message if problematic characters are detected. It will NOT use fallback paths to avoid creating projects in unexpected locations.

#### `DEFAULT_MANUFACTURER_NAME`, `DEFAULT_MANUFACTURER_CODE`, `DEFAULT_PLUGIN_CODE`

**Purpose**: Sets default values for manufacturer and plugin identification codes used when generating new projects.

**Why**: These values are used as defaults in the interactive prompts, saving time when generating multiple projects for the same manufacturer.

**Examples**:

- Manufacturer Name: `"My Company"`, `"Acme Audio"`
- Manufacturer Code: `"MyCo"`, `"Acme"` (must be exactly 4 alphabetic characters)
- Plugin Code: `"Plg1"`, `"Fx01"` (must be exactly 4 alphanumeric characters)

**Note**: 

- These codes are used internally by JUCE for plugin identification
- The Plugin Code must be unique for each plugin you create
- You can still override these values when generating a project

### Example `generator-configuration.py`

```python
#!/usr/bin/env python3
"""
Generator Configuration file for JUCE Project Generator
========================================================

Customize the values below to match your development environment.
"""

# JUCE installation paths (optional: used only for validation when generating, not written into projects)
JUCE_DIR_MACOS = "/Applications/JUCE"
JUCE_DIR_WINDOWS = "C:/JUCE"
JUCE_DIR_LINUX = "/home/username/Dev/JUCE"  # or None to skip; set env JUCE_DIR on each machine for building

# Central artefacts folder (custom folder for all projects' plugins/Standalone, per OS)
ARTEFACTS_DIR_WINDOWS = "C:/Users/Guillaume/Dev/JUCE/Artefacts"
ARTEFACTS_DIR_MACOS   = "/Volumes/Guillaume/Dev/JUCE/Artefacts"
ARTEFACTS_DIR_LINUX   = "/home/guillaume/Dev/JUCE/Artefacts"

# Default project destination (per OS)
DEFAULT_PROJECT_DIR_WINDOWS = "C:/Users/Guillaume/Dev/JUCE/Projects"
DEFAULT_PROJECT_DIR_MACOS   = "/Volumes/Guillaume/Dev/JUCE/Projects"
DEFAULT_PROJECT_DIR_LINUX   = "/home/guillaume/Dev/JUCE/Projects"

# Default manufacturer information
DEFAULT_MANUFACTURER_NAME = "My Company"
DEFAULT_MANUFACTURER_CODE = "Myco"
DEFAULT_PLUGIN_CODE = "Plg1"
```

**Note**: Build artefact copy settings are in `project-configuration.cmake` (same format as in generated projects).

### How It Works

1. When you run `generate-new-project.py`, it loads `generator-configuration.py` for generator settings
2. It reads `project-configuration.cmake` (in the generator directory) for build artefact copy defaults
3. If `generator-configuration.py` doesn't exist or constants are missing, default values are used
4. If `project-configuration.cmake` doesn't exist, built-in defaults are used for build artefact copy
5. The values are injected into the generated project templates

### Customizing Generated Projects

**Each generated project includes its own `project-configuration.cmake`** at the project root. This file controls where build outputs (AU, VST3, Standalone) are copied after each build. You can edit it at any time—no need to regenerate the project.

To change build artefact copy options for a specific project, open `project-configuration.cmake` in that project and edit the **USER OPTIONS** section only:

- **`USER_COPY_TO_SYSTEM_FOLDERS`**: `ON` or `OFF` — copy to system folders (all OS: macOS AU/VST3, Windows VST3, Linux VST3)
- **`USER_COPY_TO_ARTEFACTS_DIR`**: `ON` or `OFF` — copy to central custom folder (paths `ARTEFACTS_DIR_*` injected at generation)

Override at configure time:

```bash
cmake .. -DUSER_COPY_TO_ARTEFACTS_DIR=OFF
```

## Generated Project Structure

```
YourProject/
├── project-configuration.cmake ← Build artefact copy settings (edit to customize)
├── Source/
│   ├── PluginProcessor.h
│   ├── PluginProcessor.cpp
│   ├── PluginEditor.h
│   ├── PluginEditor.cpp
│   └── PluginFactory.cpp
├── Builds/
│   ├── macOS/
│   │   ├── ARM/           ← Apple Silicon native
│   │   ├── Intel/         ← Mac Intel native (x86_64)
│   │   ├── Intel-Rosetta/ ← x86_64 on Apple Silicon (cross-compiled)
│   │   └── Universal/     ← Universal Binary (Apple Silicon + Intel, for distribution)
│   ├── Windows/
│   └── Linux/
├── .vscode/
│   ├── settings.json
│   ├── tasks.json
│   └── launch.json
├── CMakeLists.txt
├── CMakeUserPresets.json
└── README.md
```

Build directories are separated by platform and architecture to avoid mixing files when switching between Mac Intel and Apple Silicon, or between different operating systems.

## Usage

### Building a generated project

**In Cursor (recommended for beginners):**

1. Open the project folder in Cursor (File → Open Folder).
2. When Cursor asks, **select a CMake preset** (e.g. "macOS Apple Silicon", "macOS Universal", "Windows x64"). Only presets for your current operating system are shown.
3. Build: press **Cmd+Shift+B** (macOS) or **Ctrl+Shift+B** (Windows/Linux), or use the command palette: **Cmd+Shift+P** → "CMake: Build".
4. To switch to another configuration (e.g. from ARM to Universal on macOS), click the preset name in the status bar at the bottom of Cursor, or use **Cmd+Shift+P** → "CMake: Select Configure Preset". Paths and tasks update automatically.

**From the Terminal:**

```bash
# Go to your project folder
cd /path/to/YourProject

# Configure with the preset you want (example: macOS Universal)
cmake --preset default-macos-universal

# Build
cmake --build --preset default-macos-universal
```

**Preset vs machine:** The generated project's CMake enforces consistency: on **Apple Silicon**, the "macOS Intel" preset is rejected at configure (use "macOS Intel-Rosetta" instead); on **Mac Intel**, the "macOS Intel-Rosetta" preset is rejected (use "macOS Intel" instead). You get an explicit error message if you choose the wrong one.

Other presets (use the one that matches your machine and goal):

```bash
# macOS Apple Silicon
cmake --preset default-macos-arm64 && cmake --build --preset default-macos-arm64

# macOS Intel (native on Mac Intel only — use Intel-Rosetta on Apple Silicon)
cmake --preset default-macos-x86_64 && cmake --build --preset default-macos-x86_64

# macOS Intel-Rosetta (x86_64 on Apple Silicon only — use Intel on Mac Intel)
cmake --preset default-macos-x86_64-rosetta && cmake --build --preset default-macos-x86_64-rosetta

# macOS Universal (Apple Silicon + Intel, for distribution)
cmake --preset default-macos-universal && cmake --build --preset default-macos-universal

# Windows
cmake --preset default-windows && cmake --build --preset default-windows

# Linux
cmake --preset default-linux && cmake --build --preset default-linux
```

To list all presets available on your system: `cmake --list-presets`.

### Testing Plugins

After building, plugins are automatically copied according to your `project-configuration.cmake` settings:

**When `COPY_TO_SYSTEM_FOLDERS` is ON** (all OS): Plugins go to system folders where DAWs scan automatically:
- **macOS**: AU and VST3 → `~/Library/Audio/Plug-Ins/`
- **Windows**: VST3 → `%LOCALAPPDATA%\Programs\Common\VST3\`
- **Linux**: VST3 → `~/.vst3/`

Your DAW will find them automatically after a rescan.

**When `COPY_TO_ARTEFACTS_DIR` is ON**: Plugins go to your central custom folder (paths configured in `generator-configuration.py`). Add this folder to your DAW's plugin search path if needed.

#### macOS

**System folders location** (when `COPY_TO_SYSTEM_FOLDERS` is ON):
- AU: `~/Library/Audio/Plug-Ins/Components/`
- VST3: `~/Library/Audio/Plug-Ins/VST3/`

#### Windows

**System folders location** (when `COPY_TO_SYSTEM_FOLDERS` is ON):
- VST3: `%LOCALAPPDATA%\Programs\Common\VST3\`

#### Linux

**System folders location** (when `COPY_TO_SYSTEM_FOLDERS` is ON):
- VST3: `~/.vst3/`

### Debugging

Press `F5` in Cursor to start debugging. Debug configurations are available for:

- Standalone application
- Plugin in DAW (Logic Pro, Reaper, Ableton Live)

## Platform switching

If you open a project on another machine (different OS or, on macOS, different architecture—Intel vs Apple Silicon):

- **In Cursor:** Click the preset name in the status bar (bottom of the window), or use **Cmd+Shift+P** (macOS) / **Ctrl+Shift+P** (Windows/Linux) → "CMake: Select Configure Preset", then choose the preset that matches your current machine (e.g. `default-macos-arm64`, `default-macos-universal`, `default-windows`, `default-linux`). Build paths and debug configs update automatically.
- **From the Terminal:** Run `cmake --preset <preset-name>` then `cmake --build --preset <preset-name>` with the preset appropriate for that machine (see [Building a generated project](#building-a-generated-project) above).

No extra script is required. Just select the right preset and build.

## Portable workflow (GitHub, multi-machine)

The generator is designed so that **no machine-specific paths** are committed to Git. You can create a plugin on one machine, push to GitHub, then clone and build on your other machines (e.g. one macOS, one Windows, one Linux) without editing any project files.

### How it works

- Generated projects use **`${env:JUCE_DIR}`** in `.vscode/settings.json` and in the "CMake: Configure" task. The path to JUCE is never hardcoded.
- Each machine defines `JUCE_DIR` once in its environment. The same project then builds everywhere.

### One-time setup per machine

| Platform | Where to set | Example |
|----------|--------------|---------|
| **macOS** | `~/.zshrc` (or `~/.bash_profile`) | `export JUCE_DIR="/Applications/JUCE"` |
| **Linux** | `~/.bashrc` (or `~/.profile`) | `export JUCE_DIR="/home/username/Dev/JUCE"` |
| **Windows** | System env vars, or `setx`, or PowerShell `$PROFILE` | `setx JUCE_DIR "C:\Path\To\JUCE"` |

After changing the environment, restart Cursor (or at least the integrated terminal).

### Typical workflow

1. **Create** the project on any machine with the generator; push to GitHub.
2. **Clone** the repo on the other machines.
3. On each machine: ensure `JUCE_DIR` is set (see above), then open the project in Cursor and **select the CMake preset** that matches that machine (e.g. macOS ARM, Windows, Linux). Paths and tasks adapt automatically.
4. **Build** on each machine; no path edits are needed in the project.

This keeps the repository clean and portable for collaboration and multi-OS development.

## Customization

### Build Artefact Copy Configuration

Projects support **two independent copy destinations** after build:

1. **System folders** (all OS, where DAWs scan by default):
   - **macOS**: AU → `~/Library/Audio/Plug-Ins/Components/`, VST3 → `~/Library/Audio/Plug-Ins/VST3/`
   - **Windows**: VST3 → `%LOCALAPPDATA%\Programs\Common\VST3\`
   - **Linux**: VST3 → `~/.vst3/`
   - Controlled by `COPY_TO_SYSTEM_FOLDERS` in `project-configuration.cmake`
   - **Use case**: Instant testing in your DAW after each build

2. **Central custom artefacts folder** (centralized organization):
   - Copies to a **single custom folder** for all your projects (paths `ARTEFACTS_DIR_WINDOWS/MACOS/LINUX` injected from `generator-configuration.py` at generation)
   - **Structure**: `{ARTEFACTS_DIR}/{OS}/{arch}/{format}/`
     - macOS: organized by architecture (ARM, Intel, Intel-Rosetta, Universal)
     - Windows/Linux: organized by format only (VST3, Standalone)
   - Controlled by `COPY_TO_ARTEFACTS_DIR` in `project-configuration.cmake`
   - **Use case**: Keep all your plugins organized in one place, backup, distribution prep
   - **Note**: Paths are injected at generation. On a different machine, edit `project-configuration.cmake` to update paths or regenerate with local `generator-configuration.py`

Edit `project-configuration.cmake` in any generated project to toggle these options without modifying `CMakeLists.txt`.

## Path Restrictions

### ⚠️ IMPORTANT: No Accented Characters in Paths

**The generator STRICTLY prohibits accented characters and special Unicode characters in all paths.**

This includes:

- Project destination paths (`DEFAULT_PROJECT_DIR_*`)
- Central artefacts folder paths (`ARTEFACTS_DIR_*`)
- Any path entered during interactive prompts

**Why this restriction?**

CMake and Visual Studio on Windows have known compatibility issues with Unicode paths containing accented characters. This causes build errors such as:

- `MSB8066`: Custom build errors
- Malformed characters in generated `.vcxproj` files (e.g., `T├®l├®chargements` instead of `Téléchargements`)
- Build failures during compilation

**What characters are allowed?**

- ASCII characters only (0-127)
- Letters: `a-z`, `A-Z`
- Numbers: `0-9`
- Common path characters: `/`, `\`, `:`, `-`, `_`, spaces

**What characters are NOT allowed?**

- Accented characters: `é`, `à`, `è`, `ç`, `ù`, `ê`, `ô`, `î`, `û`, etc.
- Special Unicode characters
- Non-ASCII characters

**Examples:**

| ❌ Invalid                            | ✅ Valid                              |
| ------------------------------------ | ------------------------------------ |
| `C:/Users/John/Téléchargements` | `C:/Users/John/Telechargements` |
| `D:/Projets/Été 2024`                | `D:/Projets/Ete 2024`                |
| `C:/Users/John/Musique`         | `C:/Users/John/Musique`         |

**What happens if I use an invalid path?**

- The generator will detect problematic characters immediately
- A clear error message will be displayed showing which characters are problematic
- **The generator will STOP completely** and exit with an error code
- **NO fallback paths will be used** - this prevents creating projects in unexpected locations
- You must fix the path in `generator-configuration.py` or `project-configuration.cmake` (or enter a valid path during interactive prompts) before the generator will proceed

## Troubleshooting

### Generator uses default values even after creating config files

- Make sure `generator-configuration.py` is in the same directory as `generate-new-project.py`
- Make sure `project-configuration.cmake` is in the generator directory for build artefact copy defaults
- Check for syntax errors in `generator-configuration.py` (Python syntax) - the generator will display a warning if there are errors
- Verify that constant names match exactly (case-sensitive)
- If you see a warning about invalid codes, check that:
  - `DEFAULT_MANUFACTURER_CODE` is exactly 4 alphabetic characters
  - `DEFAULT_PLUGIN_CODE` is exactly 4 alphanumeric characters

### What happens if `generator-configuration.py` has errors?

The generator is designed to be resilient and will handle various error scenarios:

1. **Syntax errors in `generator-configuration.py`**:
   
   - The generator will display a warning message showing the error
   - Default values will be used instead
   - Project generation will continue normally

2. **Invalid manufacturer/plugin codes**:
   
   - If codes don't match the required format (4 characters), a warning is displayed
   - Default values are used instead
   - You can still override them during interactive prompts

3. **Invalid or missing JUCE path**:
   
   - If the path doesn't exist in `generator-configuration.py`, a warning is displayed
   - Project generation continues; for building, set the `JUCE_DIR` environment variable on each machine: `export JUCE_DIR=/path/to/JUCE` (see [Portable workflow](#portable-workflow-github-multi-machine))

4. **Missing constants**:
   
   - If a constant is not defined, the corresponding default value is used
   - No error is displayed (this is expected behavior)

### VST3/AU plugin not copying after build

- Ensure `COPY_TO_ARTEFACTS_DIR` or `COPY_TO_SYSTEM_FOLDERS` is `ON` in `project-configuration.cmake`
- When `COPY_TO_ARTEFACTS_DIR` is ON, build outputs go to the central custom folder (paths `ARTEFACTS_DIR_*` injected from `generator-configuration.py`)
- When `COPY_TO_SYSTEM_FOLDERS` is ON (all OS), plugins go to system folders (macOS: `~/Library/Audio/Plug-Ins/`, Windows: `%LOCALAPPDATA%\Programs\Common\VST3\`, Linux: `~/.vst3/`)

### JUCE not found (any platform)

CMake reports `JUCE not found. Set JUCE_DIR...` when `JUCE_DIR` is not set or not visible to the build.

1. **Set the environment variable** (recommended, portable): Add `export JUCE_DIR=/path/to/JUCE` to your shell profile (`~/.bashrc`, `~/.zshrc`, or Windows system/env vars). Restart Cursor or the terminal.
2. **On Linux**: Ensure Ninja is installed (`sudo apt install ninja-build`)—the Linux build uses Ninja, not Visual Studio.

### Build errors with paths containing accents

If you see errors like `MSB8066` or malformed characters in build output:

- **This should not happen** if you followed the path restrictions
- Check that your project path doesn't contain accented characters
- If you're using an existing project, consider moving it to a path without accents
- The generator validates paths at creation time, but if you manually moved the project, you may need to regenerate it

## Sharing the Generator

When sharing this generator:

1. Include `generator-configuration.py` and `project-configuration.cmake` with generic example values (as shown in the Configuration section)
2. Document that users should customize these files for their environment
3. Include this README.md in your distribution

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]
