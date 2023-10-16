from flask import redirect, url_for, request, flash, render_template, abort, jsonify
from modules.models.entities import User
from modules.common.gestor_usuarios import gestor_usuarios
from flask import Blueprint, render_template, flash, request, redirect, url_for, make_response
from flask import Blueprint

usuarios_bp = Blueprint('routes_usuarios', __name__)

@usuarios_bp.route('/crear-usuario', methods=['POST'])
def crear_usuarios():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    encontrar_persona = gestor_usuarios().obtener_usuario(username)
    if encontrar_persona['Exito']:
        return {"msg": "El username ya esta en uso"}, 401
    else:
        if username and password:
            crear_usuario = gestor_usuarios().crear_usuario(**data)
            return {"msg": "Usuario creado correctamente"}, 200
        else:
            return {"msg": "Ingrese el username y password"}, 401