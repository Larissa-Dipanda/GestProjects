from app import create_app
from app.extensions import db
from app.models import User, Project, Application
import random
from datetime import datetime, timedelta

app = create_app()

# Traductions des domaines
domain_translations = {
    'Informatique': 'Computer Science',
    'Agriculture intelligente': 'Smart Agriculture',
    'Génie logiciel': 'Software Engineering',
    'Santé': 'Health',
    'Réseaux et Sécurité': 'Networks & Security',
    'Environnement': 'Environment',
    'Mobile': 'Mobile',
    'Intelligence Artificielle': 'Artificial Intelligence',
    'Éducation': 'Education',
    'Finance': 'Finance',
    'Droit': 'Law',
    'Chimie': 'Chemistry',
    'Physique': 'Physics',
    'Mathématiques': 'Mathematics',
    'Architecture': 'Architecture',
}

# Templates de titres FR/EN
title_templates = [
    ("Système {} pour {} — édition {}",
     "{} System for {} — edition {}"),
    ("Plateforme {} de gestion {} — {}",
     "{} Management Platform for {} — {}"),
    ("Application {} pour {} — {}",
     "{} Application for {} — {}"),
    ("Développement {} de {} — {}",
     "{} Development of {} — {}"),
    ("Modèle {} pour {} — {}",
     "{} Model for {} — {}"),
    ("Outil {} d'analyse {} — {}",
     "{} Analysis Tool for {} — {}"),
    ("Infrastructure {} pour {} — {}",
     "{} Infrastructure for {} — {}"),
    ("Chatbot {} en {} — {}",
     "{} Chatbot in {} — {}"),
]

subjects_fr = [
    'médical', 'cadastral numérique', 'e-learning', 'de télémédecine',
    'de paiement mobile', 'routier', 'agricole', 'climatique',
    'de reconnaissance vocale', 'de détection de fraude',
    'de gestion scolaire', 'de suivi épidémique', 'de cartographie',
    'de recommandation', 'de prédiction', 'de surveillance',
    'de traduction', 'de classification', 'de diagnostic',
    'de monitorage réseau',
]

subjects_en = [
    'medical', 'digital cadastral', 'e-learning', 'telemedicine',
    'mobile payment', 'road', 'agricultural', 'climate',
    'voice recognition', 'fraud detection',
    'school management', 'epidemic monitoring', 'mapping',
    'recommendation', 'prediction', 'surveillance',
    'translation', 'classification', 'diagnostic',
    'network monitoring',
]

zones_fr = [
    'zones rurales', 'zones urbaines', 'Cameroun', 'Afrique centrale',
    'Université de Douala', 'PME locales', 'hôpitaux publics',
    'établissements scolaires', 'agriculteurs', 'jeunes entrepreneurs',
]

zones_en = [
    'rural areas', 'urban areas', 'Cameroon', 'Central Africa',
    'University of Douala', 'local SMEs', 'public hospitals',
    'schools', 'farmers', 'young entrepreneurs',
]

descriptions_fr = [
    "Projet de recherche appliquée visant à développer une solution innovante "
    "pour résoudre des problématiques locales au Cameroun.",
    "Conception et implémentation d'un système complet intégrant les dernières "
    "technologies pour améliorer les conditions de vie.",
    "Étude et développement d'une plateforme numérique adaptée aux besoins "
    "spécifiques des populations camerounaises.",
    "Recherche et développement d'un outil technologique pour moderniser "
    "les pratiques existantes dans le contexte africain.",
    "Création d'une solution logicielle robuste pour automatiser et optimiser "
    "les processus dans le secteur ciblé.",
]

descriptions_en = [
    "Applied research project aimed at developing an innovative solution "
    "to address local issues in Cameroon.",
    "Design and implementation of a complete system integrating the latest "
    "technologies to improve living conditions.",
    "Study and development of a digital platform adapted to the specific needs "
    "of Cameroonian populations.",
    "Research and development of a technological tool to modernize "
    "existing practices in the African context.",
    "Creation of a robust software solution to automate and optimize "
    "processes in the targeted sector.",
]

with app.app_context():
    db.drop_all()
    db.create_all()

    # ── Enseignants ──
    teachers_data = [
        (' Elvis Mee', 'teacher@univ.fr'),
        (' Ben Njoya', 'b.njoya@univ.fr'),
        (' Alan Ndoe', 'a.ndoe@univ.fr'),
        (' Ben Mbembe', 'b.mbembe@univ.fr'),
        (' Alfred Ndock', 'a.ndock@univ.fr'),
        (' Basile Mbile', 'b.mbile@univ.fr'),
        (' Hélène Nganou', 'h.nganou@univ.fr'),
        (' Arlette Nguema', 'a.nguema@univ.fr'),
        (' Igor Obiang', 'i.obiang@univ.fr'),
        (' Reine Ngassa', 'r.ngassa@univ.fr'),
        (' Serge Biyong', 's.biyong@univ.fr'),
        (' Alice Feudjio', 'a.feudjio@univ.fr'),
        (' Paul Mbock', 'p.mbock@univ.fr'),
        (' Marie Atangana', 'm.atangana@univ.fr'),
        (' Patrick Mbeck', 'p.mbeck@univ.fr'),
    ]
    teachers = []
    for name, email in teachers_data:
        t = User(name=name, email=email, role='teacher')
        t.set_password('password123')
        teachers.append(t)

    # Étudiants
    students_data = [
        ('Serge Mbarga', 'student@univ.fr'),
        ('Raïssa Tamba', 'r.tamba@univ.fr'),
        ('Joël Ndoumbe', 'j.ndoumbe@univ.fr'),
        ('Carine Bello', 'c.bello@univ.fr'),
        ('Thierry Essomba', 't.essomba@univ.fr'),
        ('Nadège Fouda', 'n.fouda@univ.fr'),
        ('Christian Mba', 'c.mba@univ.fr'),
        ('Sylvie Eba', 's.eba@univ.fr'),
    ]
    students = []
    for name, email in students_data:
        s = User(name=name, email=email, role='student')
        s.set_password('password123')
        students.append(s)

    db.session.add_all(teachers + students)
    db.session.commit()

    # Statuts
    status_pool = (
        ['open'] * 3100 +
        ['closed'] * 20 +
        ['in_progress'] * 3380 +
        ['completed'] * 2000
    )
    random.shuffle(status_pool)

    domains = list(domain_translations.keys())
    years = list(range(2020, 2027))

    print("Création de 8500 projets bilingues...")

    for i in range(8500):
        status = status_pool[i]
        teacher = random.choice(teachers)
        domain_fr = random.choice(domains)
        domain_en = domain_translations[domain_fr]
        year = random.choice(years)

        idx = random.randint(0, len(subjects_fr) - 1)
        subject_fr = subjects_fr[idx]
        subject_en = subjects_en[idx]

        idx2 = random.randint(0, len(zones_fr) - 1)
        zone_fr = zones_fr[idx2]
        zone_en = zones_en[idx2]

        tpl_idx = random.randint(0, len(title_templates) - 1)
        tpl_fr, tpl_en = title_templates[tpl_idx]

        title_fr = tpl_fr.format(subject_fr, zone_fr, year)
        title_en = tpl_en.format(subject_en, zone_en, year)

        desc_idx = random.randint(0, len(descriptions_fr) - 1)

        days_ago = random.randint(1, 1200)
        created = datetime.utcnow() - timedelta(days=days_ago)

        p = Project(
            title=title_fr,
            title_en=title_en,
            description=descriptions_fr[desc_idx],
            description_en=descriptions_en[desc_idx],
            domain=domain_fr,
            domain_en=domain_en,
            teacher_id=teacher.id,
            status=status,
            max_students=random.randint(1, 6),
            created_at=created,
        )
        db.session.add(p)

        if (i + 1) % 500 == 0:
            db.session.commit()
            print(f"  {i+1}/8500 projets créés...")

    db.session.commit()

    # Candidatures de test
    open_projects = Project.query.filter_by(status='open').limit(10).all()
    for project in open_projects:
        for student in random.sample(students, random.randint(1, 3)):
            existing = Application.query.filter_by(
                student_id=student.id, project_id=project.id).first()
            if not existing:
                app_obj = Application(
                    student_id=student.id,
                    project_id=project.id,
                    motivation="Je suis très motivé par ce projet.",
                    status=random.choice(['pending', 'accepted', 'rejected'])
                )
                db.session.add(app_obj)

    db.session.commit()
    print("\n✅ Base créée avec 8500 projets bilingues !")
    print("Enseignant : teacher@univ.fr / password123")
    print("Étudiant   : student@univ.fr / password123")