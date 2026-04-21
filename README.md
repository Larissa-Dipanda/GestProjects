# GestProjects 📚

Plateforme de gestion de projets étudiants — Université de Douala

## Description

GestProjects est une application web bilingue (Français/Anglais) permettant aux enseignants de publier des sujets de projets et aux étudiants de postuler. Développée avec Flask (Python) dans le cadre d'un projet académique à l'ENSPD — Niveau 4 Génie Logiciel.

## Fonctionnalités

- Authentification avec rôles (Étudiant, Enseignant)
- CRUD complet des projets (enseignants)
- Candidatures avec lettre de motivation (étudiants)
- Gestion des candidatures : accepter / refuser
- Filtrage et recherche des projets par domaine et statut
- Dashboard personnalisé selon le rôle
- Interface bilingue Français / Anglais
- Traduction automatique via Google Gemini API
- Design responsive (mobile & desktop)
- 8500 projets de démonstration

## Stack technique

- **Backend** : Python 3, Flask 3
- **Base de données** : SQLite + SQLAlchemy
- **Authentification** : Flask-Login
- **Formulaires** : Flask-WTF
- **Traduction** : Google Gemini API
- **Frontend** : HTML, CSS, Bootstrap 5, Jinja2
- **Déploiement** : Render.com

## Installation

```bash
# Cloner le projet
git clone https://github.com/Larissa-Dipanda/GestProjects.git
cd GestProjects

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement (Windows)
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
# Créer un fichier .env à la racine :
SECRET_KEY=3eeb3ca9eca7561ecd27494252bc5cdc81b299e5d06fa063c4c1aa02930c0582
GEMINI_API_KEY=AIzaSyCpde_x-sBz2jkQgYD-vyjUqsupvGkrhws
DATABASE_URL=sqlite:///projet_univ.db

# Créer la base de données avec les données de test
python seed.py

# Lancer l'application
python wsgi.py
```

## Comptes de test

| Rôle | Email | Mot de passe |
|---|---|---|
| Enseignant | teacher@univ.fr | password123 |
| Étudiant | student@univ.fr | password123 |

## Structure du projet
GestProjects/
├── wsgi.py              # Point d'entrée
├── config.py            # Configuration
├── seed.py              # Données de test
├── Procfile             # Configuration Render
├── requirements.txt     # Dépendances
├── app/
│   ├── init.py      # Factory Flask
│   ├── models.py        # Modèles SQLAlchemy
│   ├── routes.py        # Routes principales
│   ├── auth.py          # Authentification
│   ├── forms.py         # Formulaires WTF
│   ├── extensions.py    # Extensions Flask
│   ├── utils.py         # Traduction automatique
│   └── templates/       # Templates Jinja2
│       ├── base.html
│       ├── dashboard.html
│       ├── index.html
│       ├── my_applications.html
│       ├── auth/
│       │   ├── login.html
│       │   └── register.html
│       ├── projects/
│       │   ├── list.html
│       │   ├── detail.html
│       │   ├── create.html
│       │   └── edit.html
│       └── errors/
│           ├── 403.html
│           └── 404.html
└── static/

## Déploiement

L'application est déployée sur Render.com :
🔗 [https://gestprojects.onrender.com](https://gestprojects.onrender.com)

## Auteur

**Soppi Dipanda Edika Larissa**  
Étudiante en Génie Logiciel — Niveau 4  
École Nationale Supérieure Polytechnique de Douala (ENSPD)  
Université de Douala — Année académique 2025-2026

## Encadrement

Projet réalisé dans le cadre du cours de Développement Web Dynamique avec Python — ENSPD 
Sous la supervision de Dr Phillippe TOTTO
2025-2026