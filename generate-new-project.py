#!/usr/bin/env python3
"""
JUCE Project Generator - CMake + Cursor
Orchestrates config loading, user input, file generation, and success display.
"""

import sys
from pathlib import Path

from Generator import (
    ConfigLoader,
    FileGenerator,
    InputCollector,
    SummaryDisplay,
    TemplateLoader,
    SuccessDisplay,
    TemplateRenderer,
    exitWithError,
    Color,
    kHeaderWidth,
)


def printHeader(configLoadError: str = None) -> None:
    """Print generator header and optional config error."""
    print(f"\n{Color.BLUE}{'=' * kHeaderWidth}{Color.RESET}")
    print(f"{Color.BLUE}  JUCE Project Generator - CMake + Cursor{Color.RESET}")
    print(f"{Color.BLUE}{'=' * kHeaderWidth}{Color.RESET}\n")
    if configLoadError:
        print(f"{Color.YELLOW}⚠️  Warning: Could not load generator-configuration.py:{Color.RESET}")
        print(f"{Color.YELLOW}   Error: {configLoadError}{Color.RESET}")
        print(f"{Color.YELLOW}   Using default values. Please check your generator-configuration.py file.{Color.RESET}\n")


def _runGenerationPipeline(scriptDir: Path, config: dict, data) -> None:
    templatesDir = scriptDir / "Templates"
    templateLoader = TemplateLoader(templatesDir)
    renderer = TemplateRenderer(data, config)
    fileGenerator = FileGenerator(
        templateLoader,
        data.projectDir,
        data,
        renderer,
        scriptDir,
    )
    fileGenerator.generateAll()


def main() -> None:
    scriptDir = Path(__file__).parent
    configLoader = ConfigLoader(scriptDir)
    config = configLoader.loadAll()

    printHeader(configLoader.getConfigLoadError())

    inputCollector = InputCollector(config)
    data = inputCollector.collect()

    summaryDisplay = SummaryDisplay(data)
    if not summaryDisplay.show():
        print(f"{Color.RED}❌ Project creation cancelled{Color.RESET}\n")
        sys.exit(0)

    _runGenerationPipeline(scriptDir, config, data)

    successDisplay = SuccessDisplay(data)
    successDisplay.show()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exitWithError(f"\n{Color.RED}❌ Operation cancelled by user{Color.RESET}\n")
    except Exception as e:
        exitWithError(f"\n{Color.RED}❌ Error: {e}{Color.RESET}\n")
