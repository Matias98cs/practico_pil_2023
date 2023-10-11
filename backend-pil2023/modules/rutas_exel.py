from flask import Blueprint, request
from modules.common.gestor_personas import gestor_personas
from modules.common.gestor_comun import exportar

reportes_exel = Blueprint('routes_reportes', __name__)

@reportes_exel.route('/personas/generar_exel', methods=['POST', 'GET'])
def generar_exel_personas():
    personas=gestor_personas().obtener_todo()
    personas_data=[]
    for persona in personas:
        pd={}
        pd["Nombre"] = persona.nombre
        pd["Apellido"] = persona.apellido
        pd["email"] = persona.email
        pd["Edad"] = persona.age
        pd["Fecha nacimiento"]=persona.birthdate.strftime('%d/%m/%Y')
        pd["Genero"]=persona.genero.nombre
        pd["Pais"]=persona.lugar.pais.nombre
        pd["Provincia"]=persona.lugar.provincia.nombre
        pd["Ciudad"]=persona.lugar.ciudad.nombre
        pd["Barrio"]=persona.lugar.barrio.nombre
        personas_data.append(pd)

    return exportar.exportar_excel(personas_data)