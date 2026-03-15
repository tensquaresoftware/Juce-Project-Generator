#!/usr/bin/env python3
"""
PathErrorMessages: builds formatted error messages for invalid paths.
Single responsibility: error message formatting for path validation.
"""

from typing import NamedTuple

from uiConstants import Color, kPathErrorWidth


class PathErrorContext(NamedTuple):
    pathName: str
    path: str
    charsStr: str
    configFile: str


def buildPathErrorHeader(configFile: str) -> str:
    return (
        f"\n{Color.RED}{'=' * kPathErrorWidth}{Color.RESET}\n"
        f"{Color.RED}❌ ERROR: Invalid path detected in {configFile}{Color.RESET}\n"
        f"{Color.RED}{'=' * kPathErrorWidth}{Color.RESET}\n\n"
    )


def buildPathErrorBody(pathName: str, path: str, charsStr: str) -> str:
    return (
        f"{Color.YELLOW}The parameter '{pathName}' contains problematic characters.{Color.RESET}\n\n"
        f"{Color.YELLOW}Problematic path:{Color.RESET}\n"
        f"  {Color.RED}{path}{Color.RESET}\n\n"
        f"{Color.YELLOW}Detected characters:{Color.RESET} {charsStr}\n\n"
    )


def buildPathErrorExplanation() -> str:
    return (
        f"{Color.YELLOW}Why this restriction?{Color.RESET}\n"
        f"  Paths with accents or special characters cause build errors\n"
        f"  with CMake/Visual Studio on Windows (error MSB8066).\n"
        f"  Generated .vcxproj files then contain incorrectly encoded characters.\n\n"
    )


def buildPathErrorSolution(pathName: str, configFile: str) -> str:
    return (
        f"{Color.YELLOW}Solution:{Color.RESET}\n"
        f"  1. Open the file {configFile}\n"
        f"  2. Modify '{pathName}' to use a path without accents\n"
        f"  3. Examples:\n"
        f"     ❌ \"C:/Users/John/Téléchargements\"\n"
        f"     ✅ \"C:/Users/John/Telechargements\"\n"
        f"     ❌ \"D:/Projets/Été 2024\"\n"
        f"     ✅ \"D:/Projets/Ete 2024\"\n\n"
    )


def buildPathErrorFooter() -> str:
    return (
        f"{Color.RED}The generator stops now to avoid creating a project in the wrong location.{Color.RESET}\n"
        f"{Color.RED}{'=' * kPathErrorWidth}{Color.RESET}\n"
    )


def buildFullPathErrorMessage(ctx: PathErrorContext) -> str:
    return (
        buildPathErrorHeader(ctx.configFile)
        + buildPathErrorBody(ctx.pathName, ctx.path, ctx.charsStr)
        + buildPathErrorExplanation()
        + buildPathErrorSolution(ctx.pathName, ctx.configFile)
        + buildPathErrorFooter()
    )
