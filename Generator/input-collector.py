#!/usr/bin/env python3
"""
InputCollector: collects project information from user via interactive prompts.
Single responsibility: user input collection and validation.
"""

import re
from pathlib import Path
from typing import Callable, List, NamedTuple

from pathValidation import hasProblematicChars, formatProblematicCharsString, showInteractivePathError
from pluginCategories import generateBundleId, updateAuAndVst3Categories
from projectData import ProjectData
from uiConstants import Color, kAllowedDisplayNameChars, kManufacturerCodeLength, kPluginCodeLength
from utils import getValidBooleanInput, getValidChoice


class _CodeInputSpec(NamedTuple):
    promptPrefix: str
    default: str
    length: int
    validator: Callable[[str], bool]
    errorMsg: str


class InputCollector:
    """Collects project info from user via prompts."""

    def __init__(self, config: dict):
        self.config_ = config
        self.kDefaultVersion = "1.0.0"
        self.kDefaultPluginName = "NewPlugin"

    def collect(self) -> ProjectData:
        """Run all prompts and return ProjectData."""
        data = ProjectData()
        data.projectName, data.projectDisplayName = self._inputProjectName()
        data.projectDir = Path(self.config_["destination"]) / data.projectName
        data.projectVersion = self._inputVersion()
        data.manufacturerName = self._inputManufacturerName()
        data.manufacturerCode = self._inputManufacturerCode()
        data.pluginCode = self._inputPluginCode()
        data.bundleId = generateBundleId(data.manufacturerName, data.projectName)
        self._configurePluginSettings(data)
        data.pluginFormats = self._selectPluginFormats()
        data.destinationDir = self._selectDestinationFolder()
        data.projectDir = Path(data.destinationDir) / data.projectName
        return data

    def _inputProjectName(self) -> tuple:
        while True:
            techName = input(f"  Technical project name [{self.kDefaultPluginName}]: ").strip() or self.kDefaultPluginName
            if not self._isValidProjectName(techName):
                self._showInvalidProjectNameError()
                continue
            projectDir = Path(self.config_["destination"]) / techName
            if projectDir.exists() and not self._handleExistingProject(techName):
                continue
            displayName = self._inputDisplayName(techName)
            return techName, displayName

    def _inputDisplayName(self, default: str) -> str:
        while True:
            displayName = input(f"  Display name (optional) [{default}]: ").strip() or default
            if self._isValidDisplayName(displayName):
                return displayName
            self._showInvalidDisplayNameError(displayName)

    def _inputVersion(self) -> str:
        return input(f"  Project version [{self.kDefaultVersion}]: ").strip() or self.kDefaultVersion

    def _inputManufacturerName(self) -> str:
        default = self.config_["manufacturer"]
        return input(f"  Manufacturer name [{default}]: ").strip() or default

    def _inputValidatedCode(self, spec: _CodeInputSpec) -> str:
        while True:
            code = input(f"  {spec.promptPrefix} ({spec.length} chars) [{spec.default}]: ").strip()
            if code == '':
                return spec.default
            if len(code) == spec.length and spec.validator(code):
                return code
            print(f"{Color.RED}❌ {spec.errorMsg}{Color.RESET}")

    def _inputManufacturerCode(self) -> str:
        spec = _CodeInputSpec(
            "Manufacturer code",
            self.config_["manufacturerCode"],
            kManufacturerCodeLength,
            str.isalpha,
            f"Must be exactly {kManufacturerCodeLength} alphabetic characters",
        )
        return self._inputValidatedCode(spec)

    def _inputPluginCode(self) -> str:
        spec = _CodeInputSpec(
            "Plugin code",
            self.config_["pluginCode"],
            kPluginCodeLength,
            str.isalnum,
            f"Must be exactly {kPluginCodeLength} alphanumeric characters",
        )
        return self._inputValidatedCode(spec)

    def _selectPluginFormats(self) -> str:
        print(f"\n{Color.YELLOW}Select plugin formats:{Color.RESET}")
        formats = ["AU", "VST3", "Standalone"]
        selected = []
        for fmt in formats:
            if getValidBooleanInput(f"  Include {fmt}?", default=True):
                selected.append(fmt)
        if not selected:
            print(f"{Color.RED}❌ At least one format must be selected{Color.RESET}\n")
            return self._selectPluginFormats()
        return " ".join(selected)

    def _selectDestinationFolder(self) -> str:
        print(f"\n{Color.YELLOW}Finalization:{Color.RESET}")
        default = self.config_["destination"]
        while True:
            destination = input(f"  Destination folder [{default}]: ").strip() or default
            hasProblematic, problematicChars = hasProblematicChars(destination)
            if not hasProblematic:
                return destination
            showInteractivePathError(destination, problematicChars)

    def _configurePluginSettings(self, data: ProjectData) -> None:
        print(f"\n{Color.YELLOW}Plugin Type:{Color.RESET}")
        print("  [1] Synthesizer")
        print("  [2] Audio Effect")
        print("  [3] MIDI Effect")
        choice = getValidChoice("  Plugin type", 1, 3, 1)
        data.isSynth = "TRUE" if choice == 1 else "FALSE"
        data.isMidiEffect = "TRUE" if choice == 3 else "FALSE"
        data.needsMidiInput, data.needsMidiOutput = self._midiDefaultsForPluginType(choice)
        data.auMainType, data.vst3Categories = updateAuAndVst3Categories(data.isSynth, data.isMidiEffect)

    def _midiDefaultsForPluginType(self, choice: int) -> tuple:
        """Return (needsMidiInput, needsMidiOutput) as CMake strings from plugin type choice."""
        if choice == 1:
            return "TRUE", "FALSE"
        if choice == 3:
            return "TRUE", "TRUE"
        return "FALSE", "FALSE"

    def _isValidProjectName(self, name: str) -> bool:
        return bool(re.match(r'^[a-zA-Z][a-zA-Z0-9_-]*$', name))

    def _isValidDisplayName(self, name: str) -> bool:
        return all(c in kAllowedDisplayNameChars for c in name)

    def _findInvalidCharsInDisplayName(self, name: str) -> List[str]:
        return [c for c in name if c not in kAllowedDisplayNameChars]

    def _showInvalidProjectNameError(self) -> None:
        print(f"{Color.RED}❌ Technical name must start with a letter and contain only letters, numbers, hyphens, and underscores{Color.RESET}")

    def _showInvalidDisplayNameError(self, name: str) -> None:
        invalid = self._findInvalidCharsInDisplayName(name)
        charsStr = formatProblematicCharsString(invalid)
        print(f"{Color.RED}❌ Display name contains invalid characters: {charsStr}{Color.RESET}")
        print(f"{Color.YELLOW}   Use letters, numbers, spaces, hyphens, underscores only.{Color.RESET}")

    def _handleExistingProject(self, techName: str) -> bool:
        dest = self.config_["destination"]
        print(f"\n{Color.YELLOW}⚠️  A folder named '{techName}' already exists at {dest}{Color.RESET}")
        if getValidBooleanInput("Overwrite existing folder?"):
            print(f"{Color.YELLOW}Existing folder will be overwritten.{Color.RESET}\n")
            return True
        print(f"{Color.YELLOW}Please choose a different technical name.\n{Color.RESET}")
        return False
