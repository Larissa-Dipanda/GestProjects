from dotenv import load_dotenv
load_dotenv()

from app import create_app
from app.extensions import db
from app.models import Project
from app.utils import auto_translate

app = create_app()

with app.app_context():
    projects = Project.query.filter(
        (Project.title_en == None) |
        (Project.title_en == '') |
        (Project.description_en == None) |
        (Project.description_en == '') |
        (Project.domain_en == None) |
        (Project.domain_en == '')
    ).all()

    total = len(projects)
    print(f"{total} projets à traduire...")

    if total == 0:
        print("Tous les projets sont déjà traduits !")
    else:
        for i, project in enumerate(projects):
            if not project.title_en:
                project.title_en = auto_translate(project.title)
            if not project.description_en:
                project.description_en = auto_translate(project.description)
            if not project.domain_en:
                project.domain_en = auto_translate(project.domain or '')

            if (i + 1) % 10 == 0:
                db.session.commit()
                print(f"  {i+1}/{total} traduits...")

        db.session.commit()
        print("✅ Tous les projets sont traduits !")