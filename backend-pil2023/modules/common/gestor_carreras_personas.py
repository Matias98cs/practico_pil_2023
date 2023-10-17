from modules.common.gestor_comun import ResponseMessage, validaciones
from modules.models.entities import Persona, PersonasCarreras, Carrera, Universidad, Facultad, Campus, Programa, \
    TipoPersona, db
from config import registros_por_pagina
from datetime import datetime
from sqlalchemy import or_
from sqlalchemy.orm import joinedload


class gestor_carreras_personas(ResponseMessage):
    def __init__(self):
        super().__init__()

    campos_obligatorios = {
        'universidad': 'La universidad es obligatoria',
        'campus': 'El campus es obligatorio',
        'programa': 'El programa es obligatorio',
        'facultad': 'La facultad es obligatoria',
        'tipo': 'El tipo de persona es obligatorio'
    }

    def validar_campos_obligatorios(self, kwargs):
        for campo, mensaje in self.campos_obligatorios.items():
            if campo not in kwargs or kwargs[campo] == '':
                self.Exito = False
                self.MensajePorFallo = mensaje
                return False
        return True
    
    def crear(self, **kwargs):
        if not self.validar_campos_obligatorios(kwargs):
            return self.obtenerResultado()

        tipopersona=TipoPersona.crear_y_obtener(nombre=kwargs['tipo'])
        universidad=Universidad.crear_y_obtener(nombre=kwargs['universidad'])
        facultad=Facultad.crear_y_obtener(nombre=kwargs['facultad'])
        campus=Campus.crear_y_obtener(nombre=kwargs['campus'])
        programa=Programa.crear_y_obtener(nombre=kwargs['programa'])
        carrera = Carrera.crear_y_obtener(universidad=universidad, facultad=facultad, campus=campus, programa=programa)
        persona=Persona.crear_y_obtener(id=kwargs['id_persona'])

        nueva_carrera_persona = PersonasCarreras(persona=persona, carrera=carrera, tipopersona=tipopersona)

        resultado_crear=nueva_carrera_persona.guardar()
        self.Resultado=resultado_crear['Resultado']
        self.Exito=resultado_crear['Exito']
        self.MensajePorFallo=resultado_crear['MensajePorFallo']
        
        return self.obtenerResultado()

    def editar(self, id, **kwargs):
        if not self.validar_campos_obligatorios(kwargs):
            return self.obtenerResultado()
        
        personacarrera = PersonasCarreras.query.get(id)

        if personacarrera==None:
            self.Exito=False
            self.MensajePorFallo = "La persona carrera no existe"
            return self.obtenerResultado()
        
        persona=personacarrera.persona

        universidad=personacarrera.carrera.universidad
        facultad=personacarrera.carrera.facultad
        campus=personacarrera.carrera.campus
        programa=personacarrera.carrera.programa

        if 'universidad' in kwargs:
            universidad = Universidad.crear_y_obtener(nombre=kwargs['universidad'])
        if 'facultad' in kwargs:
            facultad = Facultad.crear_y_obtener(nombre=kwargs['facultad'])
        if 'campus' in kwargs:
            campus = Campus.crear_y_obtener(nombre=kwargs['campus'])
        if 'programa' in kwargs:
            programa = Programa.crear_y_obtener(nombre=kwargs['programa'])

        carrera=Carrera.crear_y_obtener(universidad=universidad, facultad=facultad, campus=campus, programa=programa)

        tipo=personacarrera.tipopersona

        if 'tipo' in kwargs:
            tipo=TipoPersona.crear_y_obtener(nombre=kwargs['tipo'])

        personacarrera.tipopersona=tipo
        personacarrera.carrera=carrera

        resultado_guardar = personacarrera.guardar()
        self.Exito = resultado_guardar["Exito"]
        self.MensajePorFallo = resultado_guardar["MensajePorFallo"]
        return self.obtenerResultado()

    def __init__(self):
        super().__init__()

    def obtener_carreras_por_persona(self, persona):
        carreras = (
            db.session.query(PersonasCarreras)
            .filter(PersonasCarreras.persona == persona)
            # .filter(PersonasCarreras.activo == True)
            .all()
        )
        return carreras

    def obtener_pagina(self, pagina, **kwargs):
        query = PersonasCarreras.query
        if 'persona' in kwargs:
            query = query.filter(PersonasCarreras.persona == kwargs['persona'])
        carreras, total_paginas = PersonasCarreras.obtener_paginado(query, pagina, registros_por_pagina)
        return carreras, total_paginas

    def eliminar(self, id):
        carrera = PersonasCarreras.query.get(id)
        if carrera == None:
            self.Exito = False
            self.MensajePorFallo = "La carrera no existe"
            return self.obtenerResultado()
        resultado_borrar = carrera.activar(False)
        self.Exito = resultado_borrar["Exito"]
        self.MensajePorFallo = resultado_borrar["MensajePorFallo"]
        return self.obtenerResultado()