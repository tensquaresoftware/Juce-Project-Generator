#!/usr/bin/env python3
"""UI constants: colors, display widths, character whitelists."""


class Color:
    RED = '\033[0;91m'
    GREEN = '\033[0;92m'
    BLUE = '\033[0;96m'
    YELLOW = '\033[1;33m'
    RESET = '\033[0m'


kManufacturerCodeLength = 4
kPluginCodeLength = 4
kMaxCharsInErrorList = 10
kHeaderWidth = 60
kPathErrorWidth = 70

# Display name whitelist: letters, digits, spaces, hyphens, underscores
kAllowedDisplayNameChars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -_')
