import os
from flask import Flask
from flask_restful import Api
from config import db_connector, db_user, db_password, db_ip_address, db_name
from modules.apis.personas import PersonasResource
from modules.apis.lugares import LugaresResource
from modules.apis.generos import GenerosResource
from modules.apis.carreras import CarrerasResource
from modules.models.base import db
# from modules.routes_personas import personas_bp


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"{db_connector}://{db_user}:{db_password}@{db_ip_address}/{db_name}"
    db.init_app(app)
    api = Api(app)

    with app.app_context():
        db.create_all()

    # app.register_blueprint(personas_bp)
    api.add_resource(PersonasResource, '/api/personas', '/api/personas/<int:persona_id>')
    api.add_resource(LugaresResource, '/api/lugares', '/api/lugares/<string:lugar_type>')
    api.add_resource(CarrerasResource, '/api/carreras', '/api/carreras/<string:recurso>')
    api.add_resource(GenerosResource, '/api/generos')

    return app