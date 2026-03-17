---
name: Refonte copie artefacts
overview: "Refondre le système de copie des artefacts du générateur JUCE : supprimer la copie vers project_root/Artefacts/, activer la copie vers les dossiers système sur Windows et Linux, et ajouter la copie vers un dossier central custom par OS (chemins injectés à la génération)."
todos: []
isProject: false
---

# Plan d'action : refonte copie des artefacts

Référence : [Documentation/Plan-Refonte-Copie-Artefacts.md](Documentation/Plan-Refonte-Copie-Artefacts.md).

---

## Contexte

- **À supprimer** : copie vers `project_root/Artefacts/` (COPY_TO_PROJECT_FOLDERS).
- **À étendre** : copie vers dossiers système actuellement uniquement sur macOS → activer aussi Windows et Linux (COPY_TO_SYSTEM_FOLDERS).
- **À ajouter** : copie vers un **dossier central custom** par OS (ARTEFACTS_DIR_*), chemins définis dans `generator-configuration.py` et injectés dans le projet à la génération.

Nommage retenu : **DIR** pour les chemins (ARTEFACTS_DIR_*), **FOLDERS** pour les options (COPY_TO_SYSTEM_FOLDERS, COPY_TO_ARTEFACTS_DIR).

---

## Phase 1 : Dossiers système (Windows, Linux)

**Objectif** : COPY_TO_SYSTEM_FOLDERS appliqué aux 3 OS (aujourd’hui seul macOS utilise COPY_PLUGIN_AFTER_BUILD).

1. **Vérifier JUCE**
  Confirmer dans la doc JUCE que `COPY_PLUGIN_AFTER_BUILD` sous Windows copie bien vers `%LOCALAPPDATA%\Programs\Common\VST3\` et sous Linux vers `~/.vst3/`. Si ce n’est pas le cas, prévoir une copie manuelle post-build dans [Templates/CMakeLists.txt](Templates/CMakeLists.txt).
2. **Activer la copie système sur Windows et Linux**
  Dans [Templates/CMakeLists.txt](Templates/CMakeLists.txt) (vers lignes 102–108), remplacer la logique actuelle :
  - Actuellement : `COPY_PLUGIN_AFTER_BUILD_VALUE` = COPY_TO_SYSTEM_FOLDERS seulement si `APPLE`, sinon `FALSE`.
  - Nouveau : utiliser `COPY_TO_SYSTEM_FOLDERS` pour les 3 OS (APPLE, WIN32, Linux) pour définir `COPY_PLUGIN_AFTER_BUILD_VALUE`.
3. **Documentation project-config**
  Dans [Templates/project-config.cmake](Templates/project-config.cmake) et [project-config.cmake](project-config.cmake) (racine), mettre à jour les commentaires de COPY_TO_SYSTEM_FOLDERS pour préciser qu’elle s’applique aux 3 OS (macOS : AU + VST3 ; Windows : VST3 ; Linux : VST3), avec les chemins user indiqués dans le plan (section 3.1).

---

## Phase 2 : Suppression copie projet + Dossier central

### 2.1 Configuration générateur

**Fichier** : [generator-configuration.py](generator-configuration.py)

- **Ajouter** (avec commentaires sur interdiction des accents) :
  - `ARTEFACTS_DIR_WINDOWS`, `ARTEFACTS_DIR_MACOS`, `ARTEFACTS_DIR_LINUX` (ex. `C:/Users/Guillaume/Dev/JUCE/Artefacts`, etc.).
  - `DEFAULT_PROJECT_DIR_WINDOWS`, `DEFAULT_PROJECT_DIR_MACOS`, `DEFAULT_PROJECT_DIR_LINUX` (ex. `C:/Users/Guillaume/Dev/JUCE/Projects`, etc.).
- **Supprimer** : `DEFAULT_PROJECT_DESTINATION`.
- **Conserver** : JUCE_DIR_*, section manufacturer.

### 2.2 Config-loader

**Fichier** : [Generator/config-loader.py](Generator/config-loader.py)

- `**_loadDestination()`** : au lieu de `DEFAULT_PROJECT_DESTINATION`, utiliser `DEFAULT_PROJECT_DIR_WINDOWS` / `DEFAULT_PROJECT_DIR_MACOS` / `DEFAULT_PROJECT_DIR_LINUX` selon `platform.system()`. Conserver le fallback Desktop et la validation `validatePathNoProblematicChars` (avec le nom de l’attribut concerné).
- **Remplacer** `_loadCopyToProjectFolders()` par `**_loadCopyToArtefactsDir()`** : lire `USER_COPY_TO_ARTEFACTS_DIR` / `COPY_TO_ARTEFACTS_DIR` depuis project-config (default ON ou OFF selon le plan).
- **Ajouter** `**_loadArtefactsDirs()`** : retourner un dict `{"windows": ..., "macos": ..., "linux": ...}` depuis les constantes `ARTEFACTS_DIR_*` du module de config, avec validation `validatePathNoProblematicChars` pour chaque chemin.
- `**loadAll()`** : exposer `destination` (inchangé en clé), `copyToArtefactsDir` (remplace copyToProjectFolders), et `artefactsDirWindows`, `artefactsDirMacos`, `artefactsDirLinux` (ou un seul champ `artefactsDirs` dict selon ce qu’attend le template-renderer).

### 2.3 Template-renderer

**Fichier** : [Generator/template-renderer.py](Generator/template-renderer.py)

- Remplacer `copyToProjectFolders` par `**copyToArtefactsDir`** dans le contexte de rendu.
- Ajouter `**artefactsDirWindows`**, `**artefactsDirMacos`**, `**artefactsDirLinux**` au contexte (valeurs issues de `config` fourni par config-loader).

### 2.4 project-config.cmake (template et source)

**Fichiers** : [Templates/project-config.cmake](Templates/project-config.cmake), [project-config.cmake](project-config.cmake)

- **Supprimer** : `USER_COPY_TO_PROJECT_FOLDERS`, `COPY_TO_PROJECT_FOLDERS`, et toute référence à la copie vers le projet.
- **Ajouter** :
  - Option **COPY_TO_ARTEFACTS_DIR** (ON/OFF) : copie vers le dossier central custom (chemins par OS).
  - Variables injectées à la génération : **ARTEFACTS_DIR_WINDOWS**, **ARTEFACTS_DIR_MACOS**, **ARTEFACTS_DIR_LINUX** (lues depuis generator-configuration via config-loader, écrites dans le template rendu).
- Conserver **COPY_TO_SYSTEM_FOLDERS** (déjà documentée pour les 3 OS après phase 1).
- Dans le **template** : placeholders du type `{artefactsDirWindows}`, `{artefactsDirMacos}`, `{artefactsDirLinux}` et `{copyToArtefactsDir}` pour l’injection.

### 2.5 CMakeLists.txt (template)

**Fichier** : [Templates/CMakeLists.txt](Templates/CMakeLists.txt)

- **Supprimer** tout le bloc actuel « COPY TO ARTEFACTS FOLDER » (lignes ~148–254) : `PROJECT_ARTEFACTS_BASE`, `COPY_TO_PROJECT_FOLDERS`, custom target CopyArtefacts vers `PROJECT_ARTEFACTS_PLATFORM`, etc.
- **Ajouter** un nouveau bloc **COPY_TO_ARTEFACTS_DIR** :
  - Lire les variables injectées `ARTEFACTS_DIR_WINDOWS`, `ARTEFACTS_DIR_MACOS`, `ARTEFACTS_DIR_LINUX` (déjà présentes dans project-config.cmake inclus).
  - Déterminer **ARTEFACTS_DIR** selon `CMAKE_HOST_SYSTEM_NAME` (ou équivalent) et, sous macOS, sous-dossier d’arch (ARM, Intel, Intel-Rosetta, Universal) comme aujourd’hui avec `HOST_ARCH` et `CMAKE_OSX_ARCHITECTURES`.
  - Structure de destination conforme au plan (section 3.2) : par OS puis par arch (macOS) puis VST3/, AU/ (macOS), Standalone/, et prévoir CLAP/ pour Linux (futur).
  - Créer un custom target (ex. CopyToArtefactsDir) qui copie les binaires générés (VST3, AU si macOS, Standalone) vers ce dossier central.

Réutiliser la logique existante de détection macOS (ARM / Intel / Intel-Rosetta / Universal) pour le sous-dossier sous `ARTEFACTS_DIR_MACOS`.

### 2.6 Project-config-parser (si nécessaire)

**Fichier** : [Generator/project-config-parser.py](Generator/project-config-parser.py)

- Si le parser lit `USER_COPY_TO_PROJECT_FOLDERS` / `COPY_TO_PROJECT_FOLDERS` dans project-config.cmake à la racine (pour les défauts du générateur), le faire évoluer pour **USER_COPY_TO_ARTEFACTS_DIR** / **COPY_TO_ARTEFACTS_DIR**. Vérifier aussi que le template généré n’expose que les variables attendues (COPY_TO_SYSTEM_FOLDERS, COPY_TO_ARTEFACTS_DIR, ARTEFACTS_DIR_*).

---

## Phase 3 : Documentation et nettoyage

- **README.md** : décrire la nouvelle logique (dossiers système + dossier central), supprimer toute référence à `Artefacts/` du projet et aux options supprimées. Documenter les chemins par OS (section 3.1 et 3.2 du plan).
- **Templates/README.md** : idem (destinations de copie, structure du dossier central).
- **Documentation/Guide-Tests-Generateur.md** : adapter les cas de test (plus de dossier Artefacts dans le projet ; vérifier dossiers système et dossier central selon OS/arch).
- **Templates/.gitignore** : supprimer l’entrée `Artefacts/` (optionnelle si le dossier n’est plus créé).
- **Racine project-config.cmake** : aligner sur le nouveau template (options et commentaires).

---

## Points d’attention

- **Validation** : tous les chemins `ARTEFACTS_DIR`_* et `DEFAULT_PROJECT_DIR_`* doivent passer par `validatePathNoProblematicChars` (comme aujourd’hui pour DEFAULT_PROJECT_DESTINATION).
- **Projets existants** : les projets déjà générés conservent l’ancienne logique ; documenter en une phrase la migration (régénérer ou éditer project-config.cmake manuellement).
- **CLAP** : prévoir la structure `ARTEFACTS_DIR_LINUX/CLAP/` dans le CMake (dossier créé si besoin) même si le format n’est pas encore supporté par le générateur.
- **Portabilité** : rappeler dans la doc que les chemins sont injectés à la génération ; sur une autre machine, éditer `project-configuration.cmake` du projet ou régénérer avec une `generator-configuration.py` locale.

---

## Ordre d’exécution recommandé

1. Phase 1 (dossiers système Windows/Linux + doc project-config).
2. Phase 2.1–2.4 (config + loader + renderer + project-configuration template/source + renommage).
3. Phase 2.5 (CMakeLists : suppression projet + nouveau bloc dossier central).
4. Phase 2.6 (renommage project-config → project-configuration + ajustements parser).
5. Phase 3 (docs + .gitignore + tests).

