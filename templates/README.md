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
- JUCE 8 installed (set `JUCE_DIR` environment variable to your JUCE installation path, e.g., `/Applications/JUCE`)

#### Windows

- Windows 11 or later
- Cursor 2
- CMake 3.22+ (add to system PATH during installation)
- Visual Studio 2022 with "Desktop development with C++" workload
- JUCE 8 installed (set `JUCE_DIR` environment variable to your JUCE installation path, e.g., `C:\JUCE`)

### Environment Setup

Set the `JUCE_DIR` environment variable to point to your JUCE installation:

**macOS:**

```bash
export JUCE_DIR=/Applications/JUCE
```

**Windows:**

```powershell
# System environment variable (recommended)
# Set via: System Properties → Environment Variables → System variables
# Name: JUCE_DIR
# Value: C:\JUCE
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

- **AU**: Copy `.component` file to `~/Library/Audio/Plug-Ins/Components/`
- **VST3**: Copy `.vst3` bundle to `~/Library/Audio/Plug-Ins/VST3/`
- **Standalone**: Run the `.app` directly

#### Windows

- **VST3**: Copy `.vst3` folder to `C:\Program Files\Common Files\VST3\`
- **Standalone**: Run the `.exe` directly

### Debugging

Debug configurations are available in `.vscode/launch.json`:

- **macOS**: Standalone, AU in Logic Pro, VST3 in Reaper, AU in Ableton Live
- **Windows**: Standalone, VST3 in Reaper

Press `F5` in Cursor to start debugging. The debugger will automatically use the correct build directory (`Builds/macOS/ARM`, `Builds/macOS/Intel`, `Builds/Windows`, or `Builds/Linux`) based on your platform.

### Cross-Platform Configuration

The project generator automatically configures `.vscode/settings.json` for the platform where it's run. If you need to switch platforms:

- **Automatic**: Run `python configure-platform.py` from the project root (detects OS and Mac architecture automatically)
- **Manual**: Select the appropriate CMake preset in Cursor (CMake Tools will handle the rest)
