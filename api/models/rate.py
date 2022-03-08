"""Modelo relacionados com as Avaliações."""

from datetime import date, datetime
from enum import Enum, auto

from api.instances.database import database
from api.models.base import BaseModel

db = database.db


class TypeRate(Enum):
    """Enum com os tipos de Avaliações possíveis."""

    ANIME = "Anime"
    MOVIE = "Movie"
    SERIES = "Series"
    CARTOON = "Cartoon"

    def __str__(self) -> str:
        """Transforma o ENUM da classe em seu valor.

        :return: O valor da classe em string.
        :rtype: str
        """
        return self.value


class RateModel(db.Model, BaseModel):
    """Modelo de Avaliação.

    atributos:
        id* (Integer): Identificador da avaliação
        title* (String): O título da avaliação
        content* (Text): Descrição da Avaliação
        rate_type* (Enum): O tipo da Avaliação
        rate_pic (String): o caminho da imagem da Avaliação
        rate* (Integer): A nota para a Avaliação
        date_posted (Datetime): A data em que a avaliação foi criada
        rater_id (Integer): O identificador do usuário que realizou a avaliação
        seasons (SeasonModel): As temporadas relacionadas com a avaliação
    """

    __tablename__ = "rating"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=True)
    rate_type = db.Column(db.Enum(TypeRate), default=TypeRate.MOVIE)
    rate = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    # seasons = db.relationship("SeasonModel", cascade="all,delete", backref="seasons")

    def __init__(self, title: str, content: str, rate_type: str, rate: int) -> None:
        """Inicializa a instância.

        :param title: O Título da Avaliação.
        :type title: str
        :param content: O Conteúdo da Avaliação.
        :type content: str
        :param rate_type: O Tipo da Avaliação ["Movie", "Anime", "Cartoon", "Series"]
        :type rate_type: str
        :param rate: A Nota da Avaliação [1-5]
        :type rate: int
        """
        self.title = title
        self.content = content
        self.rate_type = rate_type
        self.rate = rate

    def __repr__(self) -> str:
        """Representação da classe.

        :return: f"RatingModel(title={self.title}, content={self.content}), rate_type={self.rate_type}), rate={self.rate})"
        :rtype: str
        """
        return f"RatingModel(title={self.title}, content={self.content}), rate_type={self.rate_type}), rate={self.rate})"

    def json(self) -> dict:
        """Transforma a Instância em um dicionário de dados.

        :return: O Dicionário com os dados da instância.
        :rtype: dict
        """
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "rate_type": self.rate_type,
            "rate": self.rate,
            "date_posted": self.date_posted,
        }
