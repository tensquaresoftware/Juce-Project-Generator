#!/usr/bin/env python3
"""
SummaryDisplay: displays project summary and asks for confirmation.
Single responsibility: summary presentation and create-project confirmation.
"""

from typing import TYPE_CHECKING

from pluginCategories import getPluginTypeDisplayName
from uiConstants import Color, kHeaderWidth
from utils import getValidBooleanInput

if TYPE_CHECKING:
    from projectData import ProjectData


class SummaryDisplay:
    """Displays summary and asks user to confirm project creation."""

    def __init__(self, data: "ProjectData"):
        self.data_ = data

    def show(self) -> bool:
        """Display summary and ask for confirmation. Returns True if user confirms."""
        self._printSummary()
        return getValidBooleanInput("Create project?", default=True)

    def _getSummaryFields(self) -> list[tuple[str, str]]:
        """Return list of (label, value) pairs for summary display."""
        return [
            ("Technical Name", self.data_.projectName),
            ("Display Name", self.data_.projectDisplayName),
            ("Version", self.data_.projectVersion),
            ("Manufacturer", self.data_.manufacturerName),
            ("Manufacturer Code", self.data_.manufacturerCode),
            ("Plugin Code", self.data_.pluginCode),
            ("Bundle ID", self.data_.bundleId),
            ("Plugin type", getPluginTypeDisplayName(self.data_.isSynth, self.data_.isMidiEffect)),
            ("MIDI Input", self.data_.needsMidiInput),
            ("MIDI Output", self.data_.needsMidiOutput),
            ("Formats", self.data_.pluginFormats),
            ("Destination", self.data_.projectDir),
        ]

    def _printSummary(self) -> None:
        print(f"\n{Color.YELLOW}{'=' * kHeaderWidth}{Color.RESET}")
        print(f"{Color.YELLOW}Summary{Color.RESET}")
        print(f"{Color.YELLOW}{'=' * kHeaderWidth}{Color.RESET}")
        for label, value in self._getSummaryFields():
            print(f"  {label:18} : {value}")
        print(f"{Color.YELLOW}{'=' * kHeaderWidth}{Color.RESET}\n")
