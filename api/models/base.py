"""Módulo com os Modelos Bases para outras classes."""

from abc import ABC
from typing import Union

from api.instances.database import database

db = database.db


class BaseModel:
    """BaseModel com as operações básica de banco de dados dos modelos."""

    @classmethod
    def find_by_tile(cls, title: str) -> Union[object, None]:
        """Pesquisa o primeiro objeto na classe com base no título.

        :param title: O título a ser pesquisado
        :type title: str
        :return: Um objeto com o dado retornado do Banco de Dados
        :rtype: Union[object, None]
        """
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_by_id(cls, id: int) -> Union[object, None]:
        """Pesquisa o primeiro objeto na classe com base no identificador.

        :param id: O identificador a ser pesquisado
        :type id: int
        :return: Um objeto com o dado retornado do Banco de Dados
        :rtype: Union[object, None]
        """
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_first(cls) -> Union[object, None]:
        """Retorna o primeiro objeto da base de dados.

        :return: Um objeto com o dado retornado do Banco de Dados
        :rtype: Union[object, None]
        """
        return cls.query.first()

    @classmethod
    def find_all(cls) -> Union[list[object], None]:
        """Retorna todos os objetos da classe.

        :return: uma lista de objetos retornados do Banco de Dados
        :rtype: Union[[object], None]
        """
        return cls.query.all()

    def save_to_db(self) -> None:
        """Salva a instância do objeto no banco de dados."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Remove a instância do objeto do banco de dados."""
        db.session.delete(self)
        db.session.commit()
