from flask_restx import Resource, fields
from flask import request

from api.models.rate import RateModel, TypeRate
from api.schemas.rate import RateSchema

from api.instances.server import server


api = server.api
rate = api.namespace(name="Rating", description="Rating related Operations", path="/rate")

rate_schema = RateSchema()  # Seraliza um Objeto
rate_list_schema = RateSchema(many=True)  # Serializa múltiplos Objetos


model = rate.model(
    "Model",
    {
        "title": fields.String(
            required=True, max_length=255, description="Title of Rate"
        ),
        "content": fields.String(description="Your Opinion about this title."),
        "rate_type": fields.String(
            required=True, enum=[tr.value for tr in TypeRate], default="Movie"
        ),
        "rate": fields.Integer(min=1, max=5, required=True, description="Your rate level"),
    },
)


class Rate(Resource):
    @rate.marshal_with(model)
    def get(self, id):
        return RateModel.find_by_id(id)
    

class RateList(Resource):
    
    def get(self, ):
        return rate_list_schema.dump(RateModel.find_all()), 200
    
    @rate.expect(model) # Modelo de dados esperados
    @rate.doc("Create an Item") # Descrição para a requisição post
    def post(self, ):
        rate_json = request.get_json() # pega tudo que está dentro do body da requisição
        rate_data = rate_schema.load(rate_json)
        rate_data.save_to_db()
        return rate_schema.dump(rate_data), 201