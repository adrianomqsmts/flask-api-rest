"""Controler da rota de API de Avaliação."""
from flask import request
from flask_restx import Resource, fields
from marshmallow import ValidationError
from werkzeug.wrappers import Response

from api.instances.server import server
from api.models.rate import RateModel, TypeRate
from api.schemas.rate import RateSchema

api = server.api
rate_ns = api.namespace(
    name="Rating", description="Rating related Operations", path="/rate"
)

rate_schema = RateSchema()  # Seraliza um Objeto
rate_list_schema = RateSchema(many=True)  # Serializa múltiplos Objetos

from flask import url_for


# https://www.treinaweb.com.br/blog/o-que-e-hateoas
def make_public_rate(rate: RateModel) -> dict:
    """Create a public URI based on that ID."""
    new_rate = {
        "title": rate["title"],
        "content": rate["content"],
        "rate_type": rate["rate_type"],
        "rate": rate["rate"],
        "uri": url_for("api.rate", id=rate["id"], _external=True),
    }

    return new_rate


model_output = rate_ns.model(
    "Model",
    {
        "title": fields.String(),
        "content": fields.String(),
        "rate_type": fields.String(),
        "rate": fields.Integer(),
        "uri": fields.String(),
    },
)

model_input = rate_ns.model(
    "Model",
    {
        "title": fields.String(
            required=True, max_length=255, description="Title of Rate"
        ),
        "content": fields.String(description="Your Opinion about this title."),
        "rate_type": fields.String(
            required=True, enum=[tr.value for tr in TypeRate], default="Movie"
        ),
        "rate": fields.Integer(
            min=1, max=5, required=True, description="Your rate level"
        ),
    },
)


class Rate(Resource):
    """Classe que trabalha com o CRUD baseado no ID."""

    @rate_ns.marshal_with(model_output)
    def get(self, id: int) -> Response:
        """Pesquisa um avaliação com base no identificador único.

        :param id: Identificador da avaliação
        :type id: _type_
        :return: A Avaliação pesquisada, caso contrário,  {"message": "None Rate could be found"}, 404
        :rtype: Response
        """
        rate_data = RateModel.find_by_id(id)
        if rate_data:
            rate_data = rate_schema.dump(rate_data)
            rate_data = make_public_rate(rate_data)
            return rate_data, 200
        else:
            return {"message": "That Rate could not be found"}, 404

    @rate_ns.expect(model_input)
    def put(self, id: int) -> Response:
        """Atualiza um dado existente com base no seu identificador único.

        :param id: O identificador da Avaliação a ser atualiazada
        :type id: int
        :return: A propria avaliação atualizada, caso contrário,  {"message": "None Rate could be found"}, 404
        :rtype: Response
        """
        rate_data = RateModel.find_by_id(id)
        if rate_data:
            rate_json = request.get_json()
            updated = rate_schema.load(rate_json)

            rate_data.title = updated.title
            rate_data.content = updated.content
            rate_data.rate_type = updated.rate_type
            rate_data.rate = updated.rate
            rate_data.save_to_db()

            return rate_schema.dump(rate_data), 200
        else:
            return {"message": "None Rate could be found"}, 404

    def delete(self, id: int) -> Response:
        """Remove uma Avaliação existente com base no identificador único.

        :param id: O identificador da Avaliação a ser removida
        :type id: int
        :return: 204, caso contrário,  {"message": "None Rate could be found"}, 404
        :rtype: Response
        """
        book_data = RateModel.find_by_id(id)
        if book_data:
            book_data.delete_from_db()
            return 204
        else:
            return {"message": "None Rate could be found"}, 404


class RateList(Resource):
    """Casse de Inserção de uma Avaliação e Leitura de múltiplas Avaliações."""

    @rate_ns.marshal_list_with(model_output)
    def get(self) -> Response:
        """Pesquisa todas as Avaliações existentes no Banco de Dados.

        :return: Todas as avaliações no Banco de Dados 200, caso contrário, {"message": "None Rate could be found"}, 404
        :rtype: Response
        """
        rate_all_data = RateModel.find_all()
        if rate_all_data:
            rate_uri = []
            for rate_data in rate_all_data:
                rate_data = rate_schema.dump(rate_data)
                rate_data = make_public_rate(rate_data)
                rate_uri.append(rate_data)
            return rate_uri, 200
        else:
            return {"message": "None Rate could be found"}, 404

    @rate_ns.expect(model_input, validate=True)  # Modelo de dados esperados
    @rate_ns.doc("Create an Item")  # Descrição para a requisição post
    def post(self) -> Response:
        """Insere uma nova avaliações no Banco de Dados.

        :return: A própria avaliação inserida, 201, caso contrário, 422
        :rtype: Response
        """
        try:
            rate_json = (
                request.get_json()
            )  # pega tudo que está dentro do body da requisição
            rate_data = rate_schema.load(rate_json)  # Carrega o Json para um Objeto
            rate_data.save_to_db()
            return rate_schema.dump(rate_data), 201
        except ValidationError as err:
            return err.messages, 422
