# Générateur de projets JUCE / Guide de tests complets

**Auteur :** Guillaume DUPONT  
**Organisation :** Ten Square Software  
**Date :** 2026-03-15

---

## Objectif

Ce document sert de checklist pour valider le bon fonctionnement du générateur de projets JUCE dans toutes les configurations. Il couvre les tests de génération, de build, de copie des artefacts et les cas limites.

---

## 1. Prérequis avant les tests

- [ ] Python 3.7+ installé
- [ ] JUCE 8 installé et `JUCE_DIR` défini dans l'environnement
- [ ] CMake 3.22+ installé
- [ ] Ninja installé (macOS/Linux)
- [ ] Cursor ou VS Code avec extension CMake Tools
- [ ] `generator-configuration.py` et `project-configuration.cmake` présents (ou utilisation des valeurs par défaut)

---

## 2. Tests de génération – Noms et caractères

### 2.1 Nom technique du projet

Le nom technique doit commencer par une lettre et contenir uniquement lettres, chiffres, tirets et underscores.

| Testé | Test                         | Valeur saisie          | Résultat attendu      |
| ----- | ---------------------------- | ---------------------- | --------------------- |
| [ ]   | Nom valide simple            | `MyPlugin`             | ✅ Accepté             |
| [ ]   | Nom avec underscore          | `My_Plugin_v2`         | ✅ Accepté             |
| [ ]   | Nom avec tiret               | `My-Plugin`            | ✅ Accepté             |
| [ ]   | Nom commençant par chiffre   | `1Plugin`              | ❌ Refusé              |
| [ ]   | Nom avec espace              | `My Plugin`            | ❌ Refusé              |
| [ ]   | Nom avec caractères spéciaux | `MyPlugin@`            | ❌ Refusé              |
| [ ]   | Nom avec accents             | `MonPlugin` (si é/è/à) | ❌ Refusé              |
| [ ]   | Nom vide (défaut)            | *Entrée vide*          | ✅ Utilise `NewPlugin` |


### 2.2 Nom d'affichage (Display name)

Caractères autorisés : lettres, chiffres, espaces, tirets, underscores uniquement.

| Testé | Test                     | Valeur saisie          | Résultat attendu           |
| ----- | ------------------------ | ---------------------- | -------------------------- |
| [ ]   | Nom simple               | `My Plugin`            | ✅ Accepté                  |
| [ ]   | Nom long descriptif      | `Super Synth Pro 2024` | ✅ Accepté                  |
| [ ]   | Avec tirets/underscores  | `My-Plugin_v2`         | ✅ Accepté                  |
| [ ]   | Avec accents             | `Synthé Élégant`       | ❌ Refusé                   |
| [ ]   | Avec caractères spéciaux | `Plugin™` ou `Plugin®` | ❌ Refusé                   |
| [ ]   | Avec apostrophe          | `Dave's Synth`         | ❌ Refusé                   |
| [ ]   | Vide (défaut)            | *Entrée vide*          | ✅ Utilise le nom technique |


### 2.3 Dossier de destination

Les chemins ne doivent **pas** contenir de caractères accentués ni de caractères Unicode non-ASCII.

| Testé | Test                             | Chemin                                 | Résultat attendu   |
| ----- | -------------------------------- | -------------------------------------- | ------------------ |
| [ ]   | Chemin valide                    | `~/Desktop` ou `C:/Users/John/Desktop` | ✅ Accepté          |
| [ ]   | Chemin avec accents              | `C:/Users/John/Téléchargements`        | ❌ Erreur explicite |
| [ ]   | Chemin avec accents              | `D:/Projets/Été 2024`                  | ❌ Erreur explicite |
| [ ]   | Chemin avec espace (sans accent) | `C:/Users/John/My Projects`            | ✅ Accepté          |
| [ ]   | Chemin `Default`                 | *Entrée vide*                          | ✅ Bureau système   |


### 2.4 Codes fabricant et plugin

| Testé | Test                          | Manufacturer Code  | Plugin Code         | Résultat attendu |
| ----- | ----------------------------- | ------------------ | ------------------- | ---------------- |
| [ ]   | Valides                       | `Myco` (4 lettres) | `Plg1` (4 alphanum) | ✅ Accepté        |
| [ ]   | Manufacturer trop court       | `Myc`              | —                   | ❌ Refusé         |
| [ ]   | Manufacturer avec chiffre     | `Myc1`             | —                   | ❌ Refusé         |
| [ ]   | Plugin trop long              | —                  | `Plg12`             | ❌ Refusé         |
| [ ]   | Plugin avec caractère spécial | —                  | `Plg@`              | ❌ Refusé         |


---

## 3. Tests de génération – Structure du projet

### 3.1 Fichiers et dossiers générés

Après génération, vérifier la présence de :

- [ ] `CMakeLists.txt`
- [ ] `CMakeUserPresets.json`
- [ ] `project-configuration.cmake`
- [ ] `configure-platform.py`
- [ ] `Source/PluginProcessor.h`
- [ ] `Source/PluginProcessor.cpp`
- [ ] `Source/PluginEditor.h`
- [ ] `Source/PluginEditor.cpp`
- [ ] `Source/PluginFactory.cpp`
- [ ] `.vscode/settings.json`
- [ ] `.vscode/tasks.json`
- [ ] `.vscode/launch.json`
- [ ] `.cursorrules`
- [ ] `.gitignore`
- [ ] `README.md`
- [ ] Dossiers `Builds/macOS/`, `Builds/Windows/`, `Builds/Linux/` (vides au départ)

### 3.2 Substitution des variables

Ouvrir les fichiers générés et vérifier que les placeholders ont été remplacés :

- [ ] `{projectName}` → nom technique du projet
- [ ] `{projectDisplayName}` → nom d'affichage
- [ ] `{projectVersion}` → version
- [ ] `{manufacturerName}` → nom du fabricant
- [ ] `{manufacturerCode}` → code fabricant (4 lettres)
- [ ] `{pluginCode}` → code plugin (4 alphanum)
- [ ] `{bundleId}` → identifiant bundle (ex. `com.mycompany.myplugin`)
- [ ] `{pluginFormats}` → formats sélectionnés (AU, VST3, Standalone)
- [ ] `{copyToSystemFolders}` / `{copyToProjectFolders}` → ON ou OFF

---

## 4. Tests des configurations CMake (presets)

### 4.1 Noms des presets affichés

Ouvrir le projet dans Cursor, sélectionner « CMake: Select Configure Preset » et vérifier les libellés :

| Testé | Plateforme          | Display name attendu                                  |
| ----- | ------------------- | ----------------------------------------------------- |
| [ ]   | macOS Apple Silicon | macOS Apple Silicon (Ninja) - Native on Apple Silicon |
| [ ]   | macOS Intel         | macOS Intel (Ninja) - Native on Mac Intel             |
| [ ]   | macOS Intel-Rosetta | macOS Intel-Rosetta (Ninja) - x86_64 on Apple Silicon |
| [ ]   | macOS Universal     | macOS Universal (Ninja) - Apple Silicon + Intel        |
| [ ]   | Windows             | Windows x64 (Visual Studio 2022) - Native on x64      |
| [ ]   | Linux               | Linux x64 (Ninja) - Native on x86_64                  |


### 4.2 Dossiers de build par preset

| Testé | Preset              | Dossier de build attendu      |
| ----- | ------------------- | ----------------------------- |
| [ ]   | macOS Apple Silicon | `Builds/macOS/ARM/`           |
| [ ]   | macOS Intel         | `Builds/macOS/Intel/`         |
| [ ]   | macOS Intel-Rosetta | `Builds/macOS/Intel-Rosetta/` |
| [ ]   | macOS Universal     | `Builds/macOS/Universal/`     |
| [ ]   | Windows             | `Builds/Windows/`              |
| [ ]   | Linux               | `Builds/Linux/`               |

### 4.3 Preset refusé selon la machine (CMake)

Le projet généré refuse à la configuration un preset inadapté à la machine :

| Testé | Machine      | Preset à sélectionner        | Comportement attendu |
| ----- | ------------ | ---------------------------- | -------------------- |
| [ ]   | Apple Silicon | « macOS Intel » (natif Intel) | Configuration échoue avec message : utiliser « macOS Intel-Rosetta » |
| [ ]   | Mac Intel    | « macOS Intel-Rosetta »      | Configuration échoue avec message : utiliser « macOS Intel » |


---

## 5. Tests de build et Artefacts

### 5.1 Configuration `COPY_TO_PROJECT_FOLDERS`

- [ ] S'assurer que `project-config.cmake` a `USER_COPY_TO_PROJECT_FOLDERS` à `ON`.

### 5.2 Dossiers Artefacts attendus par configuration

Après un **Build All** (ou build de chaque preset), vérifier la structure suivante :

#### macOS

| Testé | Configuration | Dossier Artefacts                | Sous-dossiers                 |
| ----- | ------------- | -------------------------------- | ----------------------------- |
| [ ]   | Apple Silicon | `Artefacts/macOS/ARM/`           | `AU/`, `VST3/`, `Standalone/` |
| [ ]   | Intel         | `Artefacts/macOS/Intel/`         | `AU/`, `VST3/`, `Standalone/` |
| [ ]   | Intel-Rosetta | `Artefacts/macOS/Intel-Rosetta/` | `AU/`, `VST3/`, `Standalone/` |
| [ ]   | **Universal** | `Artefacts/macOS/Universal/`     | `AU/`, `VST3/`, `Standalone/` |


**Point critique :** La configuration Universal doit produire `Artefacts/macOS/Universal/` et **non** `Artefacts/macOS/ARM/`.

#### Windows

| Testé | Configuration | Dossier Artefacts    | Sous-dossiers          |
| ----- | ------------- | -------------------- | ---------------------- |
| [ ]   | Windows x64   | `Artefacts/Windows/` | `VST3/`, `Standalone/` |


#### Linux

| Testé | Configuration | Dossier Artefacts  | Sous-dossiers          |
| ----- | ------------- | ------------------ | ---------------------- |
| [ ]   | Linux x64     | `Artefacts/Linux/` | `VST3/`, `Standalone/` |


### 5.3 Contenu des dossiers Artefacts

Pour chaque format activé (AU, VST3, Standalone), vérifier :

- [ ] **VST3** : présence du dossier `.vst3` (ex. `MyPlugin.vst3`) avec contenu binaire
- [ ] **AU** (macOS uniquement) : présence du dossier `.component` (ex. `MyPlugin.component`)
- [ ] **Standalone** : 
  - [ ] macOS : `MyPlugin.app`
  - [ ] Windows : `MyPlugin.exe`
  - [ ] Linux : binaire `MyPlugin` (sans extension)

### 5.4 Formats désactivés

Générer un projet avec **uniquement VST3** (sans AU ni Standalone) :

- [ ] Seul le dossier central custom `{ARTEFACTS_DIR_*}/{OS}/VST3/` est créé (pas AU, pas Standalone)
- [ ] Pas de dossier `AU/` ni `Standalone/`

---

## 6. Tests du script `configure-platform.py`

### 6.1 Sur macOS

- [ ] Exécuter `python configure-platform.py` → menu interactif affiché
- [ ] Option 1 (ARM) → `.vscode/settings.json` pointe vers `Builds/macOS/ARM`
- [ ] Option 2 (Intel) → sur Apple Silicon : Intel-Rosetta ; sur Mac Intel : Intel natif
- [ ] Option 3 (Universal) → pointe vers `Builds/macOS/Universal`
- [ ] `--arm` / `-a` → configure ARM sans prompt
- [ ] `--intel` / `-i` → configure Intel (ou Intel-Rosetta sur Apple Silicon)
- [ ] `--universal` / `-u` → configure Universal sans prompt

### 6.2 Sur Windows / Linux

- [ ] Exécution directe sans menu
- [ ] `.vscode/settings.json` mis à jour pour la plateforme courante

---

## 7. Tests de configuration

### 7.1 `generator-configuration.py` absent ou invalide

- [ ] Génération fonctionne avec valeurs par défaut
- [ ] Message d'avertissement affiché si erreur de chargement

### 7.2 `project-configuration.cmake` absent

- [ ] Valeurs par défaut utilisées (`COPY_TO_ARTEFACTS_DIR=ON`, `COPY_TO_SYSTEM_FOLDERS=ON` selon générateur)

### 7.3 `DEFAULT_PROJECT_DESTINATION` avec accents

- [ ] Erreur fatale avec message explicite
- [ ] Aucun projet créé

### 7.4 Codes fabricant/plugin invalides dans la config

- [ ] Avertissement affiché
- [ ] Valeurs par défaut utilisées (`Myco`, `Mypl`)

---

## 8. Tests de cas limites

### 8.1 Projet existant

- [ ] Générer un projet avec un nom existant au même emplacement
- [ ] Demande de confirmation « Overwrite ? »
- [ ] Refus → demande un autre nom
- [ ] Acceptation → dossier écrasé et régénéré

### 8.2 Au moins un format obligatoire

- [ ] Désactiver AU, VST3 et Standalone
- [ ] Message d'erreur : au moins un format requis
- [ ] Nouvelle sélection demandée

### 8.3 Projet avec nom très long

- [ ] Nom technique : `A` + 50 caractères valides
- [ ] Vérifier que la génération et le build fonctionnent

### 8.4 `JUCE_DIR` non défini

- [ ] Désactiver temporairement `JUCE_DIR`
- [ ] CMake doit afficher une erreur explicite à la configuration
- [ ] Réactiver `JUCE_DIR` → build OK

---

## 9. Récapitulatif par plateforme

### macOS (Apple Silicon ou Intel)

| Testé | Étape | Action                           | Vérification                                     |
| ----- | ----- | -------------------------------- | ------------------------------------------------ |
| [ ]   | 1     | Générer un projet                | Structure complète                               |
| [ ]   | 2     | Ouvrir dans Cursor               | Presets visibles                                 |
| [ ]   | 3     | Sélectionner Apple Silicon       | Configure + Build                                |
| [ ]   | 4     | Vérifier Artefacts               | `Artefacts/macOS/ARM/` avec AU, VST3, Standalone |
| [ ]   | 5     | Sélectionner Universal           | Configure + Build                                |
| [ ]   | 6     | Vérifier Artefacts               | `Artefacts/macOS/Universal/` (et non ARM)        |
| [ ]   | 7     | Exécuter `configure-platform.py` | Menu et mise à jour des fichiers                 |


### Windows

| Testé | Étape | Action             | Vérification                             |
| ----- | ----- | ------------------ | ---------------------------------------- |
| [ ]   | 1     | Générer un projet  | Structure complète                       |
| [ ]   | 2     | Ouvrir dans Cursor | Preset Windows visible                   |
| [ ]   | 3     | Configure + Build  | Succès                                   |
| [ ]   | 4     | Vérifier artefacts centraux | `{ARTEFACTS_DIR_WINDOWS}/Windows/VST3/`, `Standalone/` |


### Linux

| Testé | Étape | Action             | Vérification                           |
| ----- | ----- | ------------------ | -------------------------------------- |
| [ ]   | 1     | Générer un projet  | Structure complète                     |
| [ ]   | 2     | Ouvrir dans Cursor | Preset Linux visible                   |
| [ ]   | 3     | Configure + Build  | Succès                                 |
| [ ]   | 4     | Vérifier artefacts centraux | `{ARTEFACTS_DIR_LINUX}/Linux/VST3/`, `Standalone/` |


---

## 10. Checklist finale

- [ ] Tous les tests de noms et caractères passent
- [ ] Structure du projet générée correctement
- [ ] Presets CMake affichés avec les bons libellés
- [ ] Build réussi pour chaque configuration disponible sur la machine
- [ ] Dossiers Artefacts corrects (ARM, Intel, Intel-Rosetta, Universal, Windows, Linux)
- [ ] **Universal → `{ARTEFACTS_DIR_MACOS}/macOS/Universal/`** (régression corrigée)
- [ ] Script `configure-platform.py` fonctionnel
- [ ] Cas limites (projet existant, formats, config) gérés correctement

---

## Annexe : Tests automatisables par l’agent

Certains scénarios peuvent être vérifiés automatiquement (validation des chemins, structure des fichiers, etc.).

**Tests possibles par l'agent :** validation des chemins (accents), structure des fichiers générés, substitution des variables, exécution de `configure-platform.py` avec `--arm`/`--universal`, vérification des presets dans `CMakeUserPresets.json`.

**Tests non automatisables :** prompts interactifs du générateur, build CMake/compilation (JUCE requis), tests Windows/Linux (machine macOS uniquement).

---

*Fin du guide de tests.*
