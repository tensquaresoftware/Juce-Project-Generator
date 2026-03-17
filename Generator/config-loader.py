#!/usr/bin/env python3
"""
ConfigLoader: loads generator defaults from generator-configuration.py and project-config.cmake.
Single responsibility: configuration loading and aggregation.
"""

import platform
import importlib.util
from importlib.util import module_from_spec as moduleFromSpec
from importlib.util import spec_from_file_location as specFromFileLocation
from pathlib import Path
from typing import Callable, Dict, NamedTuple, Optional

from pathValidation import validatePathNoProblematicChars
from projectConfigParser import parse as parseProjectConfig, getValue, parseBool
from uiConstants import Color, kManufacturerCodeLength, kPluginCodeLength

_JUCE_DIR_ATTR_BY_SYSTEM = {
    "Darwin": "JUCE_DIR_MACOS",
    "Windows": "JUCE_DIR_WINDOWS",
    "Linux": "JUCE_DIR_LINUX",
}

_DEFAULT_PROJECT_DIR_ATTR_BY_SYSTEM = {
    "Darwin": "DEFAULT_PROJECT_DIR_MACOS",
    "Windows": "DEFAULT_PROJECT_DIR_WINDOWS",
    "Linux": "DEFAULT_PROJECT_DIR_LINUX",
}


class _ValidatedCodeSpec(NamedTuple):
    attrName: str
    length: int
    validator: Callable[[str], bool]
    default: str
    warningFn: Callable[[], None]


def _loadGeneratorConfigModule(scriptDir: Path) -> tuple:
    """Load generator-configuration.py. Returns (module, errorMsg)."""
    configPath = scriptDir / "generator-configuration.py"
    if not configPath.exists():
        return None, None
    try:
        spec = specFromFileLocation("generatorConfiguration", configPath)
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot load module from {configPath}")
        module = moduleFromSpec(spec)
        runModule = spec.loader.exec_module
        runModule(module)
        return module, None
    except Exception as e:
        return None, str(e)


class ConfigLoader:
    """Loads and holds generator configuration from config files."""

    def __init__(self, scriptDir: Path):
        self.scriptDir_ = scriptDir
        self.configModule_, self.configLoadError_ = _loadGeneratorConfigModule(scriptDir)
        self.projectConfigPath_ = scriptDir / "project-configuration.cmake"

    def loadAll(self) -> Dict:
        """Load all config values. Returns dict with keys: destination, manufacturer, etc."""
        return {
            "destination": self._loadDestination(),
            "manufacturer": self._loadManufacturer(),
            "manufacturerCode": self._loadManufacturerCode(),
            "pluginCode": self._loadPluginCode(),
            "copyToSystemFolders": self._loadCopyToSystemFolders(),
            "copyToArtefactsDir": self._loadCopyToArtefactsDir(),
            "artefactsDirWindows": self._loadArtefactsDir("ARTEFACTS_DIR_WINDOWS"),
            "artefactsDirMacos": self._loadArtefactsDir("ARTEFACTS_DIR_MACOS"),
            "artefactsDirLinux": self._loadArtefactsDir("ARTEFACTS_DIR_LINUX"),
            "juceDir": self._loadJuceDir(),
        }

    def getConfigLoadError(self) -> Optional[str]:
        """Return error message if generator-configuration.py failed to load."""
        return self.configLoadError_

    def _loadDestination(self) -> str:
        system = platform.system()
        attrName = _DEFAULT_PROJECT_DIR_ATTR_BY_SYSTEM.get(system)
        if not self.configModule_ or not attrName or not hasattr(self.configModule_, attrName):
            return str(Path.home() / "Desktop")
        dest = getattr(self.configModule_, attrName)
        if not dest or dest.lower() == "desktop":
            return str(Path.home() / "Desktop")
        validatePathNoProblematicChars(dest, attrName)
        return dest

    def _loadManufacturer(self) -> str:
        if self.configModule_ and hasattr(self.configModule_, 'DEFAULT_MANUFACTURER_NAME'):
            name = self.configModule_.DEFAULT_MANUFACTURER_NAME
            if name:
                return name
        return "My Company"

    def _loadValidatedCode(self, spec: _ValidatedCodeSpec) -> str:
        code = getattr(self.configModule_, spec.attrName, None) if self.configModule_ else None
        if not code:
            return spec.default
        if len(code) == spec.length and spec.validator(code):
            return code
        spec.warningFn()
        return spec.default

    def _loadManufacturerCode(self) -> str:
        spec = _ValidatedCodeSpec(
            "DEFAULT_MANUFACTURER_CODE",
            kManufacturerCodeLength,
            str.isalpha,
            "Myco",
            self._showInvalidManufacturerCodeWarning,
        )
        return self._loadValidatedCode(spec)

    def _loadPluginCode(self) -> str:
        spec = _ValidatedCodeSpec(
            "DEFAULT_PLUGIN_CODE",
            kPluginCodeLength,
            str.isalnum,
            "Mypl",
            self._showInvalidPluginCodeWarning,
        )
        return self._loadValidatedCode(spec)

    def _loadCopyFlag(self, userKey: str, cacheKey: str, default: str) -> bool:
        cfg = parseProjectConfig(self.projectConfigPath_)
        val = getValue(cfg, userKey, cacheKey, default)
        return parseBool(val)

    def _loadCopyToSystemFolders(self) -> bool:
        return self._loadCopyFlag("USER_COPY_TO_SYSTEM_FOLDERS", "COPY_TO_SYSTEM_FOLDERS", "OFF")

    def _loadCopyToArtefactsDir(self) -> bool:
        return self._loadCopyFlag("USER_COPY_TO_ARTEFACTS_DIR", "COPY_TO_ARTEFACTS_DIR", "ON")

    def _loadArtefactsDir(self, attrName: str) -> str:
        if not self.configModule_ or not hasattr(self.configModule_, attrName):
            return ""
        artefactsDir = getattr(self.configModule_, attrName)
        if not artefactsDir:
            return ""
        validatePathNoProblematicChars(artefactsDir, attrName)
        return Path(artefactsDir).as_posix()

    def _loadJuceDir(self) -> Optional[str]:
        system = platform.system()
        attrName = _JUCE_DIR_ATTR_BY_SYSTEM.get(system)
        if not attrName or not self.configModule_:
            return None
        juceDir = getattr(self.configModule_, attrName, None)
        if not juceDir:
            return None
        normalized = Path(juceDir).as_posix()
        if not Path(normalized).exists():
            self._showJuceDirNotFoundWarning(normalized)
        return normalized

    def _showInvalidManufacturerCodeWarning(self) -> None:
        print(f"{Color.YELLOW}⚠️  Warning: DEFAULT_MANUFACTURER_CODE in generator-configuration.py is invalid (must be {kManufacturerCodeLength} alphabetic chars). Using default.{Color.RESET}")

    def _showInvalidPluginCodeWarning(self) -> None:
        print(f"{Color.YELLOW}⚠️  Warning: DEFAULT_PLUGIN_CODE in generator-configuration.py is invalid (must be {kPluginCodeLength} alphanumeric chars). Using default.{Color.RESET}")

    def _showJuceDirNotFoundWarning(self, juceDir: str) -> None:
        print(f"{Color.YELLOW}⚠️  Warning: JUCE_DIR path '{juceDir}' does not exist. Project generation will continue, but CMake configuration may fail.{Color.RESET}")
