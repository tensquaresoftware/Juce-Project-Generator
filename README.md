# JUCE Project Generator for CMake + Cursor

A Python-based project generator that creates complete JUCE plugin projects with CMake build system, optimized for development in Cursor (or VS Code).

---

**Author:** Guillaume DUPONT  
**Organization:** Ten Square Software  
**Revision date:** 2026-03-21

---

## Features

- ✅ Complete JUCE plugin project structure
- ✅ CMake build system configuration
- ✅ Platform-specific settings (Windows, macOS Apple Silicon/Intel/Intel-Rosetta/Universal Binary, Linux)
- ✅ Cross-platform path normalization (automatic handling of Windows/macOS/Linux path differences)
- ✅ **Cursor / VS Code:** `.vscode/extensions.json` (CMake Tools + C/C++; clangd listed as unwanted), tasks, launch, settings; **`cmake.environment`** for `JUCE_DIR`; **`cmake.copyCompileCommands`** to the workspace root; narrowed **`cmake.enabledOutputParsers`** (no generic `cmake` parser); build **tasks** use empty `problemMatcher`s—reduces duplicate diagnostics and false “Task has errors” when post-build copy steps print harmless lines
- ✅ **C++ IntelliSense:** `CMAKE_EXPORT_COMPILE_COMMANDS`, then **CMake Tools + Microsoft C/C++** with **clangd** off by default so JUCE includes resolve without spurious red squiggles after configure
- ✅ **Smart build artefact management:**
  - **System folders**: copies plugins to standard locations where DAWs scan:
    - **Windows**: `C:\Program Files\Common Files\VST3\` (UAC prompt at build time; click Yes to copy).
    - **macOS**: `~/Library/Audio/Plug-Ins/Components/` (AU), `~/Library/Audio/Plug-Ins/VST3/` (VST3).
    - **Linux**: `~/.vst3/` (VST3)
  - **Central custom folder**: one organized location for all your projects' plugins (paths per OS, configured once in `generator-configuration.py`, injected at generation)
- ✅ Support for AU, VST3, and Standalone formats (CLAP format support planned for the upcoming release of JUCE 9)
- ✅ Configurable via `generator-configuration.py` and `project-configuration.cmake` for easy customization
- ✅ Customizable default manufacturer and plugin codes
- ✅ **Portable workflow**: projects resolve `JUCE_DIR` from the environment (recommended) or common install locations; no per-user paths injected at generation—ideal for GitHub and multi-machine (Windows / macOS / Linux) development

**Generator entry point:** `generate-new-juce-project.py` in the repository root (see **Quick Start** §4).

## Prerequisites

### All platforms

- Python 3.7+
- JUCE 8 installed
- CMake 3.22+ (3.27+ recommended)
- **Cursor** or **VS Code** with the **CMake Tools** extension (and C/C++ debugging support where you use **F5**)

### Windows

- Visual Studio 2022 with "Desktop development with C++" workload
- CMake (add to PATH during installation)

### macOS

- Xcode Command Line Tools
- Ninja: `brew install ninja`

### Linux

- Ninja, GCC, GDB, and build tools (example for Debian/Ubuntu: `sudo apt install ninja-build build-essential gdb`)
- Other distributions: install the equivalent packages with your package manager

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

Generated projects use `${env:JUCE_DIR}` everywhere. Configure it once per machine so the same project builds on Windows, macOS, and Linux without any machine-specific paths in Git.

**Windows** (System Environment Variables or PowerShell):

```powershell
# Example 1:
setx JUCE_DIR "C:\JUCE"

# Example 2:
setx JUCE_DIR "C:\Dev\JUCE"

# Example 3:
setx JUCE_DIR "D:\Guillaume\Dev\SDKs\JUCE"
```

**macOS** (add to `~/.zshrc` or `~/.bash_profile`):

```bash
# Example 1:
export JUCE_DIR="~/JUCE"

# Example 2:
export JUCE_DIR="/Applications/JUCE"

# Example 3:
export JUCE_DIR="/Volumes/Guillaume/Dev/SDKs/JUCE"
```

**Linux** (add to `~/.bashrc`):

```bash
# Example 1:
export JUCE_DIR="~/JUCE"

# Example 2:
export JUCE_DIR="/usr/local/JUCE"

# Example 3:
export JUCE_DIR="/opt/JUCE"
```

**Tilde in `JUCE_DIR`:** Prefer an absolute path (e.g. `/Applications/JUCE`). A value like `~/JUCE` is not always expanded when tools read the environment outside a login shell.

**After setting the environment variable:** Restart Cursor or VS Code (or at least the integrated terminal).

### 3. Configure the generator (optional)

Edit `generator-configuration.py` to customize:

- Default manufacturer information
- Central artefacts folder paths (per OS)
- Default project destination (per OS)
- JUCE installation paths for validation (optional)

The generator works out-of-the-box with default values if you skip this step.

### 4. Generate your first project

**In Cursor or VS Code:**

1. Open the generator folder (`Cmd+O` / `Ctrl+O`)
2. Open integrated terminal (`Cmd+J` / `Ctrl+J`)
3. Run: `python3 generate-new-juce-project.py` (or `./generate-new-juce-project.py` on Linux/macOS, or `python` on Windows)
4. Follow the interactive prompts
5. Open the generated project: `cursor .` in the project folder

**From terminal:**

```bash
python3 generate-new-juce-project.py   # or ./generate-new-juce-project.py on Linux/macOS
# Follow prompts
cd YourProject
cursor .  # or 'code .' for VS Code
```

**From the file manager (double-click):** On **macOS**, if **Python Launcher** is installed (included with the [python.org macOS installer](https://www.python.org/downloads/macos/)), you can **double-click `generate-new-juce-project.py`** in Finder, answer the prompts in the Terminal window, then open the new project in Cursor or VS Code. On **Windows** and **Linux**, there is no Python Launcher app; double-click behaviour varies—see [Usage → Option C](#option-c-double-click-from-the-file-manager).

### 5. Build your project

**In Cursor or VS Code** (with **CMake Tools**):

1. When prompted, select a **CMake preset** that matches your system
2. Build: press **F7** (default CMake Tools shortcut; yours may differ if remapped) or `Cmd+Shift+P` / `Ctrl+Shift+P` → **CMake: Build**
3. Build specific target: **Shift+F7** (default) or the equivalent command from the palette

**From terminal:**

```bash
# List available presets
cmake --list-presets

# Configure and build (below is an example for macOS / Apple Silicon)
cmake --preset default-macos-arm64   # or default-windows, default-linux, etc.
cmake --build --preset default-macos-arm64
```

### 6. Test your plugin

After building, plugins are automatically copied according to `project-configuration.cmake` settings:

- `COPY_TO_SYSTEM_FOLDERS=ON`: Plugins go to standard locations where DAWs scan (on Windows, a UAC prompt appears—click Yes to copy to `C:\Program Files\Common Files\VST3\`)
- `COPY_TO_ARTEFACTS_DIR=ON`: Plugins go to your central custom folder

Your DAW will find them after a rescan.

---

## Configuration

The generator uses two configuration files (both included in the repository):

### `generator-configuration.py`

Generator-specific settings (defaults for prompts, paths per OS). Edit this file to customize:

```python
# JUCE installation paths (optional: validation only, not written into projects).
# Use None or "" for any OS to skip validation on that platform.
JUCE_DIR_WINDOWS = "C:/JUCE"
JUCE_DIR_MACOS   = "/Applications/JUCE"
JUCE_DIR_LINUX   = "/usr/local/JUCE"

# Default manufacturer information
DEFAULT_MANUFACTURER_NAME = "My Company"
DEFAULT_MANUFACTURER_CODE = "Myco"        # Must be exactly 4 alphabetic characters
DEFAULT_PLUGIN_CODE       = "Plg1"        # Must be exactly 4 alphanumeric characters

# Default project destination (per OS)
# Use "Desktop" to default to user's Desktop folder
DEFAULT_PROJECT_DIR_WINDOWS = "C:/Users/Guillaume/Dev/SDKs/JUCE/Projects"
DEFAULT_PROJECT_DIR_MACOS   = "/Volumes/Guillaume/Dev/SDKs/JUCE/Projects"
DEFAULT_PROJECT_DIR_LINUX   = "/home/guillaume/Dev/SDKs/JUCE/Projects"

# Central artefacts folder (custom folder for all projects' plugins/Standalone, per OS)
ARTEFACTS_DIR_WINDOWS = "C:/Users/Guillaume/Dev/SDKs/JUCE/Artefacts"
ARTEFACTS_DIR_MACOS   = "/Volumes/Guillaume/Dev/SDKs/JUCE/Artefacts"
ARTEFACTS_DIR_LINUX   = "/home/guillaume/Dev/SDKs/JUCE/Artefacts"
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

The generator can be run from an IDE, from the terminal, or from the file manager where double-click is supported (see **Option C**).

#### Option A: From Cursor or VS Code (recommended for beginners)

1. Open the generator folder in the editor
2. Open integrated terminal (`Cmd+J` / `Ctrl+J`)
3. Run: `python3 generate-new-juce-project.py` (or `./generate-new-juce-project.py` on Linux/macOS)
4. Answer the prompts
5. Open the generated project: `cursor .` in the project folder (or `code .` for VS Code)

#### Option B: From terminal only

```bash
cd /path/to/Juce-Project-Generator
python3 generate-new-juce-project.py
# Follow prompts
cd YourProject
cursor .  # or open manually in IDE
```

#### Option C: Double-click from the file manager

**macOS — Python Launcher**

**Python Launcher** is included with the official [python.org macOS installer](https://www.python.org/downloads/macos/). **Double-click `generate-new-juce-project.py`** in Finder to run it in a Terminal window, answer the prompts, then open the new project in Cursor or VS Code.

**Windows**

There is **no** Python Launcher app (that name is macOS-specific). The [python.org Windows installer](https://www.python.org/downloads/windows/) can **register `.py` files** with the interpreter so that **double-clicking** runs the script in a console window; the working directory is usually the folder that contains the script, which suits this generator. If the window flashes closed or nothing runs, use PowerShell, Command Prompt, or your IDE terminal instead.

**Linux**

There is **no** Python Launcher. Behaviour depends on your desktop and file manager: **double-click often opens `.py` files in a text editor** rather than executing them. Prefer the terminal or your IDE, or use a file-manager action such as **Run in terminal** (if available). Ensure `generate-new-juce-project.py` is executable (`chmod +x`) when your environment expects it.

### Building a generated project

#### In Cursor or VS Code (recommended)

1. Open project folder in the editor
2. Select CMake preset when prompted (matches your OS and architecture)
3. Build: **F7** (or `Cmd+Shift+P` → "CMake: Build")
4. Switch preset: click preset name in status bar

#### From terminal

```bash
# List presets
cmake --list-presets

# Configure with preset (below is an example for macOS / Apple Silicon)
cmake --preset default-macos-arm64

# Build
cmake --build --preset default-macos-arm64

# Or chain them
cmake --preset default-macos-arm64 && cmake --build --preset default-macos-arm64
```

**Available presets** (per platform):

- **Windows**: `default-windows`
- **macOS**: `default-macos-arm64`, `default-macos-x86_64-rosetta`, `default-macos-x86_64`, `default-macos-universal`
- **Linux**: `default-linux`

---

## Testing & Debugging

### Testing plugins in your DAW

After building, plugins are automatically copied according to `project-configuration.cmake` settings:

**System folders** (`COPY_TO_SYSTEM_FOLDERS=ON`):

- **Windows**: VST3 is copied to `C:\Program Files\Common Files\VST3\` (the folder where Ableton Live and most DAWs look by default). **At each build, Windows shows a UAC prompt** (“Do you want to allow this app to make changes?”). **Click Yes** to allow the copy; the plugin is then installed in the system folder. If you click No, the build still completes but the plugin is not copied (you can copy it manually or rebuild and accept UAC).
- **macOS**: `~/Library/Audio/Plug-Ins/Components/` (AU), `~/Library/Audio/Plug-Ins/VST3/` (VST3)
- **Linux**: `~/.vst3/`

Your DAW will find them automatically after a rescan.

**Central custom folder** (`COPY_TO_ARTEFACTS_DIR=ON`):

- Plugins go to paths configured in `generator-configuration.py`
- Add this folder to your DAW's plugin search path if needed

### Debugging

With **CMake Tools** and the **C/C++** extension (or equivalent debugger support), press **F5** to start debugging. Build output paths follow the active CMake preset (via `cmake.buildDirectory`).

**Launch configurations (`launch.json`, generated project):**

- **macOS**: Standalone; AU in Logic Pro or Ableton Live; VST3 in Reaper (DAW paths are fixed in `launch.json`—adjust if your apps live elsewhere).
- **Windows**: Standalone; VST3 in Reaper (default path targets `C:\Program Files\REAPER (x64)\reaper.exe`—edit `launch.json` if your install differs).
- **Linux**: **Standalone** uses **GDB** (`cppdbg`) in the generated `launch.json`. DAW-hosted debug is not preset-specific in the template; add or edit launch entries for your DAW path if needed.

**JUCE Audio Plugin Host (`AudioPluginHost`):** The official JUCE tree includes a minimal host in [`extras/AudioPluginHost`](https://github.com/juce-framework/JUCE/tree/master/extras/AudioPluginHost). Build it with **CMake** or **Projucer** on **macOS, Windows, and Linux** to **load, test, and debug** AU, VST3, and other supported formats without a full DAW—handy next to the **Standalone** target and the DAW attach configurations above. It is compiled from your **JUCE installation**, not from the generated plugin project.

---

## Platform Switching

### Portable workflow (GitHub / multi-machine)

Generated projects pass `JUCE_DIR` from the environment into CMake (see `.vscode/settings.json`). The `CMakeLists.txt` also falls back to common install paths when `JUCE_DIR` is unset—set the variable explicitly on each machine for predictable CI and team builds.

**Setup per machine:**


| Platform    | Where to set    | Example                                |
| ----------- | --------------- | -------------------------------------- |
| **Windows** | System env vars | `setx JUCE_DIR "C:\Path\To\JUCE"`      |
| **macOS**   | `~/.zshrc`      | `export JUCE_DIR="/Applications/JUCE"` |
| **Linux**   | `~/.bashrc`     | `export JUCE_DIR="/usr/local/JUCE"`    |


**Workflow:**

1. Create project on any machine → push to GitHub
2. Clone on other machines
3. Set `JUCE_DIR` on each machine
4. Open in Cursor or VS Code → select appropriate preset → build

### macOS preset validation

CMake validates the build directory against the host architecture where checks apply:

- **On Apple Silicon**: configuring under `Builds/macOS/Intel` (without `Intel-Rosetta`) is rejected—use **Intel-Rosetta** for x86_64 or **ARM** for native arm64.
- **On Mac Intel**: configuring under `Builds/macOS/Intel-Rosetta` or `Builds/macOS/ARM` is rejected—use **Intel** for native x86_64.

Errors are explicit with instructions to use `cmake --list-presets`. Other mismatches (e.g. Universal preset on an unusual setup) may still fail later at compile or link time.

---

## Generated Project Structure

```
YourProject/
├── project-configuration.cmake ← Build artefact copy settings (edit to customize)
├── Source/
│   ├── PluginProcessor.h
│   ├── PluginProcessor.cpp
│   ├── PluginEditor.h
│   └── PluginEditor.cpp
├── Builds/
│   ├── Windows/
│   ├── macOS/
│   │   ├── ARM/           ← Apple Silicon native
│   │   ├── Intel/         ← Mac Intel native
│   │   ├── Intel-Rosetta/ ← x86_64 on Apple Silicon
│   │   └── Universal/     ← Universal Binary (distribution)
│   └── Linux/
├── .cursorrules        ← optional Cursor AI rules (ignored by VS Code)
├── .vscode/
│   ├── settings.json
│   ├── tasks.json
│   ├── launch.json
│   └── extensions.json   ← recommended extensions (CMake Tools, C/C++)
├── compile_commands.json   ← optional copy at workspace root after configure (gitignored; CMake Tools)
├── CMake/
│   └── CopyVst3Elevated.ps1   ← Windows: used for UAC-elevated copy to Program Files
├── CMakeLists.txt
├── CMakeUserPresets.json
└── README.md
```

Build directories are separated by platform and architecture to avoid mixing files when switching configurations.

---

## Troubleshooting

### Red squiggles on `Templates/CMakeLists.txt` in Cursor / VS Code

That file is a **Python template** (`{{…}}`, `{projectName}`, etc.), not a CMake project until you run the generator. The repo **`.vscode/settings.json`** disables CMake configure-on-open and treats `Templates/CMakeLists.txt` as **Plain Text** so CMake Tools does not validate it. Do **not** set `cmake.sourceDirectory` to `Templates/`. To work with CMake, open a **generated** plugin folder.

### “Task has errors” or a red CMake indicator after a successful build

If **CMake Tools** reports **Task has errors** but the build actually finished (plugins produced, exit code 0), it is often a **false positive** from output parsing (for example `cmake -E echo` lines in post-build copy steps). Generated projects omit the generic **`cmake`** parser from **`cmake.enabledOutputParsers`** and avoid duplicate **problem matchers** on shell build tasks. If you still see it, check the **CMake** and **Build** output channels for a real `error:` / `FAILED:` line; otherwise reload the window after a clean configure.

### Generator uses default values

- Make sure `generator-configuration.py` is in the generator directory
- Check for syntax errors in the file (warnings are displayed if errors occur)
- Verify constant names match exactly (case-sensitive)

### JUCE not found

CMake reports `JUCE not found. Set JUCE_DIR...` when `JUCE_DIR` is not set or not visible.

1. Set the environment variable (see Setup section above)
2. Restart Cursor or VS Code (or the terminal)
3. On Linux: ensure Ninja is installed (`sudo apt install ninja-build`)

### Build errors with accented characters

If you see errors like `MSB8066` or malformed characters:

- Check that your project path doesn't contain accented characters
- The generator validates paths at creation, but if you manually moved the project, regenerate it in a valid location

### Plugins not copying after build

- Ensure `COPY_TO_ARTEFACTS_DIR` or `COPY_TO_SYSTEM_FOLDERS` is `ON` in `project-configuration.cmake`
- Check CMake output for copy status messages
- **Windows (system folder)**: If the VST3 does not appear in `C:\Program Files\Common Files\VST3\`, the UAC prompt may have been cancelled. Rebuild and click **Yes** when Windows asks to allow the app to make changes. The build does not fail if you click No—the plugin is simply not copied to the system folder.

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
3. Test your changes on all supported platforms if possible (Windows, macOS, Linux)
4. Commit your changes following the project's commit message style (see git log)
5. Push to your fork and submit a pull request

Thank you for contributing!