from flask_restful import Resource
from flask import request
from modules.common.gestor_tipo_persona import gestor_tipo_persona

class TipoPersonaResource(Resource):
    def get(self):
        roles = []
        tipo_persona_rol = gestor_tipo_persona().obtener_TipoPersonas()
        for tipo in tipo_persona_rol:
            roles.append(tipo.nombre)

        return {"tipo_persona": roles}