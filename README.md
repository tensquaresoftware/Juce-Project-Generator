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
- ✅ Cross-platform path normalization (automatic handling of Windows/macOS/Linux path differences)
- ✅ Cursor/VS Code integration (tasks, launch configs, settings)
- ✅ **Smart build artefact management:**
  - **System folders**: copies plugins where DAWs look by default (macOS: `~/Library/Audio/Plug-Ins/`, Windows: `%LOCALAPPDATA%\Programs\Common\VST3\`, Linux: `~/.vst3/`)
  - **Central custom folder**: one organized location for all your projects' plugins (paths per OS, configured once in `generator-configuration.py`, injected at generation)
- ✅ Support for AU, VST3, and Standalone formats (CLAP support planned for future)
- ✅ Configurable via `generator-configuration.py` and `project-configuration.cmake` for easy customization
- ✅ Customizable default manufacturer and plugin codes
- ✅ **Portable workflow**: projects use `JUCE_DIR` from the environment—no machine-specific paths in Git; ideal for GitHub and multi-machine (macOS / Windows / Linux) development

## Prerequisites

### All platforms

- Python 3.7+
- JUCE 8 installed
- CMake 3.22+ (3.27+ recommended)
- Cursor or VS Code

### macOS

- Xcode Command Line Tools
- Ninja: `brew install ninja`

### Windows

- Visual Studio 2022 with "Desktop development with C++" workload
- CMake (add to PATH during installation)

### Linux

- Ninja: `sudo apt install ninja-build`
- GCC, GDB, build-essential: `sudo apt install build-essential gdb`

---

## Quick Start

### 1. Get the repository

**Option A: Clone with Git** (recommended for updates)

```bash
git clone https://github.com/tensquaresoftware/Juce-Project-Generator.git
cd Juce-Project-Generator
```

**Option B: Download ZIP** (simpler for beginners)

1. Visit [https://github.com/tensquaresoftware/Juce-Project-Generator](https://github.com/tensquaresoftware/Juce-Project-Generator)
2. Click the green **Code** button
3. Select **Download ZIP**
4. Extract the ZIP file to your desired location

### 2. Set `JUCE_DIR` environment variable

Generated projects use `${env:JUCE_DIR}` everywhere. Configure it once per machine so the same project builds on macOS, Windows, and Linux without any machine-specific paths in Git.

**macOS** (add to `~/.zshrc` or `~/.bash_profile`):

```bash
# Example 1:
export JUCE_DIR="/Applications/JUCE"

# Example 2:
export JUCE_DIR="~/JUCE"
```

**Windows** (System Environment Variables or PowerShell):

```powershell
# Example 1:
setx JUCE_DIR "C:\JUCE"

# Example 2:
setx JUCE_DIR "C:\Dev\JUCE"
```

**Linux** (add to `~/.bashrc`):

```bash
# Example 1:
export JUCE_DIR="~/JUCE"

# Example 2:
export JUCE_DIR="/opt/JUCE"
```

**After setting the environment variable:** Restart Cursor (or at least the integrated terminal).

### 3. Configure the generator (optional)

Edit `generator-configuration.py` to customize:
- Default manufacturer information
- Central artefacts folder paths (per OS)
- Default project destination (per OS)
- JUCE installation paths for validation (optional)

The generator works out-of-the-box with default values if you skip this step.

### 4. Generate your first project

**In Cursor IDE:**

1. Open the generator folder in Cursor (`Cmd+O` / `Ctrl+O`)
2. Open integrated terminal (`Cmd+J` / `Ctrl+J`)
3. Run: `python3 generate-new-project.py` (or `python` on Windows)
4. Follow the interactive prompts
5. Open the generated project: `cursor .` in the project folder

**From terminal:**

```bash
python3 generate-new-project.py
# Follow prompts
cd YourProject
cursor .  # or 'code .' for VS Code
```

### 5. Build your project

**In Cursor:**

1. Cursor asks you to select a **CMake preset** → choose one matching your system
2. Build: press **F7** (or `Cmd+Shift+P` → "CMake: Build")
3. Build specific target: press **Shift+F7**

**From terminal:**

```bash
# List available presets
cmake --list-presets

# Configure and build
cmake --preset default-macos-arm64    # or default-windows, default-linux, etc.
cmake --build --preset default-macos-arm64
```

### 6. Test your plugin

After building, plugins are automatically copied according to `project-configuration.cmake` settings:

- **`COPY_TO_SYSTEM_FOLDERS=ON`**: Plugins go to system folders where DAWs scan automatically
- **`COPY_TO_ARTEFACTS_DIR=ON`**: Plugins go to your central custom folder

Your DAW will find them after a rescan.

---

## Configuration

The generator uses two configuration files (both included in the repository):

### `generator-configuration.py`

Generator-specific settings (defaults for prompts, paths per OS). Edit this file to customize:

```python
# JUCE installation paths (optional: validation only, not written into projects)
JUCE_DIR_MACOS = "/Applications/JUCE"
JUCE_DIR_WINDOWS = "C:/JUCE"
JUCE_DIR_LINUX = "/home/username/JUCE"  # or None to skip validation

# Default manufacturer information
DEFAULT_MANUFACTURER_NAME = "My Company"
DEFAULT_MANUFACTURER_CODE = "Myco"  # Must be exactly 4 alphabetic characters
DEFAULT_PLUGIN_CODE = "Plg1"        # Must be exactly 4 alphanumeric characters

# Central artefacts folder (custom folder for all projects' plugins/Standalone, per OS)
ARTEFACTS_DIR_WINDOWS = "C:/Users/Guillaume/Dev/JUCE/Artefacts"
ARTEFACTS_DIR_MACOS   = "/Volumes/Guillaume/Dev/JUCE/Artefacts"
ARTEFACTS_DIR_LINUX   = "/home/guillaume/Dev/JUCE/Artefacts"

# Default project destination (per OS)
DEFAULT_PROJECT_DIR_WINDOWS = "C:/Users/Guillaume/Dev/JUCE/Projects"
DEFAULT_PROJECT_DIR_MACOS   = "/Volumes/Guillaume/Dev/JUCE/Projects"
DEFAULT_PROJECT_DIR_LINUX   = "/home/guillaume/Dev/JUCE/Projects"
# Use "Desktop" to default to user's Desktop folder
```

**Path restrictions**: Paths must NOT contain accented characters (é, à, è, ç, etc.) or special Unicode characters. Only ASCII (0-127) is allowed due to CMake/Visual Studio compatibility issues on Windows.

### `project-configuration.cmake`

Build artefact copy settings used as defaults when creating new projects. Each generated project gets its own copy that you can edit afterward.

Edit the **USER OPTIONS** section:

```cmake
# USER OPTIONS - Edit these values only
set(USER_COPY_TO_SYSTEM_FOLDERS ON)   # Copy to system folders (all OS)
set(USER_COPY_TO_ARTEFACTS_DIR ON)    # Copy to central custom folder

# CODE - Do not edit below
set(COPY_TO_SYSTEM_FOLDERS ${USER_COPY_TO_SYSTEM_FOLDERS} CACHE BOOL "...")
set(COPY_TO_ARTEFACTS_DIR ${USER_COPY_TO_ARTEFACTS_DIR} CACHE BOOL "...")
# Central artefacts directories (injected at generation)
set(ARTEFACTS_DIR_WINDOWS "...")
set(ARTEFACTS_DIR_MACOS   "...")
set(ARTEFACTS_DIR_LINUX   "...")
```

---

## Usage

### Using the generator

The generator can be run from an IDE or from the terminal.

#### Option A: From Cursor (recommended for beginners)

1. Open the generator folder in Cursor
2. Open integrated terminal (`Cmd+J` / `Ctrl+J`)
3. Run: `python3 generate-new-project.py`
4. Answer the prompts
5. Open the generated project: `cursor .` in the project folder

#### Option B: From terminal only

```bash
cd /path/to/Juce-Project-Generator
python3 generate-new-project.py
# Follow prompts
cd YourProject
cursor .  # or open manually in IDE
```

### Building a generated project

#### In Cursor (recommended)

1. Open project folder in Cursor
2. Select CMake preset when prompted (matches your OS and architecture)
3. Build: **F7** (or `Cmd+Shift+P` → "CMake: Build")
4. Switch preset: click preset name in status bar

#### From terminal

```bash
# List presets
cmake --list-presets

# Configure with preset
cmake --preset default-macos-arm64

# Build
cmake --build --preset default-macos-arm64

# Or chain them
cmake --preset default-macos-arm64 && cmake --build --preset default-macos-arm64
```

**Available presets** (per platform):
- **macOS**: `default-macos-arm64`, `default-macos-x86_64-rosetta`, `default-macos-x86_64`, `default-macos-universal`
- **Windows**: `default-windows`
- **Linux**: `default-linux`

---

## Testing & Debugging

### Testing plugins in your DAW

After building, plugins are automatically copied according to `project-configuration.cmake` settings:

**System folders** (`COPY_TO_SYSTEM_FOLDERS=ON`):
- **macOS**: `~/Library/Audio/Plug-Ins/Components/` (AU), `~/Library/Audio/Plug-Ins/VST3/` (VST3)
- **Windows**: `%LOCALAPPDATA%\Programs\Common\VST3\`
- **Linux**: `~/.vst3/`

Your DAW will find them automatically after a rescan.

**Central custom folder** (`COPY_TO_ARTEFACTS_DIR=ON`):
- Plugins go to paths configured in `generator-configuration.py`
- Add this folder to your DAW's plugin search path if needed

### Debugging

Press **F5** in Cursor to start debugging. Debug configurations available:
- Standalone application
- Plugin in DAW (Logic Pro, Reaper, Ableton Live on macOS)

All paths adapt automatically when you switch presets.

---

## Platform Switching

### Portable workflow (GitHub / multi-machine)

Generated projects use `${env:JUCE_DIR}` everywhere—no machine-specific paths in Git.

**Setup per machine:**

| Platform | Where to set | Example |
|----------|--------------|---------|
| **macOS** | `~/.zshrc` | `export JUCE_DIR="/Applications/JUCE"` |
| **Linux** | `~/.bashrc` | `export JUCE_DIR="/home/username/JUCE"` |
| **Windows** | System env vars | `setx JUCE_DIR "C:\Path\To\JUCE"` |

**Workflow:**
1. Create project on any machine → push to GitHub
2. Clone on other machines
3. Set `JUCE_DIR` on each machine
4. Open in Cursor → select appropriate preset → build

### macOS preset validation

CMake validates presets against host architecture to prevent configuration errors:

- **On Apple Silicon**: Cannot use "macOS Intel" preset (use "Intel-Rosetta" instead for x86_64)
- **On Mac Intel**: Cannot use "macOS Intel-Rosetta" or "Apple Silicon" presets

Errors are explicit with instructions to use `cmake --list-presets`.

---

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
│   │   ├── Intel/         ← Mac Intel native
│   │   ├── Intel-Rosetta/ ← x86_64 on Apple Silicon
│   │   └── Universal/     ← Universal Binary (distribution)
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

Build directories are separated by platform and architecture to avoid mixing files when switching configurations.

---

## Troubleshooting

### Generator uses default values

- Make sure `generator-configuration.py` is in the generator directory
- Check for syntax errors in the file (warnings are displayed if errors occur)
- Verify constant names match exactly (case-sensitive)

### JUCE not found

CMake reports `JUCE not found. Set JUCE_DIR...` when `JUCE_DIR` is not set or not visible.

1. Set the environment variable (see Setup section above)
2. Restart Cursor or the terminal
3. On Linux: ensure Ninja is installed (`sudo apt install ninja-build`)

### Build errors with accented characters

If you see errors like `MSB8066` or malformed characters:

- Check that your project path doesn't contain accented characters
- The generator validates paths at creation, but if you manually moved the project, regenerate it in a valid location

### Plugins not copying after build

- Ensure `COPY_TO_ARTEFACTS_DIR` or `COPY_TO_SYSTEM_FOLDERS` is `ON` in `project-configuration.cmake`
- Check CMake output for copy status messages

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contributing

We welcome contributions! Here's how you can help:

### Reporting bugs

If you encounter a bug, please [open an issue](https://github.com/tensquaresoftware/Juce-Project-Generator/issues) with:

- **Clear title**: Brief description of the problem
- **Environment**: OS (version), Python version, JUCE version, CMake version
- **Steps to reproduce**: Detailed steps to reproduce the issue
- **Expected behavior**: What you expected to happen
- **Actual behavior**: What actually happened
- **Error messages**: Full error output if applicable
- **Generator configuration**: Relevant parts of your `generator-configuration.py` (remove sensitive paths)

### Submitting changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Test your changes on all supported platforms if possible (macOS, Windows, Linux)
4. Commit your changes following the project's commit message style (see git log)
5. Push to your fork and submit a pull request

Thank you for contributing!
