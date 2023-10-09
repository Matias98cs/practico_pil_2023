from data_base_practico.helpers.models import Universidad
from modules.common.gestor_comun import ResponseMessage, validaciones
from modules.models.entities import Persona, Genero, Pais, Provincia, Ciudad, Barrio, Lugar, Facultad, Carrera, db
from config import registros_por_pagina
from datetime import datetime
from sqlalchemy import or_

class gestor_universidad(ResponseMessage):
    def __init__(self):
        super().__init__()

    campos_obligatorios = {
        'nombre': 'El nombre es obligatorio'
    }
    
    def _validar_campos_obligatorios(self, kwargs):
        for campo, mensaje in self.campos_obligatorios.items():
            if campo not in kwargs or kwargs(campo) =="":
                self.Exito = False
                self.MensajePorFallo = mensaje
                return False
        return True
    
    def obtener_universidad(self):
        return db.session.query(Universidad).all()
