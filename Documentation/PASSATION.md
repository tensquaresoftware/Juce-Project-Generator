# Passation – Juce-Project-Generator

**Date :** 2026-03-12  
**Objectif :** Préparer le prochain commit et faire le point sur l’état actuel du projet.

---

## Contexte du projet

Juce-Project-Generator est un générateur Python de projets plugin JUCE (CMake, Cursor/VS Code). Il vise à être **portable** : un projet créé sur une machine peut être cloné via GitHub sur d’autres machines (macOS, Windows, Linux) et compilé sans modifier de chemins.

---

## Modifications récentes (session 2026-03-12)

### 1. Workflow portable et `JUCE_DIR`

Le projet utilise désormais **`${env:JUCE_DIR}`** partout au lieu de chemins en dur :

- **Template `.vscode/settings.json`** : `cmake.configureSettings` et `cmake.configureEnvironment` utilisent `"JUCE_DIR": "${env:JUCE_DIR}"`
- **Template `.vscode/tasks.json`** : la tâche « CMake: Configure » passe `-DJUCE_DIR=${env:JUCE_DIR}` pour les plateformes `windows`, `osx` et `linux`
- **Suppression de l’injection de chemin** : la logique `getJuceDirConfigureSettings()` et l’écriture de chemins depuis `user-config.py` dans les projets générés ont été retirées. Les `JUCE_DIR_*` de `user-config.py` ne servent plus qu’à la validation.

### 2. Support Linux dans les tâches

- Ajout de l’override **`linux`** pour la tâche « CMake: Configure » (Ninja, `Builds/Linux`)
- Ajout des overrides **`linux`** pour « Build: Standalone », « Build: VST3 » et « Build: All »

### 3. Script `configure-platform.py`

- Prise en charge du bloc **`linux`** dans `updateTasksJson()` pour les tâches Linux
- Mise à jour des chemins et arguments pour la plateforme Linux

### 4. Documentation (README.md)

- Version passée à **1.0.3** puis **1.0.4**
- Nouvelle section **« Portable workflow (GitHub, multi-machine) »**
- Clarification du rôle de `JUCE_DIR_*` (validation uniquement)
- Mise à jour des prérequis et de la section « JUCE not found »
- Instructions pour définir `JUCE_DIR` par plateforme (macOS, Windows, Linux)

### 5. Copie VST3 sur toutes les plateformes (v1.0.4)

- **user-config.py** : ajout de `CUSTOM_VST3_FOLDER_MACOS` et `CUSTOM_VST3_FOLDER_LINUX` (en plus de `CUSTOM_VST3_FOLDER_WINDOWS`)
- **generate-new-juce-project.py** : `loadCustomVst3Folder()` remplacé par trois loaders (`loadCustomVst3FolderWindows`, `loadCustomVst3FolderMacOS`, `loadCustomVst3FolderLinux`) ; passage de `customVst3FolderWindows`, `customVst3FolderMacOS`, `customVst3FolderLinux` au template
- **templates/CMakeLists.txt** : la copie automatique du VST3 après build s’applique à **toutes les plateformes** (Windows, macOS, Linux), avec un chemin par défaut par plateforme
- **README.md** : doc des trois options VST3, section « Testing Plugins » complétée pour Linux, version 1.0.4

---

## Fichiers modifiés (pour le commit)

| Fichier | Type de modification |
|---------|----------------------|
| `templates/.vscode/settings.json` | Utilisation de `${env:JUCE_DIR}`, suppression de `{juceDirConfigureSettings}` |
| `templates/.vscode/tasks.json` | Overrides `linux` + `-DJUCE_DIR=${env:JUCE_DIR}` pour toutes les plateformes |
| `templates/CMakeLists.txt` | Copie VST3 sur toutes les plateformes (chemins Windows / macOS / Linux) |
| `generate-new-juce-project.py` | Suppression de `getJuceDirConfigureSettings()` ; trois loaders VST3 ; passage des trois chemins au template |
| `configure-platform.py` | Prise en charge du bloc `linux` dans `updateTasksJson()` |
| `user-config.py` | Ajout de `CUSTOM_VST3_FOLDER_MACOS` et `CUSTOM_VST3_FOLDER_LINUX` |
| `README.md` | Portable workflow, VST3 toutes plateformes, version 1.0.4, Testing Plugins Linux |
| `PASSATION.md` | Ce fichier (peut être supprimé ou conservé selon convention) |

---

## Projet de test associé

Le projet **Test-UbuntuPlugin** (`/home/guillaume/Desktop/Test-UbuntuPlugin`) doit être **régénéré** avec le générateur pour bénéficier de toutes les évolutions (workflow portable avec `${env:JUCE_DIR}`, copie VST3 sur Linux/macOS/Windows, tâches Linux complètes). Après régénération, il servira à valider le workflow sur Linux.

---

## À faire avant le commit

1. Vérifier que tous les changements sont cohérents
2. **Régénérer Test-UbuntuPlugin** avec le générateur (pour appliquer VST3 multi-plateformes et workflow portable)
3. Tester build + copie VST3 sur Linux (dossier défini dans `CUSTOM_VST3_FOLDER_LINUX`)
4. Décider si `PASSATION.md` doit être versionné ou rester local

---

## Notes pour l’agent IA

- Le générateur s’appuie sur `user-config.py` pour la validation des chemins JUCE et pour les chemins VST3 par plateforme
- Aucun chemin JUCE ne doit être écrit dans les projets générés ; tout passe par `JUCE_DIR` en variable d’environnement
- La copie VST3 après build est configurée pour les trois plateformes via `CUSTOM_VST3_FOLDER_WINDOWS`, `CUSTOM_VST3_FOLDER_MACOS`, `CUSTOM_VST3_FOLDER_LINUX`
- La documentation indique que l’utilisateur doit définir `JUCE_DIR` sur chaque machine (macOS, Windows, Linux)
- Les règles du projet (.cursorrules) imposent des commits en anglais et le respect des conventions de nommage (voir `.cursorrules`)
