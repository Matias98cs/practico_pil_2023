import json

from flask_restful import Resource
from flask import request, jsonify, make_response
from modules.common.gestor_personas import gestor_personas
# from modules.auth import jwt_or_login_required


class PersonasResource(Resource):

    def get(self, persona_id=None):
        if persona_id is None:
            data = request.get_json()
            print(data)
            pagina = data.get('pagina')
            filtros = data.get('filtros', {})
            personas, total_paginas = gestor_personas().obtener_pagina(pagina, **filtros)
            personas_data = []
            for persona in personas:
                persona_dic = {
                    "birthdate": persona.birthdate.isoformat(),
                    "genero": persona.genero.nombre,
                    "pais": persona.lugar.pais.nombre,
                    "provincia": persona.lugar.provincia.nombre,
                    "ciudad": persona.lugar.ciudad.nombre,
                    "barrio": persona.lugar.barrio.nombre
                }
                personas_data.append(persona_dic)
                print(personas_data)
            # for persona in personas:
            #     pd = persona.serialize()
            #     print(pd)
            #     # pd["birthdate"] = persona.birthdate.isoformat()
            #     # pd["genero"] = persona.genero.nombre
            #     # pd["pais"] = persona.lugar.pais.nombre
            #     # pd["provincia"] = persona.lugar.provincia.nombre
            #     # pd["ciudad"] = persona.lugar.ciudad.nombre
            #     # pd["barrio"] = persona.lugar.barrio.nombre
            #     personas_data.append(pd)

            # response_data = {
            #     "Exito": True,
            #     "MensajePorFallo": "",
            #     "Resultado": personas_data,
            #     "TotalPaginas": total_paginas
            # }
            # # response_data = json.dumps(response_data)
            response = make_response(personas_data, 200)
            response.headers['Content-Type'] = 'application/json'
            return response
            # return ({"message": "Datos recibidos correctamente"}), 200
            return {"Exito": True, "MensajePorFallo": "", "Resultado": personas_data,
                    "TotalPaginas": total_paginas}, 200
        else:
            resultado = gestor_personas().obtener(persona_id)
            if resultado["Exito"]:
                persona = resultado["Resultado"]
                persona_data = persona.serialize()
                persona_data["birthdate"] = persona.birthdate.isoformat()
                persona_data["pais"] = persona.lugar.pais.nombre
                persona_data["provincia"] = persona.lugar.provincia.nombre
                persona_data["ciudad"] = persona.lugar.ciudad.nombre
                persona_data["barrio"] = persona.lugar.barrio.nombre
                return {"Exito": resultado["Exito"], "MensajePorFallo": resultado["MensajePorFallo"],
                        "Resultado": persona_data}, 200
            else:
                return {"Exito": resultado["Exito"], "MensajePorFallo": resultado["MensajePorFallo"],
                        "Resultado": None}, 400

    def post(self):
        args = request.get_json()
        resultado = gestor_personas().crear(**args)
        if resultado["Exito"]:
            persona = resultado["Resultado"]
            persona_data = persona.serialize()
            persona_data["birthdate"] = persona.birthdate.isoformat()
            persona_data["pais"] = persona.lugar.pais.nombre
            persona_data["provincia"] = persona.lugar.provincia.nombre
            persona_data["ciudad"] = persona.lugar.ciudad.nombre
            persona_data["barrio"] = persona.lugar.barrio.nombre
            return {"Exito": resultado["Exito"], "MensajePorFallo": resultado["MensajePorFallo"],
                    "Resultado": persona_data}, 201
        else:
            return {"Exito": resultado["Exito"], "MensajePorFallo": resultado["MensajePorFallo"],
                    "Resultado": None}, 400

    def put(self):
        args = request.get_json()
        resultado = gestor_personas().editar(**args)
        if resultado["Exito"]:
            return {"Exito": resultado["Exito"], "MensajePorFallo": resultado["MensajePorFallo"],
                    "Resultado": None}, 201
        else:
            return {"Exito": resultado["Exito"], "MensajePorFallo": resultado["MensajePorFallo"],
                    "Resultado": None}, 400

    def delete(self, persona_id):
        resultado = gestor_personas().eliminar(persona_id)
        if resultado["Exito"]:
            return {"Exito": resultado["Exito"], "MensajePorFallo": resultado["MensajePorFallo"],
                    "Resultado": None}, 201
        else:
            return {"Exito": resultado["Exito"], "MensajePorFallo": resultado["MensajePorFallo"],
                    "Resultado": None}, 400
