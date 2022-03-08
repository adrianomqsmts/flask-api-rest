"""SQLAlchemy Database Instaces"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class Database:
    """Database Class Operations."""

    db: SQLAlchemy() = None

    def __init__(self) -> None:
        """Inicializar o banco com o SQLAlchemy."""
        self.db = SQLAlchemy()

    def set_app(self, app: Flask) -> None:
        """Ligar o Banco com o contexto da aplicação."""
        self.db.init_app(app)

    def create_all(self) -> None:
        """Gerar as tabelas."""
        self.db.create_all()

    def remove_all(self) -> None:
        """Remove as tabelas do DB."""
        pass

    def destroy_db(self) -> None:
        """Remove o Database."""
        pass


database = Database()
