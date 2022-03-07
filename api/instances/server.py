"""Servidor."""

from typing import Optional

from flask import Flask, Blueprint
from flask_restx import Api


class Server:
    """Server Instace of application."""

    def __init__(self) -> None:
        """Init App and Api."""
        self.app = Flask(__name__)
        self.blueprint = Blueprint("api", __name__, url_prefix="/api")
        self.api = Api(
            self.blueprint,
            version="1.0",
            title="RatingStars",
            description="Rating system for movies, series, etc.",
            doc="/doc",
        )
        self.app.register_blueprint(self.blueprint)

    def set_config(self, config: Optional[dict] = None) -> None:
        """Configura a aplicação com um dicionário.

        ou carregar das configuração padrão do arquivo config no servidor.

        :param config: Dicionário com os dados de configuração, defaults to None
        :type config: Optional[dict], optional
        """
        if config:
            self.app.config.from_mapping(config)
        else:
            self.app.config.from_object("api.instances.config")

    def run(self, port: int = 5000, debug: bool = True, host: str = "0.0.0.0") -> None:
        """Iniciar definindo o Host, Port e Debug.

        :param port: A porta da aplicação, defaults to 5000
        :type port: int, optional
        :param debug: A Aplicação está em desenvolvimento ou teste, defaults to True
        :type debug: bool, optional
        :param host: O endereço da aplicação, defaults to "0.0.0.0"
        :type host: str, optional
        """
        self.app.run(port=port, debug=debug, host=host)


server = Server()
