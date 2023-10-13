import os
from flask_cors import CORS
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from modules.auth import auth_bp, login_manager
from modules.rutas_exel import reportes_exel
from modules.auth import csrf
from config import db_connector, db_user, db_password, db_ip_address, db_name
from modules.apis.personas import PersonasResource
from modules.models.entities import User
from modules.apis.lugares import LugaresResource
from modules.apis.generos import GenerosResource
from modules.apis.carreras import CarrerasResource
from modules.apis.tipo_persona import TipoPersonaResource
from modules.apis.usuarios import UsuariosResource
from modules.models.base import db
from modules.routes_personas import personas_bp
from modules.routes_lugares import lugares_bp
from modules.routes_generos import generos_bp


def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"{db_connector}://{db_user}:{db_password}@{db_ip_address}/{db_name}"
    db.init_app(app)
    # csrf.init_app(app)
    CORS(app, resources={r"//*": {"origins": "http://localhost:5173", "methods": "GET" "POST" "PUT" "DELETE"}})
    api = Api(app, decorators=[csrf.exempt])
    jwt = JWTManager(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()
        # usuario = User(username=os.getenv("DEFAULT_USER"), password=os.getenv("DEFAULT_PASSWORD"), activo=1)
        # usuario.guardar()

    app.register_blueprint(auth_bp)
    app.register_blueprint(reportes_exel)
    app.register_blueprint(personas_bp)
    app.register_blueprint(lugares_bp)
    app.register_blueprint(generos_bp)
    # # api.add_resource(UsuariosResource, '/api/usuario', '/api/usuario/<int:username>')
    # api.add_resource(PersonasResource, '/api/personas', '/api/personas/<int:persona_id>')
    # api.add_resource(LugaresResource, '/api/lugares', '/api/lugares/<string:lugar_type>')
    # api.add_resource(CarrerasResource, '/api/carreras', '/api/carreras/<string:recurso>')
    # api.add_resource(TipoPersonaResource,  '/api/tipo-persona')
    # api.add_resource(GenerosResource, '/api/generos')


    return app