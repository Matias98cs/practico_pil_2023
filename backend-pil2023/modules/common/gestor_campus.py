from data_base_practico.helpers.models import Campus
from modules.common.gestor_comun import ResponseMessage, validaciones
from modules.models.entities import Persona, Genero, Pais, Provincia, Ciudad, Barrio, Lugar, Facultad, Carrera, db
from config import registros_por_pagina
from datetime import datetime 
from sqlalchemy import or_


class gestor_campus(ResponseMessage):
    def __init__(self):
        super().__init__()

    campos_obligatorios = {
        'Nombre': 'El nombre es obligatorio'
    }
    
    def _validar_campos_obligatorios(self, kwargs):
        for campo, mensaje in self.campos_obligatorios.items():
            self.Exito = False
            self.MensajePorFallo = mensaje
            return False
        return True
    
    def obtener_campus(self):
        return db.session.query(Campus).distinct().join(Carrera).all()
    
    def obtener_pagina(self, pagina, **kwargs):
        query = Campus.query.filter(Campus.activo==True)
        if 'nombre' in kwargs:
            nombre = kwargs['nombre']
            query = query.filter(Campus.nombre == nombre)
        registros_por_pagina = 10
        pagina_actual = pagina

        campus_por_pagina = query.paginate(page=pagina_actual, per_page=registros_por_pagina, error_out=False)

        return campus_por_pagina.items, campus_por_pagina.total