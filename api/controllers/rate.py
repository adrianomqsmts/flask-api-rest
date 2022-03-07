from flask_restx import Resource, fields
from flask import request
from marshmallow import ValidationError
from api.models.rate import RateModel, TypeRate
from api.schemas.rate import RateSchema
from api.instances.server import server


api = server.api
rate = api.namespace(
    name="Rating", description="Rating related Operations", path="/rate"
)

rate_schema = RateSchema()  # Seraliza um Objeto
rate_list_schema = RateSchema(many=True)  # Serializa múltiplos Objetos

from flask import url_for


def make_public_rate(rate):
    new_rate = {
        "title": rate["title"],
        "content": rate["content"],
        "rate_type": rate["rate_type"],
        "rate": rate["rate"],
        "uri": url_for("api.rate", id=rate["id"], _external=True),
    }

    return new_rate


model_get = rate.model(
    "Model",
    {
        "title": fields.String(),
        "content": fields.String(),
        "rate_type": fields.String(),
        "rate": fields.Integer(),
        "uri": fields.String(),
    },
)

model_post = rate.model(
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
    @rate.marshal_with(model_get)
    def get(self, id):
        rate_data = RateModel.find_by_id(id)
        if rate_data:
            rate_data = rate_schema.dump(rate_data)
            rate_data = make_public_rate(rate_data)
            return rate_data, 200
        else:
            return {"message": "That Rate could not be found"}, 404

    @rate.expect(model_post)
    def put(self, id):
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

    def delete(self, id):
        book_data = RateModel.find_by_id(id)
        if book_data:
            book_data.delete_from_db()
            return 204
        else:
            return {"message": "None Rate could be found"}, 404


class RateList(Resource):
    @rate.marshal_list_with(model_get)
    def get(self):
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

    @rate.expect(model_post, validate=True)  # Modelo de dados esperados
    @rate.doc("Create an Item")  # Descrição para a requisição post
    def post(self):
        try:
            rate_json = (
                request.get_json()
            )  # pega tudo que está dentro do body da requisição
            rate_data = rate_schema.load(rate_json)  # Carrega o Json para um Objeto
            rate_data.save_to_db()
            return rate_schema.dump(rate_data), 201
        except ValidationError as err:
            return err.messages, 422


"""     @rate.expect([model], validate=True) # Modelo de dados esperados, com a validação ativada
    @rate.doc("Create many items") # Descrição para a requisição post
    def post(self):
        try:
            rate_json = request.get_json() # pega tudo que está dentro do body da requisição
            rate_all_data = rate_list_schema.load(rate_json) # Carrega o Json para um Objeto
            for rate_data in rate_all_data:
                rate_data.save_to_db()
            return rate_list_schema.dump(rate_all_data), 201
        except ValidationError as err:
            return  {'errors': err.messages, 'message': 'Input payload validation failed'}, 422 """
