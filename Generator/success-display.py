#!/usr/bin/env python3
"""
SuccessDisplay: displays success message and next steps after project generation.
Single responsibility: user feedback at end of generation.
"""

from typing import TYPE_CHECKING

from platformInfo import getPlatformDisplayName, getPlatformPreset
from uiConstants import Color, kHeaderWidth
from utils import waitForEnterToExit

if TYPE_CHECKING:
    from projectData import ProjectData


class SuccessDisplay:
    """Displays success message with platform-specific next steps."""

    def __init__(self, data: "ProjectData"):
        self.data_ = data

    def show(self) -> None:
        """Print success message and wait for user."""
        platformName = getPlatformDisplayName()
        presetName = getPlatformPreset()
        self._printHeader()
        self._printLocation()
        self._printNextSteps(platformName, presetName)
        self._printFooter()
        waitForEnterToExit()

    def _getOpenCommand(self, projectPathStr: str) -> str:
        import platform
        if platform.system() == "Windows":
            return f"cd \"{projectPathStr}\"; cursor ."
        return f"cd {projectPathStr} && cursor ."

    def _printHeader(self) -> None:
        print(f"\n{Color.GREEN}{'=' * kHeaderWidth}{Color.RESET}")
        print(f"{Color.GREEN}✅ Project created successfully!{Color.RESET}")
        print(f"{Color.GREEN}{'=' * kHeaderWidth}{Color.RESET}\n")

    def _printLocation(self) -> None:
        print(f"{Color.BLUE}📍 Location:{Color.RESET} {self.data_.projectDir}\n")

    def _printOpenInstructions(self, openCommand: str) -> None:
        print(f"  1. Open project in Cursor:")
        print(f"     {Color.BLUE}{openCommand}{Color.RESET}\n")

    def _printConfigurationInfo(self, platformName: str, presetName: str) -> None:
        print(f"  2. CMake presets available for this project:")
        print(f"     - Current platform: {platformName} (preset: {presetName})")
        print(f"     - Select any preset in Cursor to build for different architectures\n")

    def _printCursorInstructions(self) -> None:
        print(f"  3. In Cursor:")
        print(f"     - Choose your CMake preset when prompted")
        print(f"     - Build: Press {Color.BLUE}Cmd+Shift+B{Color.RESET} (macOS) or {Color.BLUE}Ctrl+Shift+B{Color.RESET} (Windows/Linux)")
        print(f"     - Debug: Press {Color.BLUE}F5{Color.RESET} to start debugging\n")

    def _printReconfigurationNote(self) -> None:
        print(f"  {Color.YELLOW}Note:{Color.RESET} To switch between ARM/Intel/Universal on macOS, or change platforms:")
        print(f"     - Click the preset name in Cursor's status bar (bottom)")
        print(f"     - Or use: {Color.BLUE}Cmd+Shift+P{Color.RESET} → \"CMake: Select Configure Preset\"")
        print(f"     - All paths automatically adapt to the selected preset\n")

    def _printNextSteps(self, platformName: str, presetName: str) -> None:
        projectPathStr = str(self.data_.projectDir)
        openCommand = self._getOpenCommand(projectPathStr)
        print(f"{Color.YELLOW}Next steps:{Color.RESET}\n")
        self._printOpenInstructions(openCommand)
        self._printConfigurationInfo(platformName, presetName)
        self._printCursorInstructions()
        self._printReconfigurationNote()

    def _printFooter(self) -> None:
        print(f"{Color.GREEN}{'=' * kHeaderWidth}{Color.RESET}\n")
