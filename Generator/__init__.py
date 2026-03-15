#!/usr/bin/env python3
"""
Generator package: internal modules for the JUCE project generator.
Loads hyphenated-named modules and re-exports public API.
"""

import sys
from importlib.util import module_from_spec as moduleFromSpec
from importlib.util import spec_from_file_location as specFromFileLocation
from pathlib import Path

pkgDir = Path(__file__).parent


def loadModule(moduleName: str, fileName: str):
    """Load module from hyphenated filename and register in sys.modules."""
    path = pkgDir / fileName
    spec = specFromFileLocation(moduleName, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {path}")
    mod = moduleFromSpec(spec)
    sys.modules[moduleName] = mod
    runModule = spec.loader.exec_module
    runModule(mod)
    return mod


# Load in dependency order so imports resolve
loadModule("uiConstants", "ui-constants.py")
loadModule("utils", "utils.py")
loadModule("platformInfo", "platform-info.py")
loadModule("pathErrorMessages", "path-error-messages.py")
loadModule("pathValidation", "path-validation.py")
loadModule("projectConfigParser", "project-config-parser.py")
loadModule("pluginCategories", "plugin-categories.py")
loadModule("configLoader", "config-loader.py")
loadModule("projectData", "project-data.py")
loadModule("templateLoader", "template-loader.py")
loadModule("templateRenderer", "template-renderer.py")
loadModule("summaryDisplay", "summary-display.py")
loadModule("inputCollector", "input-collector.py")
loadModule("fileGenerator", "file-generator.py")
loadModule("successDisplay", "success-display.py")

# Re-export public API
from configLoader import ConfigLoader
from fileGenerator import FileGenerator
from inputCollector import InputCollector
from projectData import ProjectData
from summaryDisplay import SummaryDisplay
from successDisplay import SuccessDisplay
from templateLoader import TemplateLoader
from templateRenderer import TemplateRenderer
from utils import exitWithError
from uiConstants import Color, kHeaderWidth
