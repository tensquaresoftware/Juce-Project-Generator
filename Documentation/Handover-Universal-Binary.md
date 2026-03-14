# Passation : Support Universal Binary macOS

**Date :** 2026-03-14  
**Auteur :** Guillaume DUPONT  
**Projet :** Juce-Project-Generator  
**Objectif :** Document de passation pour l’agent IA — ajout du preset Universal Binary (Apple Silicon + Intel) pour la distribution macOS.

---

## 1. Contexte

Un plugin JUCE compilé pour Apple Silicon ne tourne pas sur Intel et vice versa. Actuellement, le générateur propose deux presets macOS distincts :

- `default-macos-arm64` → `Builds/macOS/ARM`
- `default-macos-x86_64` → `Builds/macOS/Intel`

Pour la **distribution**, un **Universal Binary** (Apple Silicon + Intel dans un seul fichier `.vst3` / `.component` / `.app`) est souvent préférable :

- Un seul fichier pour tous les Mac
- Moins de confusion pour l’utilisateur
- Pas de choix d’architecture à faire

**Inconvénients :** binaires ~2× plus gros, build plus lent.

---

## 2. État actuel

### Fichiers concernés

| Fichier | Rôle |
|---------|------|
| `templates/CMakeUserPresets.json` | Définit les presets CMake (arm64, x86_64, Windows, Linux) |
| `templates/CMakeLists.txt` | Utilise `CMAKE_OSX_ARCHITECTURES` par preset |
| `generate-new-juce-project.py` | Génère le projet, choisit preset/buildDir selon la machine |
| `configure-platform.py` | Reconfigure `.vscode` quand on ouvre le projet sur une autre plateforme |
| `templates/README.md` | Documentation des commandes de build |
| `README.md` | Documentation principale du générateur |

### Logique actuelle

- Sur macOS : `platform.machine()` → `arm64` ou `x86_64` → choix du preset et du `binaryDir`
- Pas de notion « Universal » : uniquement Apple Silicon ou Intel, jamais les deux en un seul build

---

## 3. Travail à effectuer

### 3.1 Ajouter le preset Universal dans `templates/CMakeUserPresets.json`

Ajouter un **configure preset** et un **build preset** pour `default-macos-universal` :

- **name :** `default-macos-universal`
- **displayName :** `macOS Universal (Apple Silicon + Intel)`
- **binaryDir :** `"${sourceDir}/Builds/macOS/Universal"`
- **cacheVariables :** `"CMAKE_OSX_ARCHITECTURES": "arm64;x86_64"`
- **condition :** `hostSystemName == "Darwin"` (comme les autres presets macOS)

Le preset doit être inséré entre `default-macos-x86_64` et `default-windows` pour garder une cohérence macOS → Windows → Linux.

### 3.2 Adapter `generate-new-juce-project.py`

Fonctions à modifier :

- **`getBuildDirMacOS()`** — actuellement retourne Apple Silicon ou Intel selon la machine. Pour Universal : retourner `Builds/macOS/Universal` si on souhaite que le preset par défaut soit Universal.  
  **Décision :** garder le comportement actuel (Apple Silicon sur M5, Intel sur Intel) pour le **développement** ; Universal sera un preset sélectionnable manuellement ou via un choix explicite si on ajoute une option.

- **`getPlatformBuildConfig()`** — retourne `(buildDir, presetName)` pour `.vscode/settings.json`.  
  **Décision :** ne pas changer par défaut. L’utilisateur pourra choisir `default-macos-universal` via CMake: Select Configure Preset.

- **`getPlatformInfo()`** — utilisé pour le message de succès.

- **`getBuildDirectoryName()`** — utilisé pour afficher le répertoire de build.

**Recommandation :** ne pas modifier la logique par défaut pour l’instant. Le preset Universal sera ajouté et disponible pour sélection manuelle. Si on veut une option « générer pour Universal par défaut », ce sera une évolution ultérieure.

### 3.3 Adapter `configure-platform.py`

- **`detectCurrentPlatform()`** — retourne uniquement Apple Silicon ou Intel.  
  **Option :** ajouter une détection « Universal » si demandé. Pour l’instant, on peut garder `detectCurrentPlatform()` inchangé ; on pourrait plus tard ajouter un argument `--universal` pour forcer le preset Universal.

**Recommandation :** ne pas modifier `configure-platform.py` dans la première version. L’utilisateur pourra choisir le preset Universal manuellement dans Cursor.

### 3.4 Mettre à jour la documentation

- **`templates/README.md`** : ajouter une section « macOS (Universal) » avec les commandes :

  ```bash
  cmake --preset default-macos-universal
  cmake --build --preset default-macos-universal
  ```

  Ou en mode manuel :

  ```bash
  cmake -B Builds/macOS/Universal -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_OSX_ARCHITECTURES="arm64;x86_64"
  cmake --build Builds/macOS/Universal --config Debug
  ```

- **`README.md`** : mentionner le preset `default-macos-universal` dans la section des presets macOS.

---

## 4. Spécifications techniques

### CMake : Universal Binary

```cmake
set(CMAKE_OSX_ARCHITECTURES "arm64;x86_64")
```

CMake génère alors un binaire « fat » contenant les deux architectures. Un seul `.vst3` / `.component` / `.app` fonctionne sur Apple Silicon et Intel.

### Structure des presets

L’ordre des presets dans `CMakeUserPresets.json` doit rester cohérent :

1. `default` (hidden)
2. `default-macos-arm64`
3. `default-macos-x86_64`
4. **`default-macos-universal`** ← nouveau
5. `default-windows`
6. `default-linux`

### Template CMakeUserPresets.json

Le fichier utilise `{{` et `}}` pour échapper les accolades dans le template Python. Le remplacement `{{` → `{` et `}}` → `}` est fait dans `generateCMakeUserPresets()` :

```python
content = content.replace("{{", "{").replace("}}", "}")
```

Le nouveau preset doit être inséré entre `default-macos-x86_64` et `default-windows`, en conservant la même structure de template.

---

## 5. Points d’attention

1. **Pas de `buildDirectory` dynamique pour Universal** — le générateur utilise `getBuildDirMacOS()` qui retourne Apple Silicon ou Intel. Universal a son propre `Builds/macOS/Universal`. Pas besoin de modifier cette logique si on ne change pas le preset par défaut.

2. **`.vscode/tasks.json`** — les tasks peuvent contenir des chemins `Builds/macOS/ARM` ou `Builds/macOS/Intel` (via `osx`). Si on veut une task dédiée Universal, il faudrait l’ajouter. Pour l’instant, l’utilisateur peut utiliser CMake: Build avec le preset Universal sélectionné.

3. **`.vscode/launch.json`** — les chemins Standalone pointent vers le buildDir actuel. Si l’utilisateur configure avec le preset Universal, le chemin sera `Builds/macOS/Universal/...`. `configure-platform.py` met à jour ces chemins. Pour Universal, il faudrait soit étendre `detectCurrentPlatform()` pour supporter Universal, soit laisser l’utilisateur choisir le preset manuellement (les chemins seront alors mis à jour par CMake Tools).

4. **Compatibilité** — JUCE 8 et CMake 3.22+ supportent `CMAKE_OSX_ARCHITECTURES` avec plusieurs valeurs. Aucune vérification supplémentaire n’est nécessaire.

---

## 6. Checklist de validation

- [ ] Preset `default-macos-universal` ajouté dans `templates/CMakeUserPresets.json`
- [ ] Build preset correspondant ajouté
- [ ] `templates/README.md` mis à jour avec la section Universal
- [ ] `README.md` mis à jour avec la mention du preset Universal
- [ ] Génération d’un nouveau projet et vérification que le preset Universal apparaît dans `CMake: Select Configure Preset`
- [ ] Build réussi avec le preset Universal → vérifier que le `.vst3` contient les deux architectures (`lipo -archs` sur le binaire)

---

## 7. Références

- **JUCE 8** : https://docs.juce.com
- **CMake CMAKE_OSX_ARCHITECTURES** : https://cmake.org/cmake/help/latest/variable/CMAKE_OSX_ARCHITECTURES.html
- **Vérification d’un fat binary** : `lipo -archs path/to/Plugin.vst3/Contents/MacOS/Plugin`
