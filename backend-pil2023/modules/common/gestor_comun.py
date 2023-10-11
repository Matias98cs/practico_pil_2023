import re
from openpyxl import Workbook
from flask import send_file
import io

class ResponseMessage:
    def __init__(self, Resultado=None, Exito=True, MensajePorFallo=""):
        self.Resultado = Resultado
        self.Exito = Exito
        self.MensajePorFallo = MensajePorFallo

    def obtenerResultado(self):
        return {
            "Resultado": self.Resultado,
            "Exito": self.Exito,
            "MensajePorFallo": self.MensajePorFallo
        }


class validaciones:
    def validar_estructura_email(email):
        # Definir la expresión regular para validar el email
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        # Usar re.match para verificar si el email coincide con el patrón
        if re.match(patron, email):
            return True
        else:
            return False


class exportar:
    def exportar_excel(datos):
        wb = Workbook()
        ws = wb.active

        headers = list(datos[0].keys())
        ws.append(headers)

        for item in datos:
            ws.append(list(item.values()))

        excel_data = io.BytesIO()
        wb.save(excel_data)
        excel_data.seek(0)

        response_headers = {
            'Content-Disposition': 'attachment; filename=reporte.xlsx',
            'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        }

        return excel_data.read(), 200, response_headers