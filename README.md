# syesulu (Soulou)

Application bureau de **gestion d'élevage avicole** : poulaillers, arrivages de poussins, suivi journalier et stock d'aliments.

## Fonctionnalités

- Enregistrement des sujets (poussins / poulets)
- Gestion des poulaillers et poussinières
- Suivi des arrivages, mortalité et production d'œufs
- Stock d'aliments : magasins, produits, rapports entrée/sortie
- Alertes et transferts entre poulaillers
- Rapports périodiques et inventaire
- Sauvegarde de la base de données

## Stack technique

- Python · PyQt4
- Peewee ORM · SQLite (`db_chicken.db`)
- Interface en français (gettext)

## Installation

```bash
# PyQt4 requis
python sulu/soulou.py
```

## Structure

```
syesulu/
└── sulu/
    ├── soulou.py      # Point d'entrée
    ├── model.py
    ├── ui/            # Poulaillers, monitoring, magasins…
    └── doc/           # Spécifications et maquettes
```

## Auteur

[Ibrahima Fadiga](https://github.com/fadiga) — Bamako, Mali
