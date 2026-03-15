#!/usr/bin/env python3
"""Utilities: exit handling, wait for user, common prompts."""

import sys

from uiConstants import Color


def getValidBooleanInput(prompt: str, default: bool = False) -> bool:
    """Prompt for y/n. Returns True for y/yes, False for n/no."""
    defaultStr = "Y/n" if default else "y/N"
    while True:
        choice = input(f"{prompt} [{defaultStr}]: ").strip()
        if choice == '':
            return default
        choiceLower = choice.lower()
        if choiceLower in ['y', 'yes']:
            return True
        if choiceLower in ['n', 'no']:
            return False
        _showInvalidBooleanInputError()


def getValidChoice(prompt: str, minVal: int, maxVal: int, default: int) -> int:
    """Prompt for integer in [minVal, maxVal]. Empty input returns default."""
    hint = f"{minVal}-{maxVal}"
    while True:
        raw = input(f"{prompt} [{hint}, default {default}]: ").strip()
        if raw == '':
            return default
        try:
            value = int(raw)
            if minVal <= value <= maxVal:
                return value
        except ValueError:
            pass
        print(f"{Color.RED}❌ Enter a number between {minVal} and {maxVal}{Color.RESET}")


def _showInvalidBooleanInputError() -> None:
    print(f"{Color.RED}❌ Invalid response. Please enter 'y' or 'n'{Color.RESET}")


def waitForEnterToExit() -> None:
    print(f"\n{Color.YELLOW}Press [Enter] to exit...{Color.RESET}")
    try:
        input()
    except (EOFError, KeyboardInterrupt):
        pass


def exitWithError(message: str = "") -> None:
    if message:
        print(message)
    waitForEnterToExit()
    sys.exit(1)
