import os

# Charge .env seulement en local
if os.path.exists('.env'):
    from dotenv import load_dotenv
    load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '3eeb3ca9eca7561ecd27494252bc5cdc81b299e5d06fa063c4c1aa02930c0582'
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or 'sqlite:///projet_univ.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False