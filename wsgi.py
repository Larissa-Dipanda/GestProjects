from app import create_app
from app.extensions import db
import logging

logging.basicConfig(level=logging.DEBUG)

app = create_app()

with app.app_context():
    try:
        db.create_all()
        logging.info("Base de données créée avec succès")
    except Exception as e:
        logging.error(f"Erreur base de données: {e}")

if __name__ == '__main__':
    app.run(debug=False)