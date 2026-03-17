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

**Important:** Build directories are separated by platform and architecture (`Builds/macOS/ARM`, `Builds/macOS/Intel`, `Builds/macOS/Intel-Rosetta`, `Builds/macOS/Universal`, `Builds/Windows`, `Builds/Linux`) to avoid mixing files when switching between configurations.

After building, plugins are copied according to `project-configuration.cmake` settings:
- **System folders**: for immediate DAW testing
- **Central artefacts folder**: for centralized organization (if `COPY_TO_ARTEFACTS_DIR` is ON)

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

**Note:** On Apple Silicon, this preset is rejected at configure; use "macOS Intel-Rosetta" instead.

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

When building for Intel compatibility on an Apple Silicon Mac, use the Intel-Rosetta preset. Build outputs go to your configured central artefacts folder under `macOS/Intel-Rosetta/` (path set in `project-configuration.cmake` via `ARTEFACTS_DIR_MACOS`). On Mac Intel, this preset is rejected at configure; use "macOS Intel" instead.

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

The project uses **CMake Presets** for flexible configuration. Simply:

1. Open the project folder in Cursor
2. Select your preferred CMake preset when prompted:
   - **macOS Apple Silicon (Native)**: `default-macos-arm64` → builds to `Builds/macOS/ARM`
   - **macOS Intel (Native on Mac Intel)**: `default-macos-x86_64` → builds to `Builds/macOS/Intel`
   - **macOS Intel-Rosetta (x86_64 on Apple Silicon)**: `default-macos-x86_64-rosetta` → builds to `Builds/macOS/Intel-Rosetta`
   - **macOS Universal (Distribution)**: `default-macos-universal` → builds to `Builds/macOS/Universal`
   - **Windows**: `default-windows` → builds to `Builds/Windows`
   - **Linux**: `default-linux` → builds to `Builds/Linux`

3. Build the project:
   - **Recommended**: Press `Cmd+Shift+B` (macOS) or `Ctrl+Shift+B` (Windows/Linux) to build
   - **Or** use command palette: `Cmd+Shift+P` → "CMake: Build"
   - **Or** run specific tasks: `Cmd+Shift+P` → "Tasks: Run Task" → Choose task

**Switching presets**: Click the preset name in the status bar (bottom of Cursor window) or use `Cmd+Shift+P` → "CMake: Select Configure Preset". All paths automatically adapt to the selected preset.

### Build Artefacts

After building, plugins are automatically copied according to your `project-configuration.cmake` settings:

1. **System folders** (`COPY_TO_SYSTEM_FOLDERS`): Copies where DAWs scan by default for immediate testing
   - **macOS**: `~/Library/Audio/Plug-Ins/Components/` (AU), `~/Library/Audio/Plug-Ins/VST3/` (VST3)
   - **Windows**: `%LOCALAPPDATA%\Programs\Common\VST3\`
   - **Linux**: `~/.vst3/`

2. **Central custom folder** (`COPY_TO_ARTEFACTS_DIR`): Organized location for all projects
   - Paths configured in `generator-configuration.py` and injected at generation (`ARTEFACTS_DIR_*`)
   - **Structure**: `{{ARTEFACTS_DIR}}/{{OS}}/{{arch}}/{{format}}/`
   - **macOS**: `macOS/ARM/`, `Intel/`, `Intel-Rosetta/`, or `Universal/` (each contains `AU/`, `VST3/`, `Standalone/`)
   - **Windows**: `Windows/VST3/`, `Windows/Standalone/`
   - **Linux**: `Linux/VST3/`, `Linux/Standalone/`

The destination **automatically matches your selected preset**. No manual configuration needed.

### Build Artefact Copy Configuration

Control where plugins are copied after each build by editing the **USER OPTIONS** section in `project-configuration.cmake`:

- **`USER_COPY_TO_SYSTEM_FOLDERS`**: `ON`/`OFF`
  - Copies to system folders where DAWs scan (all OS)
  - **Use case**: Instant testing in your DAW
  
- **`USER_COPY_TO_ARTEFACTS_DIR`**: `ON`/`OFF`
  - Copies to central custom folder (paths `ARTEFACTS_DIR_*`)
  - Organized by platform and architecture
  - **Use case**: Centralized management, backup, distribution prep

Both can be enabled simultaneously for maximum convenience.

### Debugging

Debug configurations automatically use the active preset's build directory. Press `F5` to start debugging:

- **macOS**: Standalone, AU in Logic Pro, VST3 in Reaper, AU in Ableton Live
- **Windows**: Standalone, VST3 in Reaper

All paths adapt automatically when you switch presets.

### Command Line Usage (Advanced)

For advanced users or CI/CD:

```bash
# List available presets
cmake --list-presets

# Configure with a specific preset
cmake --preset default-macos-universal

# Build with the preset
cmake --build --preset default-macos-universal

# Or chain them
cmake --preset default-macos-universal && cmake --build --preset default-macos-universal
```
