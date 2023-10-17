# from modules.auth import jwt_or_login_required
from modules.common.gestor_carreras_personas import gestor_carreras_personas
from modules.common.gestor_personas import gestor_personas
# from modules.common.gestor_comun import gestor_comun
from modules.common.gestor_carreras import gestor_carreras
from flask import Blueprint, render_template, flash, request, redirect, url_for, make_response
from flask import Blueprint

carreras_bp = Blueprint("routes_carreras", __name__)
@carreras_bp.route("/carreras-todo/<recurso>", methods=["GET"])
def carreras_todo(recurso):
    if not recurso:
        return {"Exito": False, "MensajePorFallo": "Recurso no definido", "Resultado": None}, 400

    elif recurso == "obtener_universidades":
        print(recurso)
        universidades = gestor_carreras().obtener_universidades()

        universidades_data = []
        for cadaUna in universidades:
            pd = cadaUna.serialize()
            universidades_data.append(pd)
        return {"Exito": True, "MensajePorFallo": None, "Resultado": universidades_data}, 200

    elif recurso == "obtener_roles":
        roles = gestor_carreras().obtener_roles()

        roles_data = []
        for cadaUna in roles:
            pd = cadaUna.serialize()
            roles_data.append(pd)
        return {"Exito": True, "MensajePorFallo": None, "Resultado": roles_data}, 200

    else:
        return {"Exito": False, "MensajePorFallo": "Recurso no definido", "Resultado": None}, 400


@carreras_bp.route("/obtener_facultad_campus_programa/<recurso>", methods=["GET", "POST"])
def obtener_todo(recurso):
    if not recurso:
        return {"Exito": False, "MensajePorFallo": "Recurso no definido", "Resultado": None}, 400
    elif recurso == "obtener_facultades":
        data = request.get_json()
        universidad = data.get('universidad')
        if not universidad:
            return {"Exito": False, "MensajePorFallo": "Debe indicar una Universidad", "Resultado": None}, 400

        facultades = gestor_carreras().obtener_facultades(universidad=universidad)

        facultades_data = []
        for cadaUna in facultades:
            pd = cadaUna.serialize()
            facultades_data.append(pd)
        return {"Exito": True, "MensajePorFallo": None, "Resultado": facultades_data}, 200

    elif recurso == "obtener_campus":
        data = request.get_json()
        universidad = data.get('universidad')
        facultad = data.get('facultad')
        if not universidad or not facultad:
            return {"Exito": False, "MensajePorFallo": "Debe indicar una Universidad / Facultad",
                    "Resultado": None}, 400

        campus = gestor_carreras().obtener_campus(universidad=universidad, facultad=facultad)

        campus_data = []
        for cadaUna in campus:
            pd = cadaUna.serialize()
            campus_data.append(pd)
        return {"Exito": True, "MensajePorFallo": None, "Resultado": campus_data}, 200

    elif recurso == "obtener_programas":
        data = request.get_json()
        universidad = data.get('universidad')
        facultad = data.get('facultad')
        campus = data.get('campus')
        if not universidad or not facultad or not campus:
            return {"Exito": False, "MensajePorFallo": "Debe indicar una Universidad / Facultad / Campus",
                    "Resultado": None}, 400

        programas = gestor_carreras().obtener_programas(universidad=universidad, facultad=facultad, campus=campus)

        programas_data = []
        for cadaUna in programas:
            pd = cadaUna.serialize()
            programas_data.append(pd)
        return {"Exito": True, "MensajePorFallo": None, "Resultado": programas_data}, 200

@carreras_bp.route('/carrera-persona/<int:persona_id>', methods=['GET'])
def persona_carrera(persona_id):
    if persona_id:
        persona = gestor_personas().obtener(persona_id)
        persona_carrera = gestor_carreras_personas().obtener_carreras_por_persona(persona['Resultado'])
        carrera_persona_data = []
        for item in persona_carrera:
            pd = item.serialize()
            pd["universidad"] = item.carrera.universidad.nombre
            pd["facultad"] = item.carrera.facultad.nombre
            pd["campus"] = item.carrera.campus.nombre
            pd["programa"] = item.carrera.programa.nombre
            pd["rol"] = item.tipopersona.nombre
            carrera_persona_data.append(pd)
        return {"Exito": True, "MensajePorFallo": None, "Resultado": carrera_persona_data}, 200
    else:
        return {"Exito": False, "MensajePorFallo": "No ingreso la persona_id", "Resultado": None}, 401


@carreras_bp.route("/asignar-carrera", methods=["POST"])
def asignar_carrera():
    data = request.get_json()
    universidad = data.get('universidad')
    facultad = data.get('facultad')
    campus = data.get('campus')
    programa = data.get('programa')
    tipo = data.get('tipo')
    id_persona = data.get('id_persona')
    if not universidad or not facultad or not campus or not programa or not tipo:
        return {"Exito": False,
                "MensajePorFallo": "Debe indicar una Universidad / Facultad / Campus / Programa / Rol",
                "Resultado": None}, 400

    programas = gestor_carreras_personas().crear(universidad=universidad, facultad=facultad,
                                                 campus=campus, programa=programa, tipo=tipo,
                                                 id_persona=id_persona)
    return ({"Exito": True, "MensajePorFallo": programas['MensajePorFallo'], "Resultado": None},
            200)


@carreras_bp.route("/eliminar-carrera/<recurso>", methods=["POST"])
def eliminar_carrera(recurso):
    if not recurso:
        return {"Exito": False, "MensajePorFallo": "Recurso no definido", "Resultado": None}, 400

    elif recurso == "eliminar":
        data = request.get_json()
        carrera_persona_id = data.get('id')
        if not carrera_persona_id:
            return {"Exito": False, "MensajePorFallo": "Debe indicar una carrera", "Resultado": None}, 400

        resultado = gestor_carreras_personas().eliminar(carrera_persona_id)
        if resultado["Exito"]:
            return {"Exito": resultado["Exito"], "MensajePorFallo": resultado["MensajePorFallo"],
                    "Resultado": None}, 201
        else:
            return {"Exito": resultado["Exito"], "MensajePorFallo": resultado["MensajePorFallo"],
                    "Resultado": None}, 400


    else:
        return {"Exito": False, "MensajePorFallo": "Recurso no definido", "Resultado": None}, 400


@carreras_bp.route("/editar-carrera", methods=["POST"])
def editar_carrera():
    data = request.get_json()
    carrera_id = data.get("carrera_id")
    campos = {
        "universidad": data.get('universidad'),
        "facultad": data.get('facultad'),
        "campus": data.get('campus'),
        "programa": data.get('programa'),
        "tipo": data.get('tipo')
    }
    if all(value is not None for value in campos.values()):
        persona_carrera = gestor_carreras_personas().editar(carrera_id, **campos)
        if persona_carrera['Exito']:
            return {"Exito": persona_carrera["Exito"], "MensajePorFallo": persona_carrera["MensajePorFallo"],
                    "Resultado": None}, 201
        else:
            return {"Exito": False, "MensajePorFallo": persona_carrera['MensajePorFallo'], "Resultado": None}, 400
    else:
        return {"Exito": False, "MensajePorFallo": "Al menos un campo no tiene datos", "Resultado": None}, 400
