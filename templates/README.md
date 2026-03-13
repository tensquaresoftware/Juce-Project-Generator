# {projectDisplayName}

Version: {projectVersion}  
Manufacturer: {manufacturerName}  
Formats: {pluginFormats}

## Build Instructions

### Prerequisites

#### macOS

- macOS Tahoe or later
- Cursor 2
- CMake 3.22+
- Ninja build system
- JUCE 8 installed at `/Applications/JUCE` (or set `JUCE_DIR` if elsewhere)

#### Windows

- Windows 11 or later
- Cursor 2
- CMake 3.22+ (add to system PATH during installation)
- Visual Studio 2022 with "Desktop development with C++" workload
- JUCE 8 installed at `C:\Program Files\JUCE` (or set `JUCE_DIR` if elsewhere)

### Environment Setup

JUCE is auto-detected at standard locations (`/Applications/JUCE` on macOS, `C:/Program Files/JUCE` on Windows, `/usr/local/JUCE` on Linux). If installed elsewhere, set `JUCE_DIR`:

**macOS:**

```bash
export JUCE_DIR=/path/to/JUCE
```

**Windows:**

```powershell
# System environment variable: JUCE_DIR = C:\path\to\JUCE
```

### Build

**Important:** Build directories are separated by platform and architecture (`Builds/macOS/ARM`, `Builds/macOS/Intel`, `Builds/Windows`, `Builds/Linux`) to avoid mixing files when switching between Mac Intel and Apple Silicon.

#### macOS (Apple Silicon)

```bash
# Configure (using Ninja)
cmake -B Builds/macOS/ARM -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_OSX_ARCHITECTURES=arm64

# Build all formats
cmake --build Builds/macOS/ARM --config Debug

# Or build specific format
cmake --build Builds/macOS/ARM --target {projectName}_Standalone --config Debug
cmake --build Builds/macOS/ARM --target {projectName}_AU --config Debug
cmake --build Builds/macOS/ARM --target {projectName}_VST3 --config Debug
```

#### macOS (Intel)

```bash
# Configure (using Ninja)
cmake -B Builds/macOS/Intel -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_OSX_ARCHITECTURES=x86_64

# Build all formats
cmake --build Builds/macOS/Intel --config Debug

# Or build specific format
cmake --build Builds/macOS/Intel --target {projectName}_Standalone --config Debug
cmake --build Builds/macOS/Intel --target {projectName}_AU --config Debug
cmake --build Builds/macOS/Intel --target {projectName}_VST3 --config Debug
```

#### Windows

```powershell
# Configure (using Visual Studio 2022)
cmake -B Builds/Windows -G "Visual Studio 17 2022" -DCMAKE_BUILD_TYPE=Debug

# Build all formats
cmake --build Builds/Windows --config Debug

# Or build specific format
cmake --build Builds/Windows --target {projectName}_Standalone --config Debug
cmake --build Builds/Windows --target {projectName}_VST3 --config Debug
```

**Note:** Audio Unit (AU) format is only available on macOS. On Windows, only VST3 and Standalone formats are built.

### Using Cursor IDE

The project is **automatically configured** for your platform when generated. Simply:

1. Open the project folder in Cursor
2. CMake Tools extension will automatically detect the project and use the correct preset
3. Select your build kit when prompted (CMake Tools will suggest the correct one):
   - **macOS Apple Silicon**: Ninja generator, preset `default-macos-arm64`
   - **macOS Intel**: Ninja generator, preset `default-macos-x86_64`
   - **Windows**: Visual Studio 2022 generator
4. Build the project:
   - Use the command palette: `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS) → "CMake: Build"
   - Or use tasks: `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS) → "Tasks: Run Task" → Select "Build: All"
   - **Note**: "Build: AU" task is only available on macOS

**If you open the project on a different platform** than where it was generated:
- Run the configuration script: `python configure-platform.py` (or `python3 configure-platform.py` on macOS)
- Or manually select the CMake preset: `Ctrl+Shift+P` → "CMake: Select Configure Preset" → Choose the appropriate preset

### Plugin Installation

#### macOS

- **AU**: Copied automatically to `~/Library/Audio/Plug-Ins/Components/` if `COPY_TO_SYSTEM_FOLDERS` is ON in `project-config.cmake`; or to a custom folder if `CUSTOM_AU_FOLDER_MACOS` is set
- **VST3**: Copied automatically to `~/Library/Audio/Plug-Ins/VST3/` if `COPY_TO_SYSTEM_FOLDERS` is ON; or to a custom folder if `CUSTOM_VST3_FOLDER_MACOS` is set
- **Standalone**: Run the `.app` directly

#### Windows

- **VST3**: Copied automatically to the folder set in `CUSTOM_VST3_FOLDER_WINDOWS` (in `project-config.cmake`), or copy manually to `C:\Program Files\Common Files\VST3\`
- **Standalone**: Run the `.exe` directly

#### Linux

- **VST3**: Copied automatically to the folder set in `CUSTOM_VST3_FOLDER_LINUX` (in `project-config.cmake`)
- **Standalone**: Run the binary from the build directory

### Plugin Copy Configuration

Edit the **USER OPTIONS** section in `project-config.cmake` to customize where plugins are copied:

- **`USER_COPY_TO_SYSTEM_FOLDERS`**: `ON`/`OFF` — copy AU and VST3 to system folders on macOS
- **`USER_CUSTOM_VST3_FOLDER_*`**, **`USER_CUSTOM_AU_FOLDER_MACOS`**: `"path"` or `NONE`

### Debugging

Debug configurations are available in `.vscode/launch.json`:

- **macOS**: Standalone, AU in Logic Pro, VST3 in Reaper, AU in Ableton Live
- **Windows**: Standalone, VST3 in Reaper

Press `F5` in Cursor to start debugging. The debugger will automatically use the correct build directory (`Builds/macOS/ARM`, `Builds/macOS/Intel`, `Builds/Windows`, or `Builds/Linux`) based on your platform.

### Cross-Platform Configuration

The project generator automatically configures `.vscode/settings.json` for the platform where it's run. If you need to switch platforms:

- **Automatic**: Run `python configure-platform.py` from the project root (detects OS and Mac architecture automatically)
- **Manual**: Select the appropriate CMake preset in Cursor (CMake Tools will handle the rest)
