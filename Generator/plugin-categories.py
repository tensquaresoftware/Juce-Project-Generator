#!/usr/bin/env python3
"""
PluginCategories: derives AU/VST3 categories and bundle ID from plugin settings.
Single responsibility: plugin type to category mapping.
"""

import re


def generateBundleId(manufacturerName: str, projectName: str) -> str:
    """Generate reverse-DNS bundle ID from manufacturer and project name."""
    manufacturerId = re.sub(r'[^a-zA-Z0-9]', '', manufacturerName)
    if manufacturerId and not manufacturerId[0].isalpha():
        manufacturerId = "Company" + manufacturerId
    projectId = re.sub(r'[^a-zA-Z0-9_-]', '', projectName)
    return f"com.{manufacturerId}.{projectId}"


def getPluginTypeDisplayName(isSynth: str, isMidiEffect: str) -> str:
    """Return human-readable plugin type for summary."""
    if isSynth == "TRUE":
        return "Synthesizer"
    if isMidiEffect == "TRUE":
        return "MIDI Effect"
    return "Audio Effect"


def updateAuAndVst3Categories(isSynth: str, isMidiEffect: str) -> tuple:
    """Return (auMainType, vst3Categories) based on plugin type."""
    if isSynth == "TRUE":
        return "kAudioUnitType_MusicDevice", "Instrument|Synth"
    if isMidiEffect == "TRUE":
        return "kAudioUnitType_MIDIProcessor", "Fx|MIDI"
    return "kAudioUnitType_Effect", "Fx"
