from flask import Flask
from config import Config
from app.extensions import db, login_manager, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Connectez-vous pour accéder à cette page.'
    login_manager.login_message_category = 'warning'

    from app.auth import auth as auth_blueprint
    from app.routes import main as main_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    # ── Injecte lang dans tous les templates ──
    from flask import session

    @app.context_processor
    def inject_globals():
        return {'lang': session.get('lang', 'fr')}

    return app