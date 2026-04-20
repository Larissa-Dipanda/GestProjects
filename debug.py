from app import create_app
from app.extensions import db
from app.models import Project
from app.utils import auto_translate

app = create_app()

with app.app_context():
    # Vérifie un projet existant
    p = Project.query.first()
    print("=== PROJET EXISTANT ===")
    print("title:", p.title)
    print("title_en:", p.title_en)
    print("domain:", p.domain)
    print("domain_en:", p.domain_en)
    print()

    # Teste auto_translate directement
    print("=== TEST TRADUCTION ===")
    test = "Système de gestion pour zones rurales"
    print("FR:", test)
    print("EN:", auto_translate(test))
    print()

    test2 = "Informatique"
    print("FR:", test2)
    print("EN:", auto_translate(test2))
    print()

    # Compte les projets sans traduction
    sans_traduction = Project.query.filter(
        (Project.title_en == None) | (Project.title_en == '')
    ).count()
    print(f"Projets sans traduction: {sans_traduction}")