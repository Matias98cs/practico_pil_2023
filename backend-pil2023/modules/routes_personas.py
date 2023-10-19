from flask import Blueprint, render_template, flash, request, redirect, url_for, make_response
from modules.common.gestor_personas import gestor_personas
from flask import Blueprint
import json

personas_bp = Blueprint('routes_personas', __name__)


@personas_bp.route('/personas', methods=['GET'])
def obtener_lista_paginada():
    page = request.args.get('page', default=1, type=int)
    nombre = request.args.get('nombre', default="", type=str)
    apellido = request.args.get('apellido', default="", type=str)
    email = request.args.get('email', default="", type=str)
    filtros = {
        'nombre': nombre,
        'apellido': apellido,
        'email': email
    }
    personas, total_paginas = gestor_personas().obtener_pagina(page, **filtros)
    personas_data = []
    for persona in personas:
        pd = persona.serialize()
        pd["birthdate"] = persona.birthdate.isoformat()
        pd["genero"] = persona.genero.nombre
        pd["pais"] = persona.lugar.pais.nombre
        pd["provincia"] = persona.lugar.provincia.nombre
        pd["ciudad"] = persona.lugar.ciudad.nombre
        pd["barrio"] = persona.lugar.barrio.nombre
        personas_data.append(pd)
    return {'personas':personas_data, 'total_paginas':total_paginas, 'filtros':filtros}



@personas_bp.route('/personas/<int:persona_id>/editar', methods=['GET', 'POST'])
def editar_persona(persona_id):
    if request.method == 'POST':
        data = request.get_json()
        resultado = gestor_personas().editar(persona_id, **data)
        if resultado["Exito"]:
            return {"Persona": None, "resultado": "Persona actualizada correctamente"}, 200
        else:
            return {"Persona": None, "resultado": resultado['MensajePorFallo']}, 401

    resultado = gestor_personas().obtener(persona_id)
    if resultado["Exito"]:
        persona = resultado["Resultado"]
        pd = persona.serialize()
        return {"persona": pd, "resultado": "Persona encontrada"}
    else:
        return {"resultado": resultado['MensajePorFallo'], "persona": None}


@personas_bp.route('/personas/<int:persona_id>', methods=['POST'])
def eliminar_persona(persona_id):
    resultado = gestor_personas().eliminar(persona_id)
    if resultado["Exito"]:
        return {"resultado": "Persona eliminada correctamente"}, 200
    else:
        flash('Error al eliminar persona', 'success')
        return {"resultado": "Error al eliminar persona"}, 401


@personas_bp.route('/personas/crear', methods=['GET', 'POST'])
def crear_persona():
    formulario_data = {}
    if request.method == 'POST':
        formulario_data = request.get_json()
        resultado = gestor_personas().crear(**formulario_data)
        if resultado["Exito"]:
            return {"resultado": "Persona creada correctamente"}, 200
        else:
            return {"resultado": resultado['MensajePorFallo']}, 401


@personas_bp.route('/persona/<int:persona_id>', methods=['GET'])
def obtener_persona(persona_id):
    if persona_id:
        resultado = gestor_personas().obtener(persona_id)
        if resultado['Exito']:
            persona = resultado['Resultado']
            persona_data = persona.serialize()
            persona_data["birthdate"] = persona.birthdate.isoformat()
            persona_data["pais"] = persona.lugar.pais.nombre
            persona_data["provincia"] = persona.lugar.provincia.nombre
            persona_data["ciudad"] = persona.lugar.ciudad.nombre
            persona_data["barrio"] = persona.lugar.barrio.nombre
            persona_data["genero"] = persona.genero.nombre
            return {"exito": True,"persona": persona_data}, 200
        else:
            return {"exito": False,"persona": None, "msg": "No existe esa persona"}