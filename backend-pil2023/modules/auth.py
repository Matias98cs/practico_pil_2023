from flask import redirect, url_for, request, flash, render_template, abort, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from modules.models.entities import User
from flask import Blueprint
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_jwt_extended import create_access_token, jwt_required
from flask_wtf.csrf import CSRFProtect
from functools import wraps
import json

auth_bp = Blueprint('auth', __name__)

login_manager = LoginManager()
csrf = CSRFProtect()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/sing-up', methods=['POST'])
@csrf.exempt
def sign_up():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    activo = 1
    try:
        if username and password:
            print('Datos correctamente')
            user = User(username=username, password=password, activo=activo)
            user.guardar()
            print('Usuario creado correctamente')
            return {"msg": "Usuario creado correctamente"}, 200
        else:
            print('Faltan datos')
            return {"msg": "Faltan datos para crear el usuario"}, 401

    except Exception as e:
        print(f'Hubo un error al crear un usuario: {e}')
        return {"msg": "Error al crear un usuario"}, 400

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
            "activo": user.activo
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
