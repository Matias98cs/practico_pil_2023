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
        formulario_data = request.form.to_dict()
        resultado = gestor_personas().editar(persona_id, **formulario_data)
        if resultado["Exito"]:
            flash('Persona actualizada correctamente', 'success')
            return redirect(url_for('routes_personas.obtener_lista_paginada'))
        else:
            flash(resultado["MensajePorFallo"], 'warning')

    resultado = gestor_personas().obtener(persona_id)
    if resultado["Exito"]:
        persona = resultado["Resultado"]
        return render_template('personas/editar_persona.html', persona=persona)
    else:
        flash(resultado["MensajePorFallo"], 'warning')
        return redirect(url_for('routes_personas.obtener_lista_paginada'))


@personas_bp.route('/personas/<int:persona_id>', methods=['POST'])
def eliminar_persona(persona_id):
    resultado = gestor_personas().eliminar(persona_id)
    if resultado["Exito"]:
        flash('Persona eliminada correctamente', 'success')
    else:
        flash('Error al eliminar persona', 'success')
    return redirect(url_for('routes_personas.obtener_lista_paginada'))


@personas_bp.route('/personas/crear', methods=['GET', 'POST'])
def crear_persona():
    formulario_data = {}
    if request.method == 'POST':
        formulario_data = request.form.to_dict()
        resultado = gestor_personas().crear(**formulario_data)
        if resultado["Exito"]:
            flash('Persona creada correctamente', 'success')
            return redirect(url_for('routes_personas.obtener_lista_paginada'))
        else:
            flash(resultado["MensajePorFallo"], 'warning')
    return render_template('personas/crear_persona.html', formulario_data=formulario_data)

