#!/usr/bin/env python3
"""
PathValidation: detects problematic characters (accents, non-ASCII) in paths.
Single responsibility: path character validation.
"""

from typing import List, Tuple

from pathErrorMessages import PathErrorContext, buildFullPathErrorMessage
from uiConstants import Color, kMaxCharsInErrorList


def isPathSeparator(char: str) -> bool:
    return char in ['/', '\\', ':', ' ']


def isNonAsciiChar(char: str) -> bool:
    return ord(char) > 127


def findProblematicCharsInPath(path: str) -> List[str]:
    problematicChars = []
    for char in path:
        if isPathSeparator(char):
            continue
        if isNonAsciiChar(char):
            problematicChars.append(char)
    return problematicChars


def hasProblematicChars(path: str) -> Tuple[bool, List[str]]:
    problematicChars = findProblematicCharsInPath(path)
    return len(problematicChars) > 0, problematicChars


def formatProblematicCharsString(problematicChars: List[str]) -> str:
    uniqueChars = list(set(problematicChars))
    charsStr = ', '.join(f"'{c}'" for c in uniqueChars[:kMaxCharsInErrorList])
    if len(uniqueChars) > kMaxCharsInErrorList:
        charsStr += f" ... (and {len(uniqueChars) - kMaxCharsInErrorList} more)"
    return charsStr


def validatePathNoProblematicChars(
    path: str,
    pathName: str,
    configFile: str = "generator-configuration.py",
) -> None:
    """Validate path. Exits with error message if invalid."""
    hasProblematic, problematicChars = hasProblematicChars(path)
    if not hasProblematic:
        return
    charsStr = formatProblematicCharsString(problematicChars)
    ctx = PathErrorContext(pathName, path, charsStr, configFile)
    from utils import exitWithError
    exitWithError(buildFullPathErrorMessage(ctx))


def showInteractivePathError(destination: str, problematicChars: List[str]) -> None:
    charsStr = formatProblematicCharsString(problematicChars)
    print(f"\n{Color.RED}❌ ERROR: The path contains problematic characters.{Color.RESET}")
    print(f"{Color.YELLOW}   Path: {destination}{Color.RESET}")
    print(f"{Color.YELLOW}   Detected characters: {charsStr}{Color.RESET}")
    print(f"{Color.YELLOW}   Paths with accents cause build errors with CMake/Visual Studio.{Color.RESET}")
    print(f"{Color.YELLOW}   Solution: Use a path without accents (e.g., 'Telechargements' instead of 'Téléchargements'){Color.RESET}\n")
