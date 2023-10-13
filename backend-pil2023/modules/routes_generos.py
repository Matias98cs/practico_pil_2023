from modules.common.gestor_generos import gestor_generos
from flask import Blueprint, render_template, flash, request, redirect, url_for, make_response
from flask import Blueprint


generos_bp = Blueprint('routes_generos', __name__)

@generos_bp.route('/generos', methods=['GET'])
def generos():
    generos = gestor_generos().obtener_todo()
    generos_data = [genero.serialize() for genero in generos]
    return {"Exito": True, "MensajePorFallo": None, "Resultado": generos_data}, 200