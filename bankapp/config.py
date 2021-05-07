from pathlib import Path

SECRET_KEY = 'SxM$X2rVok%ctoAh8iwt2Eq6'
SQLALCHEMY_DATABASE_URI = f'sqlite:///{Path("./bankapp.db").absolute()}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
