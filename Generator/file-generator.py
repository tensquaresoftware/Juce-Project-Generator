#!/usr/bin/env python3
"""
FileGenerator: creates project structure and writes all generated files.
Single responsibility: file system operations for project generation.
"""

import shutil
from pathlib import Path
from typing import TYPE_CHECKING

from templateLoader import TemplateLoader
from uiConstants import Color

if TYPE_CHECKING:
    from projectData import ProjectData
    from templateRenderer import TemplateRenderer


class FileGenerator:
    """Generates all project files from templates."""

    def __init__(
        self,
        templateLoader: TemplateLoader,
        projectDir: Path,
        data: "ProjectData",
        renderer: "TemplateRenderer",
        scriptDir: Path,
    ):
        self.loader_ = templateLoader
        self.projectDir_ = projectDir
        self.data_ = data
        self.renderer_ = renderer
        self.scriptDir_ = scriptDir

    def generateAll(self) -> None:
        """Create structure and generate all files."""
        self._createStructure()
        self._generateCMakeLists()
        self._generateProjectConfig()
        self._generatePluginProcessor()
        self._generatePluginEditor()
        self._generatePluginFactory()
        self._generateVSCodeSettings()
        self._generateVSCodeTasks()
        self._generateVSCodeLaunch()
        self._generateCursorRules()
        self._generateGitIgnore()
        self._generateCMakeUserPresets()
        self._generateReadme()

    def _createStructure(self) -> None:
        print(f"\n{Color.GREEN}📁 Creating project structure...{Color.RESET}")
        if self.projectDir_.exists():
            shutil.rmtree(self.projectDir_)
        (self.projectDir_ / "Source").mkdir(parents=True, exist_ok=True)
        (self.projectDir_ / ".vscode").mkdir(parents=True, exist_ok=True)

    def _writeFile(self, relativePath: str, content: str) -> None:
        filePath = self.projectDir_ / relativePath
        filePath.parent.mkdir(parents=True, exist_ok=True)
        filePath.write_text(content, encoding='utf-8')

    def _generateFromTemplate(self, templatePath: str, outputPath: str) -> None:
        content = self.loader_.load(templatePath)
        rendered = self.renderer_.render(content)
        self._writeFile(outputPath, rendered)

    def _generateSourcePair(self, componentName: str, basePath: str) -> None:
        print(f"{Color.GREEN}📝 Generating {componentName}.h...{Color.RESET}")
        self._generateFromTemplate(f"{basePath}.h", f"{basePath}.h")
        print(f"{Color.GREEN}📝 Generating {componentName}.cpp...{Color.RESET}")
        self._generateFromTemplate(f"{basePath}.cpp", f"{basePath}.cpp")

    def _generateCMakeLists(self) -> None:
        print(f"{Color.GREEN}📝 Generating CMakeLists.txt...{Color.RESET}")
        self._generateFromTemplate("CMakeLists.txt", "CMakeLists.txt")

    def _generateProjectConfig(self) -> None:
        print(f"{Color.GREEN}📝 Generating project-configuration.cmake...{Color.RESET}")
        self._generateFromTemplate("project-configuration.cmake", "project-configuration.cmake")

    def _generatePluginProcessor(self) -> None:
        self._generateSourcePair("PluginProcessor", "Source/PluginProcessor")

    def _generatePluginEditor(self) -> None:
        self._generateSourcePair("PluginEditor", "Source/PluginEditor")

    def _generatePluginFactory(self) -> None:
        print(f"{Color.GREEN}📝 Generating PluginFactory.cpp...{Color.RESET}")
        self._generateFromTemplate("Source/PluginFactory.cpp", "Source/PluginFactory.cpp")

    def _generateVSCodeSettings(self) -> None:
        print(f"{Color.GREEN}📝 Generating .vscode/settings.json...{Color.RESET}")
        self._generateFromTemplate(".vscode/settings.json", ".vscode/settings.json")

    def _generateVSCodeTasks(self) -> None:
        print(f"{Color.GREEN}📝 Generating .vscode/tasks.json...{Color.RESET}")
        self._generateFromTemplate(".vscode/tasks.json", ".vscode/tasks.json")

    def _generateVSCodeLaunch(self) -> None:
        print(f"{Color.GREEN}📝 Generating .vscode/launch.json...{Color.RESET}")
        self._generateFromTemplate(".vscode/launch.json", ".vscode/launch.json")

    def _generateCursorRules(self) -> None:
        print(f"{Color.GREEN}📝 Generating .cursorrules...{Color.RESET}")
        content = self.loader_.load(".cursorrules")
        self._writeFile(".cursorrules", content)

    def _generateGitIgnore(self) -> None:
        print(f"{Color.GREEN}📝 Generating .gitignore...{Color.RESET}")
        content = self.loader_.load(".gitignore")
        self._writeFile(".gitignore", content)

    def _generateCMakeUserPresets(self) -> None:
        print(f"{Color.GREEN}📝 Generating CMakeUserPresets.json...{Color.RESET}")
        content = self.loader_.load("CMakeUserPresets.json")
        self._writeFile("CMakeUserPresets.json", content)

    def _generateReadme(self) -> None:
        print(f"{Color.GREEN}📝 Generating README.md...{Color.RESET}")
        self._generateFromTemplate("README.md", "README.md")
