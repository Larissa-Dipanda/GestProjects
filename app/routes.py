from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, session
from functools import wraps
from flask_login import login_required, current_user
from datetime import datetime
from app.models import Project, Application, User
from app.extensions import db
from app.utils import auto_translate
main = Blueprint('main', __name__)


def teacher_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_teacher():
            abort(403)
        return f(*args, **kwargs)
    return decorated


def student_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_student():
            abort(403)
        return f(*args, **kwargs)
    return decorated


# ── Langue ──────────────────────────────────────────────────
@main.route('/set-lang/<lang>')
def set_lang(lang):
    if lang in ['fr', 'en']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('main.index'))


def get_lang():
    return session.get('lang', 'fr')


# ── Accueil ──────────────────────────────────────────────────
@main.route('/')
def index():
    projects = Project.query.filter_by(status='open').limit(6).all()
    return render_template('index.html', projects=projects, lang=get_lang())


# ── Dashboard ────────────────────────────────────────────────
@main.route('/dashboard')
@login_required
def dashboard():
    now = datetime.now()
    lang = get_lang()

    if current_user.is_teacher():
        projects = Project.query.filter_by(
            teacher_id=current_user.id
        ).order_by(Project.created_at.desc()).all()
        total_apps = sum(len(p.applications) for p in projects)

        # Stats par statut
        stats = {
            'open': sum(1 for p in projects if p.status == 'open'),
            'in_progress': sum(1 for p in projects if p.status == 'in_progress'),
            'completed': sum(1 for p in projects if p.status == 'completed'),
            'closed': sum(1 for p in projects if p.status == 'closed'),
        }
        return render_template('dashboard.html', projects=projects,
                               total_apps=total_apps, now=now,
                               stats=stats, lang=lang)

    if current_user.is_student():
        applications = Application.query.filter_by(
            student_id=current_user.id).all()
        recent_projects = Project.query.filter_by(status='open') \
            .order_by(Project.created_at.desc()).limit(6).all()
        open_projects_count = Project.query.filter_by(status='open').count()
        return render_template('dashboard.html', applications=applications,
                               recent_projects=recent_projects,
                               open_projects_count=open_projects_count,
                               now=now, lang=lang)
    abort(403)


# ── Liste projets avec filtres avancés ───────────────────────
@main.route('/projects')
def projects_list():
    lang = get_lang()
    search = request.args.get('search', '')
    domain = request.args.get('domain', '')
    status_filter = request.args.get('status', '')
    page = request.args.get('page', 1, type=int)

    query = Project.query

    if search:
        if lang == 'en':
            query = query.filter(Project.title_en.ilike(f'%{search}%'))
        else:
            query = query.filter(Project.title.ilike(f'%{search}%'))
    if domain:
        if lang == 'en':
            query = query.filter(Project.domain_en.ilike(f'%{domain}%'))
        else:
            query = query.filter(Project.domain.ilike(f'%{domain}%'))
    if status_filter:
        query = query.filter(Project.status == status_filter)

    query = query.order_by(Project.created_at.desc())
    projects = query.paginate(page=page, per_page=12, error_out=False)

    # Stats globales
    global_stats = {
        'total': Project.query.count(),
        'open': Project.query.filter_by(status='open').count(),
        'in_progress': Project.query.filter_by(status='in_progress').count(),
        'closed': Project.query.filter_by(status='closed').count(),
        'completed': Project.query.filter_by(status='completed').count(),
    }

    # ── Domaines traduits selon la langue ──
    if lang == 'en':
        raw_domains = db.session.query(Project.domain_en).distinct().order_by(
            Project.domain_en).all()
        domains = [d[0] for d in raw_domains if d[0]]
    else:
        raw_domains = db.session.query(Project.domain).distinct().order_by(
            Project.domain).all()
        domains = [d[0] for d in raw_domains if d[0]]

    return render_template('projects/list.html', projects=projects,
                           search=search, domain=domain,
                           status_filter=status_filter,
                           global_stats=global_stats,
                           domains=domains, lang=lang)

# ── Détail projet ─────────────────────────────────────────────
@main.route('/projects/<int:id>')
def project_detail(id):
    project = Project.query.get_or_404(id)
    from app.forms import ApplicationForm
    form = ApplicationForm()
    user_application = None
    if current_user.is_authenticated and current_user.is_student():
        user_application = Application.query.filter_by(
            student_id=current_user.id, project_id=id).first()
    lang = get_lang()
    return render_template('projects/detail.html', project=project,
                           form=form, user_application=user_application,
                           lang=lang)


# ─@main.route('/projects/new', methods=['GET', 'POST'])
@login_required
@teacher_required
def create_project():
    from app.forms import ProjectForm
    import concurrent.futures
    form = ProjectForm()
    lang = get_lang()

    DOMAIN_EN_TO_FR = {
        'Computer Science': 'Informatique',
        'Artificial Intelligence': 'Intelligence Artificielle',
        'Software Engineering': 'Génie logiciel',
        'Networks & Security': 'Réseaux et Sécurité',
        'Mobile': 'Mobile',
        'Health': 'Santé',
        'Smart Agriculture': 'Agriculture intelligente',
        'Environment': 'Environnement',
        'Education': 'Éducation',
        'Finance': 'Finance',
        'Mathematics': 'Mathématiques',
        'Physics': 'Physique',
        'Chemistry': 'Chimie',
        'Architecture': 'Architecture',
        'Law': 'Droit',
    }
    DOMAIN_FR_TO_EN = {v: k for k, v in DOMAIN_EN_TO_FR.items()}

    if form.validate_on_submit():
        domain_input = form.domain.data or ''

        if lang == 'en' and domain_input in DOMAIN_EN_TO_FR:
            domain_fr = DOMAIN_EN_TO_FR[domain_input]
            domain_en = domain_input
        else:
            domain_fr = domain_input
            domain_en = DOMAIN_FR_TO_EN.get(domain_input, '')

        # Traductions en parallèle
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_title = executor.submit(auto_translate, form.title.data)
            future_desc = executor.submit(auto_translate, form.description.data)
            if not domain_en:
                future_domain = executor.submit(auto_translate, domain_input)
            title_en = future_title.result()
            desc_en = future_desc.result()
            if not domain_en:
                domain_en = future_domain.result()

        project = Project(
            title=form.title.data,
            title_en=title_en,
            description=form.description.data,
            description_en=desc_en,
            domain=domain_fr,
            domain_en=domain_en,
            max_students=form.max_students.data,
            status=form.status.data,
            teacher_id=current_user.id
        )
        db.session.add(project)
        db.session.commit()
        flash('Projet créé avec succès !' if lang == 'fr' else 'Project created!',
              'success')
        return redirect(url_for('main.dashboard'))

    return render_template('projects/create.html', form=form, lang=lang)

# ── Modifier projet ───────────────────────────────────────────
@main.route('/projects/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@teacher_required
def edit_project(id):
    from app.forms import ProjectForm
    import concurrent.futures
    project = Project.query.get_or_404(id)
    if project.teacher_id != current_user.id:
        abort(403)
    form = ProjectForm(obj=project)
    lang = get_lang()
    if form.validate_on_submit():
        project.title = form.title.data
        project.description = form.description.data
        project.domain = form.domain.data
        project.max_students = form.max_students.data
        project.status = form.status.data

        # Traductions en parallèle pour réduire le temps d'attente
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_title = executor.submit(auto_translate, form.title.data)
            future_desc = executor.submit(auto_translate, form.description.data)
            future_domain = executor.submit(
                auto_translate, form.domain.data or '')
            project.title_en = future_title.result()
            project.description_en = future_desc.result()
            project.domain_en = future_domain.result()

        db.session.commit()
        flash('Projet modifié !' if lang == 'fr' else 'Project updated!',
              'success')
        return redirect(url_for('main.dashboard'))
    return render_template('projects/edit.html', form=form,
                           project=project, lang=lang)
    
# ── Supprimer projet ──────────────────────────────────────────
@main.route('/projects/<int:id>/delete', methods=['POST'])
@login_required
@teacher_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    if project.teacher_id != current_user.id:
        abort(403)
    db.session.delete(project)
    db.session.commit()
    flash('Projet supprimé.', 'info')
    return redirect(url_for('main.dashboard'))


# ── Changer statut projet ─────────────────────────────────────
@main.route('/projects/<int:id>/status/<new_status>', methods=['POST'])
@login_required
@teacher_required
def change_project_status(id, new_status):
    project = Project.query.get_or_404(id)
    if project.teacher_id != current_user.id:
        abort(403)
    valid = ['open', 'closed', 'in_progress', 'completed']
    if new_status in valid:
        project.status = new_status
        db.session.commit()
        flash(f'Statut mis à jour : {new_status}', 'success')
    return redirect(url_for('main.project_detail', id=id))


# ── Postuler ──────────────────────────────────────────────────
@main.route('/projects/<int:id>/apply', methods=['POST'])
@login_required
@student_required
def apply_project(id):
    from app.forms import ApplicationForm
    project = Project.query.get_or_404(id)
    existing = Application.query.filter_by(
        student_id=current_user.id, project_id=id).first()
    if existing:
        flash('Vous avez déjà postulé.', 'warning')
        return redirect(url_for('main.project_detail', id=id))
    form = ApplicationForm()
    if form.validate_on_submit():
        application = Application(
            student_id=current_user.id,
            project_id=id,
            motivation=form.motivation.data
        )
        db.session.add(application)
        db.session.commit()
        flash('Candidature envoyée !', 'success')
    return redirect(url_for('main.project_detail', id=id))


# ── Gérer candidatures ────────────────────────────────────────
@main.route('/applications/<int:id>/<action>', methods=['POST'])
@login_required
@teacher_required
def manage_application(id, action):
    application = Application.query.get_or_404(id)
    if action == 'accept':
        application.status = 'accepted'
        flash('Candidature acceptée.', 'success')
    elif action == 'reject':
        application.status = 'rejected'
        flash('Candidature refusée.', 'info')
    db.session.commit()
    return redirect(url_for('main.project_detail', id=application.project_id))


# ── Mes candidatures ──────────────────────────────────────────
@main.route('/my-applications')
@login_required
@student_required
def my_applications():
    applications = Application.query.filter_by(
        student_id=current_user.id
    ).order_by(Application.applied_at.desc()).all()
    return render_template('my_applications.html',
                           applications=applications, lang=get_lang())


# ── Erreurs ───────────────────────────────────────────────────
@main.app_errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403


@main.app_errorhandler(404)
def not_found(e):
    return render_template('errors/404.html'), 404