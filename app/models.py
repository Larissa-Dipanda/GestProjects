from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    projects = db.relationship('Project', backref='teacher', lazy=True,
                               foreign_keys='Project.teacher_id')
    applications = db.relationship('Application', backref='student', lazy=True,
                                   foreign_keys='Application.student_id')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_teacher(self):
        return self.role == 'teacher'

    def is_student(self):
        return self.role == 'student'


class Project(db.Model):
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    title_en = db.Column(db.String(200))
    description = db.Column(db.Text, nullable=False)
    description_en = db.Column(db.Text)
    domain = db.Column(db.String(100))
    domain_en = db.Column(db.String(100))
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    max_students = db.Column(db.Integer, default=1)
    status = db.Column(db.String(20), default='open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    applications = db.relationship('Application', backref='project',
                                   lazy=True, cascade='all, delete-orphan')

    def get_title(self, lang='fr'):
        if lang == 'en':
            if self.title_en:
                return self.title_en
            from app.utils import auto_translate
            return auto_translate(self.title)
        return self.title

    def get_description(self, lang='fr'):
        if lang == 'en':
            if self.description_en:
                return self.description_en
            from app.utils import auto_translate
            return auto_translate(self.description)
        return self.description

    def get_domain(self, lang='fr'):
        if lang == 'en':
            if self.domain_en:
                return self.domain_en
            from app.utils import auto_translate
            return auto_translate(self.domain or '')
        return self.domain or 'Général'

    def status_label(self, lang='fr'):
        labels = {
            'fr': {
                'open': 'Ouvert',
                'closed': 'Fermé',
                'in_progress': 'En cours',
                'completed': 'Terminé',
            },
            'en': {
                'open': 'Open',
                'closed': 'Closed',
                'in_progress': 'In Progress',
                'completed': 'Completed',
            }
        }
        return labels.get(lang, labels['fr']).get(self.status, self.status)

    def status_color(self):
        colors = {
            'open': '#16a34a',
            'closed': '#dc2626',
            'in_progress': '#2563eb',
            'completed': '#888888',
        }
        return colors.get(self.status, '#888')

    def status_bg(self):
        bgs = {
            'open': 'rgba(34,197,94,0.12)',
            'closed': 'rgba(239,68,68,0.12)',
            'in_progress': 'rgba(37,99,235,0.12)',
            'completed': 'rgba(136,136,136,0.12)',
        }
        return bgs.get(self.status, 'rgba(136,136,136,0.12)')


class Application(db.Model):
    __tablename__ = 'application'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    motivation = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)