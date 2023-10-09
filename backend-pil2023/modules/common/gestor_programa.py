from data_base_practico.helpers.models import Programa
from modules.common.gestor_comun import ResponseMessage, validaciones
from modules.models.entities import Persona, Genero, Pais, Provincia, Ciudad, Barrio, Lugar, Facultad, Carrera, db
from config import registros_por_pagina
from datetime import datetime 
from sqlalchemy import or_


class gestor_programa(ResponseMessage):
    def __init__(self):
        super().__init__()

    campos_obligatorios = {
        'nombre': 'El nombre es obligatorio'
    }
    
    def _validar_campos_obligatorios(self, kwargs):
        for campo, mensaje in self.campos_obligatorios.items():
            self.Exito = False
            self.MensajePorFallo = mensaje
            return False
        return True
    
    def obtener_programa(self):
        return db.session.query(Programa).distinct().join(Carrera).all()
    
    def obtener_pagina(self, pagina, **kwargs):
        query = Programa.query.filter(Programa.activo==True)
        if 'nombre' in kwargs:
            nombre = kwargs['nombre']
            query = query.filter(Programa.nombre == nombre)
        registros_por_pagina = 10
        pagina_actual = pagina

        programa_por_pagina = query.paginate(page=pagina_actual, per_page=registros_por_pagina, error_out=False)

        return programa_por_pagina.items, programa_por_pagina.total