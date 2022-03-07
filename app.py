from flask_restx import Resource
from api.instances.server import server
from api.instances.ma import ma 
from api.instances.database import database
from api.controllers.rate import Rate, RateList, rate

server.set_config()
app = server.app 
api = server.api
db = database.db

@app.before_first_request
def create_tables():
    db.create_all()
    
api.add_resource(Rate, '/rate/<int:id>')
api.add_resource(RateList, '/rate')       


if __name__ == "__main__":  # pragma: no cover
    db.init_app(app)
    ma.init_app(app)
    server.run()