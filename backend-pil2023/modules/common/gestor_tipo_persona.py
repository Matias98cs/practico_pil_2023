from modules.models.entities import Persona, TipoPersona, db
from modules.common.gestor_comun import ResponseMessage

class gestor_tipo_persona(ResponseMessage):
    def __init__(self):
        super().__init__()

    def obtener_TipoPersonas(self):
        return TipoPersona.obtener_todo()