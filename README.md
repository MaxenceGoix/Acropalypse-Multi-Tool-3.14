# Acropalypse Multi-Tool — version modernisée

Application de bureau pour détecter des PNG/GIF contenant des données après leur fin normale et tenter de reconstruire les images concernées.

## Nouveautés

- Interface réunie dans une seule fenêtre avec deux onglets : **Détection** et **Reconstruction**.
- Aperçus côte à côte, profils d’appareils, dimensions modifiables et sauvegarde explicite.
- Analyse récursive des dossiers.
- Traitements longs exécutés en arrière-plan ; les mises à jour de l’interface restent sur le thread Tk.
- Chemins de fichiers temporaires uniques, sans dépendance à un nom `restored.png` partagé.
- Dépendances Python actualisées et extension GIF reconstruite depuis les sources avec PyO3.
- CI de compilation de wheels pour Windows et Linux, Python 3.10–3.14.

## Démarrer

Consultez [BUILD.md](BUILD.md) pour l’installation détaillée.

Pour lancer l’interface après installation des dépendances :

```bash
python gui.py
```

L’installation de base active le traitement PNG. Le support GIF nécessite la compilation de l’extension native Rust.

## Compatibilité et limites

- Python 3.10–3.14
- Windows 10/11 et Linux
- Tkinter requis
- Pillow requis
- Rust requis uniquement pour compiler le support GIF

Ce projet est un outil de récupération spécialisé dans certains fichiers affectés par la vulnérabilité aCropalypse (notamment des captures d’écran Windows Snipping Tool et certains appareils Pixel). Il ne peut pas restaurer arbitrairement toute image recadrée. La détection de données supplémentaires après IEND est un indicateur, pas une preuve absolue de vulnérabilité.

## Crédits

La logique initiale de reconstruction PNG et GIF provient du projet d’origine et de ses contributeurs. Voir [LICENSE](LICENSE) et les références dans l’historique du projet.
