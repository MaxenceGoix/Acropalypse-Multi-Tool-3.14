# Installation et compilation

## Python pris en charge

Python 3.10 à 3.14. L’interface est basée sur Tkinter et fonctionne sous Windows 10/11 et Linux.
Tkinter doit être présent dans l’installation Python (sur certaines distributions Linux, installez aussi `python3-tk`).

## Installation rapide (PNG)

```bash
python -m venv .venv
# Windows PowerShell : .venv\\Scripts\\Activate.ps1
# Linux : source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python gui.py
```

Cette installation permet la détection et la reconstruction PNG.

## Activer la prise en charge GIF

La récupération GIF utilise une extension Rust/PyO3 compilée pour la version de Python et le système utilisés. Les anciens binaires `.pyd` et `.so` précompilés ont été retirés : ils n’étaient pas interchangeables entre versions de Python et systèmes.

Prérequis : Rust stable (`rustup`), puis :

```bash
python -m pip install --upgrade maturin
python -m pip install .
```

Cela compile et installe `gif_lib.acropalypse_gif` pour l’environnement Python actif. Relancez ensuite `python gui.py`.

## Générer une wheel

Depuis la racine du dépôt :

```bash
python -m pip install maturin
maturin build --release --out dist
```

La CI GitHub Actions construit automatiquement des wheels Windows et Linux pour Python 3.10 à 3.14. Récupérez l’artefact correspondant à votre système et version de Python.

## Dépannage

- `No module named tkinter` : installez le composant Tk/Tkinter de votre distribution Python (`python3-tk` sur Debian/Ubuntu).
- GIF indisponible : vérifiez que `python -m pip install .` a été exécuté dans le même environnement virtuel que `python gui.py`.
- En cas d’erreur de compilation Rust, mettez à jour Rust stable (`rustup update`) et réessayez.

La reconstruction dépend du format, de la provenance et des dimensions d’origine de l’image. Un résultat visuel plausible n’est pas une garantie de restauration exacte.

## Créer une application autonome

Après avoir installé les dépendances (et compilé le module GIF si nécessaire) :

```bash
python -m pip install pyinstaller
python package_app.py
```

L’exécutable est généré dans `dist/`. Il faut effectuer cette opération sur chaque système cible : une compilation Windows produit un `.exe` Windows, une compilation Linux produit un binaire Linux. PyInstaller ne réalise pas de compilation croisée fiable entre ces deux systèmes.
