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

**Important:** Build directories are separated by platform and architecture (`Builds/macOS/ARM`, `Builds/macOS/Intel`, `Builds/macOS/Intel-Rosetta`, `Builds/macOS/Universal`, `Builds/Windows`, `Builds/Linux`) to avoid mixing files when switching between Mac Intel and Apple Silicon.

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

#### macOS (Intel) — native on Mac Intel

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

#### macOS (Intel-Rosetta) — x86_64 on Apple Silicon

When building for Intel compatibility on an Apple Silicon Mac, use the Intel-Rosetta preset. Build outputs go to `Artefacts/macOS/Intel-Rosetta/`.

```bash
# Configure (using preset)
cmake --preset default-macos-x86_64-rosetta

# Build all formats
cmake --build --preset default-macos-x86_64-rosetta

# Or manual mode
cmake -B Builds/macOS/Intel-Rosetta -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_OSX_ARCHITECTURES=x86_64
cmake --build Builds/macOS/Intel-Rosetta --config Debug
```

#### macOS (Universal)

For **distribution**, build a Universal Binary (Apple Silicon + Intel in a single `.vst3` / `.component` / `.app`). One file works on both Apple Silicon and Intel Macs. Note: binaries are ~2× larger and builds take longer than single-architecture builds.

```bash
# Configure (using preset)
cmake --preset default-macos-universal

# Build all formats
cmake --build --preset default-macos-universal

# Or manual mode
cmake -B Builds/macOS/Universal -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_OSX_ARCHITECTURES="arm64;x86_64"
cmake --build Builds/macOS/Universal --config Debug

# Or build specific format
cmake --build Builds/macOS/Universal --target {projectName}_Standalone --config Debug
cmake --build Builds/macOS/Universal --target {projectName}_AU --config Debug
cmake --build Builds/macOS/Universal --target {projectName}_VST3 --config Debug
```

To verify the binary contains both architectures: `lipo -archs Builds/macOS/Universal/{projectName}_artefacts/Debug/{projectName}.vst3/Contents/MacOS/{projectName}` (should show `arm64 x86_64`).

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

The project is **automatically configured** for your platform when generated (Apple Silicon or Intel for development). For distribution builds, select the Universal preset manually. Simply:

1. Open the project folder in Cursor
2. CMake Tools extension will automatically detect the project and use the correct preset
3. Select your build kit when prompted (CMake Tools will suggest the correct one):
   - **macOS Apple Silicon**: Ninja generator, preset `default-macos-arm64`
   - **macOS Intel** (native on Mac Intel): Ninja generator, preset `default-macos-x86_64`
   - **macOS Intel-Rosetta** (x86_64 on Apple Silicon): Ninja generator, preset `default-macos-x86_64-rosetta`
   - **macOS Universal** (distribution): Ninja generator, preset `default-macos-universal`
   - **Windows**: Visual Studio 2022 generator
4. Build the project:
   - Use the command palette: `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS) → "CMake: Build"
   - Or use tasks: `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS) → "Tasks: Run Task" → Select "Build: All"
   - **Note**: "Build: AU" task is only available on macOS

**If you open the project on a different platform** than where it was generated:
- Run the configuration script: `python configure-platform.py` (or `python3 configure-platform.py` on macOS). On macOS, an interactive menu lets you choose ARM, Intel, or Universal (Intel on Apple Silicon routes to Intel-Rosetta); use `--arm`, `--intel`, `--intel-rosetta`, or `--universal` to skip the prompt.
- Or manually select the CMake preset: `Ctrl+Shift+P` → "CMake: Select Configure Preset" → Choose the appropriate preset (`default-macos-arm64`, `default-macos-x86_64`, `default-macos-x86_64-rosetta`, `default-macos-universal`, `default-windows`, `default-linux`)

### Build Artefacts

When `COPY_TO_PROJECT_FOLDERS` is ON (default), build outputs (AU, VST3, Standalone) are copied to `Artefacts/{{OS}}/{{arch}}/{{format}}/`:
- **macOS**: `Artefacts/macOS/ARM/`, `Artefacts/macOS/Intel/`, `Artefacts/macOS/Intel-Rosetta/`, or `Artefacts/macOS/Universal/` (depending on build preset and host) — each contains `AU/`, `VST3/`, `Standalone/`. Intel-Rosetta = x86_64 built on Apple Silicon.
- **Windows**: `Artefacts/Windows/VST3/`, `Artefacts/Windows/Standalone/`
- **Linux**: `Artefacts/Linux/VST3/`, `Artefacts/Linux/Standalone/`

Add the appropriate folder to your DAW's plugin search path. Run Standalone directly from its folder.

When `COPY_TO_SYSTEM_FOLDERS` is ON (macOS only), AU and VST3 are copied to `~/Library/Audio/Plug-Ins/` — your DAW will find them automatically.

### Build Artefact Copy Configuration

Edit the **USER OPTIONS** section in `project-config.cmake`:

- **`USER_COPY_TO_SYSTEM_FOLDERS`**: `ON`/`OFF` — copy AU and VST3 to system folders on macOS (`~/Library/Audio/Plug-Ins/`)
- **`USER_COPY_TO_PROJECT_FOLDERS`**: `ON`/`OFF` — copy to project `Artefacts/` folder (organized by platform and architecture). No path to configure.

### Debugging

Debug configurations are available in `.vscode/launch.json`:

- **macOS**: Standalone, AU in Logic Pro, VST3 in Reaper, AU in Ableton Live
- **Windows**: Standalone, VST3 in Reaper

Press `F5` in Cursor to start debugging. The debugger will automatically use the correct build directory (`Builds/macOS/ARM`, `Builds/macOS/Intel`, `Builds/macOS/Intel-Rosetta`, `Builds/Windows`, or `Builds/Linux`) based on your platform.

### Cross-Platform Configuration

The project generator automatically configures `.vscode/settings.json` for the platform where it's run. If you need to switch platforms:

- **Automatic**: Run `python configure-platform.py` from the project root. On macOS, an interactive menu lets you choose ARM, Intel, or Universal (Intel on Apple Silicon → Intel-Rosetta); on Windows/Linux, direct execution.
- **Manual**: Select the appropriate CMake preset in Cursor (CMake Tools will handle the rest)
