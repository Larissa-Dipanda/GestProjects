from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User


class RegisterForm(FlaskForm):
    name = StringField('Nom complet', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirmer le mot de passe',
                               validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Rôle', choices=[('student', 'Étudiant'), ('teacher', 'Enseignant')])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Cet email est déjà utilisé.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])


class ProjectForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[DataRequired()])
    domain = StringField('Domaine', validators=[Length(max=100)])
    max_students = IntegerField('Nombre max d\'étudiants', default=1)
    status = SelectField('Statut', choices=[('open', 'Ouvert'), ('closed', 'Fermé'),
                                             ('completed', 'Terminé')])


class ApplicationForm(FlaskForm):
    motivation = TextAreaField('Lettre de motivation',
                                validators=[DataRequired(), Length(min=50)])