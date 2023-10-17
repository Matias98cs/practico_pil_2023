from modules.common.gestor_comun import ResponseMessage, validaciones
from modules.models.entities import (Persona, Carrera, Universidad, Facultad, Campus, Programa, TipoPersona,
                                     PersonasCarreras, db)
from config import registros_por_pagina

class gestor_carreras(ResponseMessage):
    def __init__(self):
        super().__init__()

    def obtener_universidades(self):
        return db.session.query(Universidad).distinct().join(Carrera).all()

    def obtener_facultades(self, **kwargs):
        resultado = (
            db.session.query(Facultad)
            .distinct()
            .join(Carrera)
            .join(Universidad)
            .filter(Universidad.nombre == kwargs["universidad"])
            .all()
        )
        return resultado

    def obtener_campus(self, **kwargs):
        resultado = (
            db.session.query(Campus)
            .distinct()
            .join(Carrera)
            .join(Universidad)
            .join(Facultad)
            .filter(Universidad.nombre == kwargs["universidad"])
            .filter(Facultad.nombre == kwargs["facultad"])
            .all()
        )
        return resultado

    def obtener_programas(self, **kwargs):
        resultado = (
            db.session.query(Programa)
            .distinct()
            .join(Carrera)
            .join(Universidad)
            .join(Facultad)
            .join(Campus)
            .filter(Universidad.nombre == kwargs["universidad"])
            .filter(Facultad.nombre == kwargs["facultad"])
            .filter(Campus.nombre == kwargs["campus"])
            .all()
        )
        return resultado

    def obtener_roles(self, **kwargs):
        resultado = (
            db.session.query(TipoPersona).all()
        )
        return resultado


    def obtener_pagina(self, pagina, **kwargs):
        query = PersonasCarreras.query.filter_by(persona_id=kwargs["persona_id"])
        if 'programa' in kwargs:
            query = query.join(Carrera).join(Programa).filter(Programa.nombre.ilike(f"%{kwargs['programa']}%"))
        if 'facultad' in kwargs:
            query = query.join(Facultad).filter(Facultad.nombre.ilike(f"%{kwargs['facultad']}%"))
        if 'universidad' in kwargs:
            query = query.join(Universidad).filter(Universidad.nombre.ilike(f"%{kwargs['universidad']}%"))

        carreras, total_paginas = PersonasCarreras.obtener_paginado(query, pagina, registros_por_pagina)
        return carreras, total_paginas


    def obtener_todo(self):
        return Carrera.obtener_todo()

    def obtener_todo_facultades(self):
        return Facultad.obtener_todo()

    def obtener_todo_campus(self):
        return Campus.obtener_todo()

    def obtener_todo_programa(self):
        return Programa.obtener_todo()