#!/usr/bin/env python3
"""
TemplateRenderer: renders template content with project variables.
Single responsibility: template variable substitution.
"""

from typing import TYPE_CHECKING

from platformInfo import (
    BUILD_DIR_LINUX,
    BUILD_DIR_WINDOWS,
    getBuildDirMacOS,
    getPlatformBuildConfig,
)

if TYPE_CHECKING:
    from projectData import ProjectData


class TemplateRenderer:
    """Renders template content with project and config variables."""

    def __init__(self, data: "ProjectData", config: dict):
        self.data_ = data
        self.config_ = config

    def _buildFormatContext(self) -> dict:
        copyToSystem = "ON" if self.config_["copyToSystemFolders"] else "OFF"
        copyToProject = "ON" if self.config_["copyToProjectFolders"] else "OFF"
        return {
            "projectName": self.data_.projectName,
            "projectDisplayName": self.data_.projectDisplayName,
            "projectVersion": self.data_.projectVersion,
            "manufacturerName": self.data_.manufacturerName,
            "manufacturerCode": self.data_.manufacturerCode,
            "pluginCode": self.data_.pluginCode,
            "pluginFormats": self.data_.pluginFormats,
            "isSynth": self.data_.isSynth,
            "needsMidiInput": self.data_.needsMidiInput,
            "needsMidiOutput": self.data_.needsMidiOutput,
            "isMidiEffect": self.data_.isMidiEffect,
            "auMainType": self.data_.auMainType,
            "vst3Categories": self.data_.vst3Categories,
            "bundleId": self.data_.bundleId,
            "copyToSystemFolders": copyToSystem,
            "copyToProjectFolders": copyToProject,
            "buildDirMacOS": getBuildDirMacOS(),
            "buildDirWindows": BUILD_DIR_WINDOWS,
            "buildDirLinux": BUILD_DIR_LINUX,
        }

    def render(self, templateContent: str) -> str:
        return templateContent.format(**self._buildFormatContext())

    def getPlatformBuildConfig(self) -> tuple:
        """Return (buildDir, presetName) for current platform."""
        return getPlatformBuildConfig()
