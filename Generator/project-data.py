#!/usr/bin/env python3
"""ProjectData: holds all collected project information."""

from pathlib import Path


class ProjectData:
    """Holds all collected project information."""

    def __init__(self):
        self.projectName = ""
        self.projectDisplayName = ""
        self.projectVersion = ""
        self.manufacturerName = ""
        self.manufacturerCode = ""
        self.pluginCode = ""
        self.pluginFormats = ""
        self.destinationDir = ""
        self.projectDir = Path()
        self.bundleId = ""
        self.isSynth = "FALSE"
        self.needsMidiInput = "FALSE"
        self.needsMidiOutput = "FALSE"
        self.isMidiEffect = "FALSE"
        self.auMainType = ""
        self.vst3Categories = ""
