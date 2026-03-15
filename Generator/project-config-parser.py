#!/usr/bin/env python3
"""
ProjectConfigParser: parses project-config.cmake and extracts variable values.
Single responsibility: CMake set() variable extraction.
"""

import re
from pathlib import Path
from typing import Dict


def parse(configPath: Path) -> Dict[str, str]:
    """Parse project-config.cmake and return dict of variable names to values."""
    result: Dict[str, str] = {}
    if not configPath.exists():
        return result
    content = configPath.read_text(encoding='utf-8')
    pattern = r'set\s*\(\s*(\w+)\s+("(?:[^"\\]|\\.)*"|[^\s)]+)'
    for m in re.finditer(pattern, content):
        varName, val = m.group(1), m.group(2)
        if val.startswith('"') and val.endswith('"'):
            val = val[1:-1].replace('\\"', '"')
        result[varName] = val
    return result


def getValue(cfg: Dict[str, str], userKey: str, cacheKey: str, default: str) -> str:
    """Prefer USER_* variable over CACHE variable."""
    return cfg.get(userKey, cfg.get(cacheKey, default))


def parseBool(val: str) -> bool:
    """Convert CMake-style bool string to Python bool."""
    return val.upper() in ("ON", "TRUE", "1", "YES")
