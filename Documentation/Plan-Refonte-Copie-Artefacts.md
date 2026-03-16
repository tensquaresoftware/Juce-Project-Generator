# Plan de refonte : copie des artefacts post-build

**Document de référence pour l’implémentation** — à présenter à l’agent IA pour prise en charge sur Mac M5.

---

## 1. Contexte et vision

Le générateur JUCE actuel a été testé sur 3 machines (Mac M5/macOS Tahoe, Mac Intel/Windows 11, PC Dell/Ubuntu) via clonage GitHub. Le système de copie des artefacts actuel ne correspond plus à l’usage souhaité.

### Objectifs initiaux pour les utilisateurs

1. Créer rapidement un projet JUCE à partir du générateur
2. Compiler le projet sans effort sous n’importe quel OS et architecture (macOS ARM/Intel/Rosetta/Universal, Windows, Linux), via IDE ou Terminal, avec une configuration CMake adaptée
3. **Copier automatiquement les plugins (AU, VST3, CLAP selon le cas) vers les dossiers système** où les DAW cherchent par défaut
4. **Copier automatiquement les plugins et Standalone vers un dossier central custom du développeur** (un chemin par OS), pour faciliter les tests en pointant les DAW vers ce dossier unique, et retrouver facilement les exécutables Standalone

### Constat actuel

- La copie vers `Artefacts/` du projet est jugée maladroite et ne sera **pas conservée**
- La copie vers les dossiers système n’est implémentée que sur **macOS**
- La copie vers un dossier central custom n’est **pas implémentée**

---

## 2. Décisions prises

| Décision | Choix |
|----------|-------|
| Source du chemin du dossier central | **Valeurs injectées à la génération** (pas d’env vars). L’utilisateur modifie une string dans un fichier de config. |
| Copie vers le dossier du projet | **Supprimée** — ne plus copier vers `project_root/Artefacts/` |
| Ordre d’implémentation | **1.** Dossiers système (Windows, Linux) — **2.** Dossier central custom |
| Nommage | **DIR** pour les chemins (ex. `ARTEFACTS_DIR_WINDOWS`), **FOLDERS** pour les cibles de copie (ex. `COPY_TO_SYSTEM_FOLDERS`) |

---

## 3. Structure des destinations par OS

### 3.1 Dossiers système (où les DAW cherchent par défaut)

| OS | Format | Chemin système (user) | Chemin système (global) |
|----|--------|----------------------|-------------------------|
| **macOS** | AU | `~/Library/Audio/Plug-Ins/Components/` | `/Library/Audio/Plug-Ins/Components/` |
| **macOS** | VST3 | `~/Library/Audio/Plug-Ins/VST3/` | `/Library/Audio/Plug-Ins/VST3/` |
| **Windows** | VST3 | `%LOCALAPPDATA%\Programs\Common\VST3\` | `C:\Program Files\Common Files\VST3\` |
| **Linux** | VST3 | `~/.vst3/` | `/usr/local/lib/vst3/` |
| **Linux** | CLAP | `~/.clap` (convention courante) | (à définir) |

**Recommandation pour le dev** : utiliser les chemins **user** (pas besoin de droits admin).

- Windows user : `C:\Users\<user>\AppData\Local\Programs\Common\VST3`
- Linux user : `~/.vst3/`

### 3.2 Dossier central custom (structure)

Le chemin de base est défini par OS dans `generator-configuration.py`, puis injecté dans le projet. Structure sous ce chemin :

**Windows :**
```
ARTEFACTS_DIR_WINDOWS/
├── VST3/
│   └── MyPlugin.vst3
└── Standalone/
    └── MyPlugin.exe
```

**macOS :**
```
ARTEFACTS_DIR_MACOS/
├── ARM/
│   ├── AU/
│   │   └── MyPlugin.component
│   ├── VST3/
│   │   └── MyPlugin.vst3
│   └── Standalone/
│       └── MyPlugin.app
├── Intel/
│   ├── AU/
│   ├── VST3/
│   └── Standalone/
├── Intel-Rosetta/
│   ├── AU/
│   ├── VST3/
│   └── Standalone/
└── Universal/
    ├── AU/
    ├── VST3/
    └── Standalone/
```

**Linux :**
```
ARTEFACTS_DIR_LINUX/
├── VST3/
│   └── MyPlugin.vst3
├── CLAP/          # futur
│   └── MyPlugin.clap
└── Standalone/
    └── MyPlugin
```

---

## 4. Modifications à apporter

### 4.1 `generator-configuration.py`

**Nouvelles constantes :**

```python
# Dossier central custom : tous les plugins et Standalone de tous les projets
# L'utilisateur modifie ces chemins selon sa machine.
# Injectés à la génération dans project-config.cmake.
ARTEFACTS_DIR_WINDOWS = "C:/Users/Guillaume/Dev/JUCE/Artefacts"
ARTEFACTS_DIR_MACOS   = "/Volumes/Guillaume/Dev/JUCE/Artefacts"
ARTEFACTS_DIR_LINUX   = "/home/guillaume/Dev/JUCE/Artefacts"

# Destination par défaut des projets créés (remplace DEFAULT_PROJECT_DESTINATION)
DEFAULT_PROJECT_DIR_WINDOWS = "C:/Users/Guillaume/Dev/JUCE/Projects"
DEFAULT_PROJECT_DIR_MACOS   = "/Volumes/Guillaume/Dev/JUCE/Projects"
DEFAULT_PROJECT_DIR_LINUX   = "/home/guillaume/Dev/JUCE/Projects"
```

**À supprimer :**
- `DEFAULT_PROJECT_DESTINATION`

**À conserver :**
- `JUCE_DIR_WINDOWS`, `JUCE_DIR_MACOS`, `JUCE_DIR_LINUX` (inchangés)
- Section manufacturer (inchangée)

### 4.2 `project-config.cmake` (template et fichier source)

**Nouvelles options :**

```cmake
# COPY_TO_SYSTEM_FOLDERS: ON/OFF
#   When ON: copies plugins to system folders where DAWs look by default.
#   - macOS: AU → ~/Library/Audio/Plug-Ins/Components/, VST3 → ~/Library/Audio/Plug-Ins/VST3/
#   - Windows: VST3 → %LOCALAPPDATA%\Programs\Common\VST3\
#   - Linux: VST3 → ~/.vst3/

# COPY_TO_ARTEFACTS_DIR: ON/OFF
#   When ON: copies plugins and Standalone to the central custom folder (path per OS).
#   Paths are defined below and injected at project generation.
```

**À supprimer :**
- `USER_COPY_TO_PROJECT_FOLDERS` / `COPY_TO_PROJECT_FOLDERS`

**Variables injectées (depuis generator-configuration.py) :**
- `ARTEFACTS_DIR_WINDOWS`
- `ARTEFACTS_DIR_MACOS`
- `ARTEFACTS_DIR_LINUX`

Le projet choisit le bon chemin selon `CMAKE_HOST_SYSTEM_NAME` ou équivalent.

### 4.3 `templates/CMakeLists.txt`

**Phase 1 — Dossiers système :**

- Activer `COPY_PLUGIN_AFTER_BUILD` pour **Windows** et **Linux** (actuellement `FALSE` pour tout sauf macOS).
- JUCE gère déjà la copie vers les dossiers système via `COPY_PLUGIN_AFTER_BUILD`. Vérifier si JUCE utilise bien les chemins user sous Windows/Linux, ou si une copie manuelle post-build est nécessaire.

**Note :** Sous Windows, `COPY_PLUGIN_AFTER_BUILD` de JUCE copie vers `%LOCALAPPDATA%\Programs\Common\VST3\`. Sous Linux, vers `~/.vst3/`. À confirmer dans la doc JUCE.

**Phase 2 — Dossier central :**

- Supprimer toute la logique `COPY_TO_PROJECT_FOLDERS` et `PROJECT_ARTEFACTS_BASE` (lignes ~148–254).
- Ajouter une nouvelle logique `COPY_TO_ARTEFACTS_DIR` :
  - Déterminer `ARTEFACTS_DIR` selon la plateforme (Windows/Mac/Linux) et l’architecture (macOS : ARM/Intel/Intel-Rosetta/Universal).
  - Créer un custom target qui copie VST3, AU (macOS), Standalone vers la structure décrite en 3.2.

### 4.4 `Generator/config-loader.py`

- Remplacer `_loadDestination()` : utiliser `DEFAULT_PROJECT_DIR_WINDOWS`, `DEFAULT_PROJECT_DIR_MACOS`, `DEFAULT_PROJECT_DIR_LINUX` selon `platform.system()`.
- Remplacer `_loadCopyToProjectFolders()` par `_loadCopyToArtefactsDir()`.
- Ajouter `_loadArtefactsDirs()` : retourner un dict `{ "windows": ..., "macos": ..., "linux": ... }` pour injection dans le template.
- Mettre à jour `loadAll()` pour exposer ces nouvelles valeurs.

### 4.5 `Generator/template-renderer.py`

- Remplacer `copyToProjectFolders` par `copyToArtefactsDir`.
- Ajouter `artefactsDirWindows`, `artefactsDirMacos`, `artefactsDirLinux` au contexte de rendu.
- Adapter `_buildFormatContext()` en conséquence.

### 4.6 `Generator/input-collector.py`

- `config["destination"]` vient déjà du config-loader ; si la destination est maintenant par OS, aucune modification majeure si le loader renvoie le bon chemin selon la plateforme.

### 4.7 Fichiers à mettre à jour (documentation, .gitignore)

- `README.md` : décrire la nouvelle logique (dossiers système + dossier central), supprimer les références à `Artefacts/` du projet.
- `templates/README.md` : idem.
- `Documentation/Guide-Tests-Generateur.md` : adapter les tests pour la nouvelle structure.
- `templates/.gitignore` : supprimer `Artefacts/` (ce dossier n’existe plus dans le projet).
- `project-config.cmake` (à la racine du générateur) : aligner sur le nouveau template.

---

## 5. Ordre d’implémentation recommandé

### Phase 1 : Dossiers système (Windows, Linux)

1. Étudier le comportement de `COPY_PLUGIN_AFTER_BUILD` de JUCE sous Windows et Linux (chemins exacts).
2. Modifier `templates/CMakeLists.txt` pour activer `COPY_PLUGIN_AFTER_BUILD` sur Windows et Linux quand `COPY_TO_SYSTEM_FOLDERS` est ON.
3. Mettre à jour `project-config.cmake` (template et source) : commentaires pour indiquer que l’option s’applique aux 3 OS.

### Phase 2 : Suppression de la copie projet + Dossier central

1. Supprimer `COPY_TO_PROJECT_FOLDERS` et toute la logique associée dans `CMakeLists.txt`.
2. Ajouter `ARTEFACTS_DIR_*` dans `generator-configuration.py`.
3. Ajouter `DEFAULT_PROJECT_DIR_*` dans `generator-configuration.py`, supprimer `DEFAULT_PROJECT_DESTINATION`.
4. Modifier `project-config.cmake` : `USER_COPY_TO_ARTEFACTS_DIR`, injection des chemins `ARTEFACTS_DIR_*`.
5. Modifier `config-loader.py` : charger les nouveaux chemins et flags.
6. Modifier `template-renderer.py` : injecter les nouvelles variables.
7. Implémenter la logique CMake pour copier vers le dossier central (structure par OS/arch).
8. Mettre à jour la documentation et les tests.

### Phase 3 : Homogénéisation et nettoyage

1. Vérifier la cohérence du nommage (DIR vs FOLDERS).
2. Mettre à jour tous les fichiers mentionnés en 4.7.
3. Tester sur les 3 OS.

---

## 6. Fichiers impactés (résumé)

| Fichier | Modifications |
|---------|---------------|
| `generator-configuration.py` | Nouveaux chemins ARTEFACTS_DIR_*, DEFAULT_PROJECT_DIR_* |
| `project-config.cmake` | Nouveau template, suppression COPY_TO_PROJECT_FOLDERS |
| `templates/project-config.cmake` | Idem + placeholders pour injection |
| `templates/CMakeLists.txt` | Dossiers système (phase 1), dossier central (phase 2), suppression projet |
| `Generator/config-loader.py` | Destination par OS, artefacts dirs, copyToArtefactsDir |
| `Generator/template-renderer.py` | Contexte copyToArtefactsDir + artefactsDir* |
| `README.md` | Nouvelle doc |
| `templates/README.md` | Nouvelle doc |
| `Documentation/Guide-Tests-Generateur.md` | Tests adaptés |
| `templates/.gitignore` | Supprimer Artefacts/ |

---

## 7. Points d’attention

- **Validation des chemins** : s’assurer que `ARTEFACTS_DIR_*` et `DEFAULT_PROJECT_DIR_*` passent par `validatePathNoProblematicChars` (pas d’accents, etc.).
- **Projets existants** : les projets déjà générés garderont l’ancienne logique tant qu’ils ne sont pas régénérés. Documenter la migration si nécessaire.
- **CLAP** : le format CLAP n’est pas encore supporté par le générateur. Prévoir la structure `ARTEFACTS_DIR_LINUX/CLAP/` pour une future évolution.
- **Portabilité** : les chemins sont injectés à la génération. Sur une machine différente (ex. clone GitHub), l’utilisateur devra éditer `project-config.cmake` du projet pour adapter `ARTEFACTS_DIR_*` à son environnement, ou régénérer le projet avec sa propre `generator-configuration.py`.

---

*Document créé le 16 mars 2025 — Plan de refonte copie artefacts JUCE Project Generator*
