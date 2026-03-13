# JUCE Project Generator for CMake + Cursor

A Python-based project generator that creates complete JUCE plugin projects with CMake build system, optimized for development in Cursor (or VS Code).

---

**Author:** Guillaume DUPONT  
**Organization:** Ten Square Software  
**Revision date:** 2026-03-12

---

## Features

- ✅ Complete JUCE plugin project structure
- ✅ CMake build system configuration
- ✅ Platform-specific settings (macOS Apple Silicon/Intel, Windows, Linux)
- ✅ Cross-platform path normalization (automatic handling of Windows/macOS path differences)
- ✅ Cursor/VS Code integration (tasks, launch configs, settings)
- ✅ Configurable plugin copy: system folders (macOS AU/VST3), custom VST3/AU folders (all platforms)
- ✅ Support for AU, VST3, and Standalone formats
- ✅ Configurable via `generator-config.py` and `project-config.cmake` for easy customization
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
   
   - Copy `generator-config.py` and `project-config.cmake` and customize them (see Configuration section below). The `JUCE_DIR_*` options in `generator-config.py` are only used for **validation** when generating; they are not written into generated projects.

3. **Run the generator**:
   
   ```bash
   python generate-new-juce-project.py
   ```

4. **Follow the interactive prompts** to create your project

## Configuration

The generator uses two configuration files (both in the generator directory):

- **`generator-config.py`**: Generator-specific settings (defaults for prompts, JUCE validation)
- **`project-config.cmake`**: Plugin copy settings used as defaults when creating new projects. Each generated project gets its own copy of this file at the project root, which you can edit afterward to customize VST3/AU copy paths for that project.

### Setup

1. **Create or Edit `generator-config.py`**:
   
   The `generator-config.py` file should be located in the same directory as `generate-new-juce-project.py`.
   
   If the file doesn't exist, the generator will use default values. You can create it by copying the example below.

2. **Create or Edit `project-config.cmake`** (in the generator directory):
   
   This file defines default plugin copy paths for new projects. Edit it to match your setup. If it doesn't exist, the generator uses built-in defaults.

3. **Configure Your Settings**:
   
   Edit `generator-config.py` and `project-config.cmake` to match your environment.

### Configuration Options

#### `JUCE_DIR_MACOS`, `JUCE_DIR_WINDOWS`, `JUCE_DIR_LINUX`

**Purpose**: Optional. Used **only for validation** when generating (warns if the path doesn't exist). These values are **not** written into generated projects.

**Why**: Generated projects use `${env:JUCE_DIR}` in `.vscode/settings.json` and in the CMake: Configure task. So the same repo can be cloned on macOS, Windows, and Linux; on each machine you set `JUCE_DIR` in the environment once, and the project builds without any machine-specific paths in Git.

**Examples** (for validation only):

- macOS: `JUCE_DIR_MACOS = "/Applications/JUCE"`
- Windows: `JUCE_DIR_WINDOWS = "C:/JUCE"` or `"C:/Program Files/JUCE"`
- Linux: `JUCE_DIR_LINUX = "/home/username/Dev/JUCE"` or `"/opt/JUCE"`

**Note**: If set to `None`, the generator skips path validation. **Building** always requires `JUCE_DIR` to be set in your shell/IDE environment on each machine (see [Portable workflow](#portable-workflow-github-multi-machine)).

#### `project-config.cmake` (in generator directory)

**Purpose**: Defines default plugin copy settings for new projects. The generator reads this file and copies its values into each generated project. Edit this file to customize defaults.

**Variables** (CMake format):

- **`COPY_TO_SYSTEM_FOLDERS`**: `ON` or `OFF` — copy AU and VST3 to system folders on macOS
- **`CUSTOM_VST3_FOLDER_WINDOWS`**, **`CUSTOM_VST3_FOLDER_MACOS`**, **`CUSTOM_VST3_FOLDER_LINUX`**: Path or `""` to disable
- **`CUSTOM_AU_FOLDER_MACOS`**: Path or `""` to disable (macOS only)

**Example** (excerpt):

```cmake
set(COPY_TO_SYSTEM_FOLDERS ON CACHE BOOL "...")
set(CUSTOM_VST3_FOLDER_MACOS "/Users/username/Plugins/VST3" CACHE PATH "...")
set(CUSTOM_AU_FOLDER_MACOS "" CACHE PATH "...")
```

**⚠️ IMPORTANT - Path Restrictions**: Same as `DEFAULT_PROJECT_DESTINATION` — paths must NOT contain accented or special Unicode characters.

#### `DEFAULT_PROJECT_DESTINATION`

**Purpose**: Sets the default folder where new projects will be created.

**Default**: If set to `"Default"`, projects will be created on your Desktop.

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

### Example `generator-config.py`

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

# Default project destination
# Set to "Default" to use Desktop, or specify a custom path
DEFAULT_PROJECT_DESTINATION = "Default"

# Default manufacturer information
# These will be used as defaults when generating new projects
DEFAULT_MANUFACTURER_NAME = "My Company"
DEFAULT_MANUFACTURER_CODE = "Myco"
DEFAULT_PLUGIN_CODE = "Plg1"
```

**Note**: Plugin copy settings are in `project-config.cmake` (same format as in generated projects).

### How It Works

1. When you run `generate-new-juce-project.py`, it loads `generator-config.py` for generator settings
2. It reads `project-config.cmake` (in the generator directory) for plugin copy defaults
3. If `generator-config.py` doesn't exist or constants are missing, default values are used
4. If `project-config.cmake` doesn't exist, built-in defaults are used for plugin copy
5. The values are injected into the generated project templates

### Customizing Generated Projects

**Each generated project includes its own `project-config.cmake`** at the project root. This file controls where plugins (VST3, AU) are copied after each build. You can edit it at any time—no need to regenerate the project.

To change plugin copy options for a specific project, open `project-config.cmake` in that project and edit:

- **`COPY_TO_SYSTEM_FOLDERS`**: Set to `ON` or `OFF` to enable/disable copy to system folders (macOS: `~/Library/Audio/Plug-Ins/Components/` and `~/Library/Audio/Plug-Ins/VST3/`)
- **`CUSTOM_VST3_FOLDER_WINDOWS`**, **`CUSTOM_VST3_FOLDER_MACOS`**, **`CUSTOM_VST3_FOLDER_LINUX`**: Path or `""` to disable
- **`CUSTOM_AU_FOLDER_MACOS`**: Path or `""` to disable (macOS only)

You can also override at configure time:

```bash
cmake .. -DCOPY_TO_SYSTEM_FOLDERS=OFF -DCUSTOM_VST3_FOLDER_MACOS="/your/path"
```

## Generated Project Structure

```
YourProject/
├── project-config.cmake   ← Plugin copy settings (edit to customize)
├── Source/
│   ├── PluginProcessor.h
│   ├── PluginProcessor.cpp
│   ├── PluginEditor.h
│   ├── PluginEditor.cpp
│   └── PluginFactory.cpp
├── Builds/
│   ├── macOS/
│   │   ├── ARM/      ← Apple Silicon (M1/M2/M3)
│   │   └── Intel/    ← Mac Intel
│   ├── Windows/
│   └── Linux/
├── .vscode/
│   ├── settings.json
│   ├── tasks.json
│   └── launch.json
├── CMakeLists.txt
├── CMakeUserPresets.json
├── configure-platform.py
└── README.md
```

Build directories are separated by platform and architecture to avoid mixing files when switching between Mac Intel and Apple Silicon, or between different operating systems.

## Usage

### Building

1. Open the project in Cursor

2. Select the CMake kit when prompted (the project is auto-configured for your platform and, on macOS, for your processor architecture—Intel or Apple Silicon)

3. Build the project:
   - Use the command palette: `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS) → "CMake: Build"
   - Or use the terminal:
   
   ```bash
   # macOS Apple Silicon
   cmake --preset default-macos-arm64
   cmake --build --preset default-macos-arm64
   
   # macOS Intel
   cmake --preset default-macos-x86_64
   cmake --build --preset default-macos-x86_64
   
   # Windows
   cmake --preset default-windows
   cmake --build --preset default-windows
   
   # Linux
   cmake --preset default-linux
   cmake --build --preset default-linux
   ```

### Testing Plugins

#### macOS

- **AU**: Copy `.component` to `~/Library/Audio/Plug-Ins/Components/`
- **VST3**: Copy `.vst3` to `~/Library/Audio/Plug-Ins/VST3/`
- **Standalone**: Run the `.app` directly

#### Windows

- **VST3**: Automatically copied to your custom folder (configured in `project-config.cmake`)
  - Configure your DAW to scan this folder
  - Or manually copy to `C:\Program Files\Common Files\VST3\` (requires admin)
- **Standalone**: Run the `.exe` directly

#### Linux

- **VST3**: Automatically copied to your custom folder (configured in `project-config.cmake`, e.g. `/home/username/Plugins/VST3`)
  - Configure your DAW to scan this folder
- **Standalone**: Run the binary from the build directory

### Debugging

Press `F5` in Cursor to start debugging. Debug configurations are available for:

- Standalone application
- Plugin in DAW (Logic Pro, Reaper, Ableton Live)

## Platform Switching

If you open a project on a different platform than where it was generated (or on a different Mac architecture—Intel vs Apple Silicon):

```bash
python configure-platform.py
```

This script automatically detects your operating system and, on macOS, your processor architecture (Intel or Apple Silicon). It updates:

- `.vscode/settings.json` (CMake build directory and preset)
- `.vscode/launch.json` (debug executable paths)
- `.vscode/tasks.json` (build paths)

You can also manually select the appropriate CMake preset: `Ctrl+Shift+P` → "CMake: Select Configure Preset" → Choose the preset for your platform (e.g., `default-macos-arm64`, `default-macos-x86_64`, `default-windows`, `default-linux`).

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
3. On each machine: ensure `JUCE_DIR` is set (see above), then run `python configure-platform.py` to adapt `.vscode/settings.json`, `tasks.json`, and `launch.json` to the current OS.
4. **Build** on each machine; no path edits are needed in the project.

This keeps the repository clean and portable for collaboration and multi-OS development.

## Customization

### Plugin Copy Configuration

Projects support two types of plugin copy after build:

1. **System folders** (macOS): AU → `~/Library/Audio/Plug-Ins/Components/`, VST3 → `~/Library/Audio/Plug-Ins/VST3/`
   - Controlled by `COPY_TO_SYSTEM_FOLDERS` in `project-config.cmake`

2. **Custom folders**: VST3 (all platforms) and AU (macOS)
   - Set paths in `project-config.cmake`; use `""` to disable for a given platform

Edit `project-config.cmake` in any generated project to customize without modifying `CMakeLists.txt`.

## Path Restrictions

### ⚠️ IMPORTANT: No Accented Characters in Paths

**The generator STRICTLY prohibits accented characters and special Unicode characters in all paths.**

This includes:

- Project destination paths (`DEFAULT_PROJECT_DESTINATION`)
- VST3 folder paths in `project-config.cmake` (`CUSTOM_VST3_FOLDER_WINDOWS`, `CUSTOM_VST3_FOLDER_MACOS`, `CUSTOM_VST3_FOLDER_LINUX`)
- AU folder path in `project-config.cmake` (`CUSTOM_AU_FOLDER_MACOS`)
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
- You must fix the path in `generator-config.py` or `project-config.cmake` (or enter a valid path during interactive prompts) before the generator will proceed

## Troubleshooting

### Generator uses default values even after creating config files

- Make sure `generator-config.py` is in the same directory as `generate-new-juce-project.py`
- Make sure `project-config.cmake` is in the generator directory for plugin copy defaults
- Check for syntax errors in `generator-config.py` (Python syntax) - the generator will display a warning if there are errors
- Verify that constant names match exactly (case-sensitive)
- If you see a warning about invalid codes, check that:
  - `DEFAULT_MANUFACTURER_CODE` is exactly 4 alphabetic characters
  - `DEFAULT_PLUGIN_CODE` is exactly 4 alphanumeric characters

### What happens if `generator-config.py` has errors?

The generator is designed to be resilient and will handle various error scenarios:

1. **Syntax errors in `generator-config.py`**:
   
   - The generator will display a warning message showing the error
   - Default values will be used instead
   - Project generation will continue normally

2. **Invalid manufacturer/plugin codes**:
   
   - If codes don't match the required format (4 characters), a warning is displayed
   - Default values are used instead
   - You can still override them during interactive prompts

3. **Invalid or missing JUCE path**:
   
   - If the path doesn't exist in `generator-config.py`, a warning is displayed
   - Project generation continues; for building, set the `JUCE_DIR` environment variable on each machine: `export JUCE_DIR=/path/to/JUCE` (see [Portable workflow](#portable-workflow-github-multi-machine))

4. **Missing constants**:
   
   - If a constant is not defined, the corresponding default value is used
   - No error is displayed (this is expected behavior)

### VST3/AU plugin not copying to custom folder

- The generator automatically normalizes paths (converts backslashes to forward slashes), so you can use either format in `generator-config.py` or `project-config.cmake`
- Ensure the folder path doesn't require admin privileges (unless that's intentional)
- Verify the path is set (not `""`) in `project-config.cmake` for the platform you're building on
- For system folder copy on macOS, ensure `COPY_TO_SYSTEM_FOLDERS` is `ON` in `project-config.cmake`

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

1. Include `generator-config.py` and `project-config.cmake` with generic example values (as shown in the Configuration section)
2. Document that users should customize these files for their environment
3. Include this README.md in your distribution

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]
