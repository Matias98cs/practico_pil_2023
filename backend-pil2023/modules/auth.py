from flask import redirect, url_for, request, flash, render_template, abort, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from modules.models.entities import User
from flask import Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_jwt_extended.exceptions import JWTDecodeError
from flask_wtf.csrf import CSRFProtect
from functools import wraps
from modules.common.gestor_usuarios import gestor_usuarios
from flask_restful import Resource

auth_bp = Blueprint('auth', __name__)

login_manager = LoginManager()
csrf = CSRFProtect()

# class UsuariosResource(Resource):
#     def post(self):
#         data = request.get_json()
#         username = data.get('username')
#         print(f"Username: {username}")
#         resultado = gestor_usuarios().obtener_usuario(username)
#         if resultado['Exito']:
#             return {"Exito": resultado["Exito"], "MensajePorFallo": resultado['MensajePorFallo'],
#                     "Resultado": None}, 400
#         else:
#             args = request.get_json()
#             crear_usuario = gestor_usuarios().crear_usuario(**args)
#             return {"Exito": crear_usuario["Exito"], "MensajePorFallo": "Usuario creado correctamente",
#                     "Resultado": None}, 200


@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = None
    jwt_identity = get_jwt_identity()
    try:
        if jwt_identity:
            current_user = jwt_identity
            return jsonify(logged_in_as=current_user), 200
        else:
            return jsonify({"message": "Token de acceso no válido"}), 401
    except JWTDecodeError:
        print(f"Error de Token")

@auth_bp.route('/perfil', methods=['GET'])
@csrf.exempt
@jwt_required()
def perfil():
    try:
        current_user = get_jwt_identity()
        username = current_user
        user = User.query.filter_by(username=username).first()
        if username:
            user_send = {
                "username": user.username,
                "dni": user.persona_id,
                "fecha_alta": user.fecha_alta,
                "activo": user.activo,
                "id": user.id
            }
            return {"user": user_send}, 200
        else:
            return {"msg": "Error de access token"}, 400
    except Exception as e:
        print(f"Hubo un error al encontrar el usuario: {e}")
        return {"msg": f"Error al encontrar el usuario : {e}"}


@auth_bp.route('/login-jwt', methods=['POST'])
@csrf.exempt
def login_jwt():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):

        user_send = {
            "username": user.username,
            "dni": user.persona_id,
            "fecha_alta": user.fecha_alta,
            "activo": user.activo,
            "id": user.id
        }
        access_token = create_access_token(identity=username)
        return {"user": user_send, "access_token": access_token}, 200
    else:
        return {"user": None, "access_token": None, "msg": "Credenciales invalidas"}, 401


def jwt_or_login_required():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                jwt_required()(lambda: None)()
            except:
                if current_user.is_authenticated:
                    return f(*args, **kwargs)
                return {"message": "Acceso no autorizado"}, 401
            return f(*args, **kwargs)

        return decorated_function

    return decorator
