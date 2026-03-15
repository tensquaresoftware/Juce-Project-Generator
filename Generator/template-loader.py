#!/usr/bin/env python3
"""
TemplateLoader: loads template file contents from Templates directory.
Single responsibility: reading template files from disk.
"""

from pathlib import Path


class TemplateLoader:
    """Loads template files from Templates directory."""

    def __init__(self, templatesDir: Path):
        self.templatesDir_ = templatesDir
        if not self.templatesDir_.exists():
            raise FileNotFoundError(f"Templates directory not found: {self.templatesDir_}")

    def load(self, templatePath: str) -> str:
        fullPath = self.templatesDir_ / templatePath
        if not fullPath.exists():
            raise FileNotFoundError(f"Template not found: {templatePath}")
        return fullPath.read_text(encoding='utf-8')
