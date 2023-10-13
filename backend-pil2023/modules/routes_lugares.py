from flask_restful import Resource
from flask import request
from modules.common.gestor_lugares import gestor_lugares
from flask import Blueprint, render_template, flash, request, redirect, url_for, make_response
from flask import Blueprint
import json

lugares_bp = Blueprint('routes_lugares', __name__)

@lugares_bp.route("/lugares/<lugar>", methods=['GET', 'POST'])
def obtener_lugares(lugar):
    if lugar == "obtener_paises":
        paises = gestor_lugares().consultar_paises()
        paises_data = []
        for item in paises:
            ps = item.serialize()
            paises_data.append(ps)
        return {"resultado": "Obteniendo paises", "paises": paises_data}, 200
    else:
        data = request.get_json()
        pais = data.get('pais')
        barrio = data.get('barrio')
        provincia = data.get('provincia')
        ciudad = data.get('ciudad')
        lugares = gestor_lugares().consultar_lugares(pais=pais, provincia=provincia, ciudad=ciudad, barrio=barrio)
        lugares_data = []
        for item in lugares:
            lg = item.serialize()
            lg["pais"] = item.pais.nombre
            lg["provincia"] = item.provincia.nombre
            lg["ciudad"] = item.ciudad.nombre
            lg["barrio"] = item.barrio.nombre
            lugares_data.append(lg)
        return {"lugares": lugares_data}, 200

    return {"resultado": "Error al obtener lugares"}, 404


@lugares_bp.route('/lugares/<lugar_type>', methods=['POST', 'GET'])
def obtener_pro_ciu_ba(lugar_type):
    if lugar_type == 'obtener_provincias':
        data = request.get_json()
        pais = data.get('pais')
        if not pais:
            return {"Exito": False, "resultado": "Debe indicar el pais", "Resultado": None}, 400

        provincias = gestor_lugares().consultar_provincias(pais=pais)
        provincias_data = [provincia.seralize() for provincia in provincias]
        return {"Exito": True, "resultado": provincias_data}, 200

    elif (lugar_type == 'obtener_ciudades'):
        data = request.get_json()
        pais = data.get('pais')
        provincia = data.get('provincia')
        if not pais or not provincia:
            return {"Exito": False, "MensajePorFallo": "Debe indicar el pais y provincia", "Resultado": None}, 400
        ciudades = gestor_lugares().consultar_ciudades(pais=pais, provincia=provincia)
        ciudades_data = [ciudad.serialize() for ciudad in ciudades]
        return {"Exito": True, "MensajePorFallo": None, "Resultado": ciudades_data}, 200
    elif (lugar_type == 'obtener_barrios'):
        data = request.get_json()
        pais = data.get('pais')
        provincia = data.get('provincia')
        ciudad = data.get('ciudad')
        if not pais or not provincia or not ciudad:
            return {"Exito": False, "MensajePorFallo": "Debe indicar el pais, provincia y ciudad",
                    "Resultado": None}, 400
        barrios = gestor_lugares().consultar_barrios(pais=pais, provincia=provincia, ciudad=ciudad)
        barrios_data = [barrio.serialize() for barrio in barrios]
        return {"Exito": True, "MensajePorFallo": None, "Resultado": barrios_data}, 200
    else:
        return {"Exito": False, "MensajePorFallo": "Recurso no definido", "Resultado": None}, 400
