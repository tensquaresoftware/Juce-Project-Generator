# JUCE Project Generator for CMake + Cursor

A Python-based project generator that creates complete JUCE plugin projects with CMake build system, optimized for development in Cursor (or VS Code).

---

**Author:** Guillaume DUPONT  
**Organization:** Ten Square Software  
**Version:** 1.0.0  
**Revision date:** 2025-12-12

---

## Features

- ✅ Complete JUCE plugin project structure
- ✅ CMake build system configuration
- ✅ Platform-specific settings (macOS/Windows)
- ✅ Cross-platform path normalization (automatic handling of Windows/macOS path differences)
- ✅ Cursor/VS Code integration (tasks, launch configs, settings)
- ✅ Automatic VST3 plugin installation to custom folder (Windows)
- ✅ Support for AU, VST3, and Standalone formats
- ✅ Configurable via `user-config.py` for easy customization
- ✅ Customizable default manufacturer and plugin codes

## Quick Start

### Prerequisites

- Python 3.7+
- JUCE 8 installed
- CMake 3.22+
- Cursor or VS Code

### Setup

1. **Configure JUCE installation path** (recommended):
   
   Edit `user-config.py` and set the JUCE path for your platform:
   
   - **macOS**: `JUCE_DIR_MACOS = "/Applications/JUCE"`
   - **Windows**: `JUCE_DIR_WINDOWS = "C:/JUCE"`
   - **Linux**: `JUCE_DIR_LINUX = "/opt/JUCE"`
   
   Alternatively, you can set the `JUCE_DIR` environment variable (see Configuration section below).

2. **Configure your environment** (optional):
   
   - Copy `user-config.py` and customize other settings (see Configuration section below)

3. **Run the generator**:
   
   ```bash
   python generate-new-juce-project.py
   ```

4. **Follow the interactive prompts** to create your project

## Configuration

The generator uses a `user-config.py` file to store user-specific settings. This allows you to:

- Customize default paths without modifying the core generator code
- Share the generator with others while keeping your personal settings separate
- Easily adapt the generator to different development environments

### Setup

1. **Create or Edit `user-config.py`**:
   
   The `user-config.py` file should be located in the same directory as `generate-new-juce-project.py`.
   
   If the file doesn't exist, the generator will use default values. You can create it by copying the example below.

2. **Configure Your Settings**:
   
   Edit `user-config.py` and modify the constants to match your environment.

### Configuration Options

#### `JUCE_DIR_MACOS`, `JUCE_DIR_WINDOWS`, `JUCE_DIR_LINUX`

**Purpose**: Defines the path to your JUCE installation directory for each platform.

**Why**: This eliminates the need to set the `JUCE_DIR` environment variable. The generator will automatically use the correct path based on your platform when creating projects.

**Examples**:

- macOS: `JUCE_DIR_MACOS = "/Applications/JUCE"`
- Windows: `JUCE_DIR_WINDOWS = "C:/JUCE"` or `"C:/Program Files/JUCE"` (forward slashes recommended, but backslashes are automatically normalized)
- Linux: `JUCE_DIR_LINUX = "/opt/JUCE"` or `"/usr/local/JUCE"`

**Note on path format**: The generator automatically normalizes paths for cross-platform compatibility. You can use forward slashes (`/`) or backslashes (`\`) on Windows - both will work correctly.

**Note**: 

- If set to `None` or not configured, the generated project will require the `JUCE_DIR` environment variable to be set.
- You can still override this per-project by setting the `JUCE_DIR` environment variable or configuring CMake with `-DJUCE_DIR=/path/to/JUCE`.

#### `CUSTOM_VST3_FOLDER_WINDOWS`

**Purpose**: Defines the default folder where VST3 plugins will be automatically copied after build on Windows.

**Why**: This allows you to test plugins in your DAW without requiring administrator privileges. The standard VST3 location (`C:\Program Files\Common Files\VST3`) requires admin rights, which can be inconvenient during development.

**Examples**:

- Personal folder: `"C:/Users/YourName/VST3"` or `"C:\\Users\\YourName\\VST3"` (both formats work)
- Custom drive: `"D:/MyPlugins/VST3"`
- Standard location (requires admin): `"C:/Program Files/Common Files/VST3"`

**Note**: The generator automatically normalizes paths, so you can use either forward slashes (`/`) or backslashes (`\`) on Windows.

**Note**: After setting this, configure your DAW (Ableton Live, Reaper, etc.) to scan this custom folder for VST3 plugins.

**⚠️ IMPORTANT - Path Restrictions**:

- **NO ACCENTED CHARACTERS**: Same restrictions as `DEFAULT_PROJECT_DESTINATION` - paths must NOT contain accented or special Unicode characters
- The generator will validate this path and **stop immediately** with an error message if problematic characters are detected

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

### Example `user-config.py`

```python
#!/usr/bin/env python3
"""
User Configuration file for JUCE Project Generator
===================================================

Customize the values below to match your development environment.
"""

# JUCE installation paths (set for your platform)
JUCE_DIR_MACOS = "/Applications/JUCE"
JUCE_DIR_WINDOWS = "C:/JUCE"
JUCE_DIR_LINUX = None  # Set to your JUCE path if needed

# Custom VST3 installation folder (Windows)
# Change this to your preferred VST3 folder
CUSTOM_VST3_FOLDER_WINDOWS = "C:/Users/YourName/VST3"

# Default project destination
# Set to "Default" to use Desktop, or specify a custom path
DEFAULT_PROJECT_DESTINATION = "Default"

# Default manufacturer information
# These will be used as defaults when generating new projects
DEFAULT_MANUFACTURER_NAME = "My Company"
DEFAULT_MANUFACTURER_CODE = "Myco"
DEFAULT_PLUGIN_CODE = "Plg1"
```

### How It Works

1. When you run `generate-new-juce-project.py`, it attempts to load `user-config.py`
2. If `user-config.py` exists and contains the constants, they are used
3. If `user-config.py` doesn't exist or constants are missing, default values are used
4. The constants are injected into the generated project templates

### Customizing Generated Projects

Even after generating a project, you can customize the VST3 folder:

1. **During CMake configuration**:
   
   ```bash
   cmake .. -DCUSTOM_VST3_FOLDER="your/custom/path"
   ```

2. **In the generated CMakeLists.txt**:
   Edit the `CUSTOM_VST3_FOLDER` value directly in the file (around line 108)

## Generated Project Structure

```
YourProject/
├── Source/
│   ├── PluginProcessor.h
│   ├── PluginProcessor.cpp
│   ├── PluginEditor.h
│   ├── PluginEditor.cpp
│   └── PluginFactory.cpp
├── .vscode/
│   ├── settings.json
│   ├── tasks.json
│   └── launch.json
├── CMakeLists.txt
├── CMakeUserPresets.json
├── configure-platform.py
└── README.md
```

## Usage

### Building

1. Open the project in Cursor

2. Select the CMake kit when prompted

3. Build the project:
   - Use the command palette: `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS) → "CMake: Build"
   - Or use the terminal:
   
   ```bash
   cmake --preset default-windows  # or default-macos
   cmake --build --preset default-windows
   ```

### Testing Plugins

#### macOS

- **AU**: Copy `.component` to `~/Library/Audio/Plug-Ins/Components/`
- **VST3**: Copy `.vst3` to `~/Library/Audio/Plug-Ins/VST3/`
- **Standalone**: Run the `.app` directly

#### Windows

- **VST3**: Automatically copied to your custom folder (configured in `user-config.py`)
  - Configure your DAW to scan this folder
  - Or manually copy to `C:\Program Files\Common Files\VST3\` (requires admin)
- **Standalone**: Run the `.exe` directly

### Debugging

Press `F5` in Cursor to start debugging. Debug configurations are available for:

- Standalone application
- Plugin in DAW (Logic Pro, Reaper, Ableton Live)

## Platform Switching

If you open a project on a different platform than where it was generated:

```bash
python configure-platform.py
```

This automatically updates `.vscode/settings.json` for the current platform.

## Customization

### Custom VST3 Folder

The generator automatically configures projects to copy VST3 plugins to a custom folder on Windows. This:

- Avoids requiring administrator privileges
- Makes testing faster during development
- Can be customized per-project or globally via `user-config.py`

To change the folder for a specific project, edit `CMakeLists.txt` or configure CMake:

```bash
cmake .. -DCUSTOM_VST3_FOLDER="your/custom/path"
```

## Path Restrictions

### ⚠️ IMPORTANT: No Accented Characters in Paths

**The generator STRICTLY prohibits accented characters and special Unicode characters in all paths.**

This includes:

- Project destination paths (`DEFAULT_PROJECT_DESTINATION`)
- VST3 folder paths (`CUSTOM_VST3_FOLDER_WINDOWS`)
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
- You must fix the path in `user-config.py` (or enter a valid path during interactive prompts) before the generator will proceed

## Troubleshooting

### Generator uses default values even after creating `user-config.py`

- Make sure `user-config.py` is in the same directory as `generate-new-juce-project.py`
- Check for syntax errors in `user-config.py` (Python syntax) - the generator will display a warning if there are errors
- Verify that constant names match exactly (case-sensitive)
- If you see a warning about invalid codes, check that:
  - `DEFAULT_MANUFACTURER_CODE` is exactly 4 alphabetic characters
  - `DEFAULT_PLUGIN_CODE` is exactly 4 alphanumeric characters

### What happens if `user-config.py` has errors?

The generator is designed to be resilient and will handle various error scenarios:

1. **Syntax errors in `user-config.py`**:
   
   - The generator will display a warning message showing the error
   - Default values will be used instead
   - Project generation will continue normally

2. **Invalid manufacturer/plugin codes**:
   
   - If codes don't match the required format (4 characters), a warning is displayed
   - Default values are used instead
   - You can still override them during interactive prompts

3. **Invalid or missing JUCE path**:
   
   - If the path doesn't exist, a warning is displayed
   - Project generation continues, but CMake configuration may fail later
   - You can set the `JUCE_DIR` environment variable as a fallback

4. **Missing constants**:
   
   - If a constant is not defined, the corresponding default value is used
   - No error is displayed (this is expected behavior)

### VST3 plugin not copying to custom folder

- The generator automatically normalizes paths (converts backslashes to forward slashes), so you can use either format in `user-config.py`
- Ensure the folder path doesn't require admin privileges (unless that's intentional)
- Verify the path is correct in the generated `CMakeLists.txt`

### Build errors with paths containing accents

If you see errors like `MSB8066` or malformed characters in build output:

- **This should not happen** if you followed the path restrictions
- Check that your project path doesn't contain accented characters
- If you're using an existing project, consider moving it to a path without accents
- The generator validates paths at creation time, but if you manually moved the project, you may need to regenerate it

## Sharing the Generator

When sharing this generator:

1. Include `user-config.py` with generic example values (as shown in the Configuration section)
2. Document that users should customize `user-config.py` for their environment
3. Include this README.md in your distribution

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]
