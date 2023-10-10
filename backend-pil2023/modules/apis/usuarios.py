from flask import redirect, url_for, request, flash, render_template, abort, jsonify
from modules.models.entities import User
from modules.common.gestor_usuarios import gestor_usuarios
from flask_restful import Resource

class UsuariosResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        resultado = gestor_usuarios().obtener_usuario(username)
        if resultado['Exito']:
            return jsonify({"Exito": False, "Resultado": None, "msg": "Username duplicado, no se puede crear un usario existente"})
        else:
            args = request.get_json()
            crear_usuario = gestor_usuarios().crear_usuario(**args)
            return jsonify({"Exito": True, "Resultado": None, "msg": "Usuario creado correctamente"})
