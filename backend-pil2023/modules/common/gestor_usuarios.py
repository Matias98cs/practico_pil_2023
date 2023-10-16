from modules.common.gestor_comun import ResponseMessage, validaciones
from modules.models.entities import User
from sqlalchemy import or_, func

class gestor_usuarios(ResponseMessage):
    def __init__(self):
        super().__init__()

    campos_obligatorios = {
        'username': 'El nombre de usuario es obligatorio',
        'password': 'El password es obligator'
    }

    def _validar_campos_obligatorios(self, kwargs):
        for campo, mensaje in self.campos_obligatorios.items():
            if campo not in kwargs or kwargs[campo] == '':
                self.Exito = False
                self.MensajePorFallo = mensaje
                return False
        return True

    def obtener_usuario(self, username):
        user = User.query.filter_by(username=username).first()
        if user:
            self.Exito = True
            self.MensajePorFallo = "Ya existe un usuario con el mismo username"
            return self.obtenerResultado()
        else:
            self.Exito = False
            self.MensajePorFallo = ""
            return self.obtenerResultado()

    def crear_usuario(self, **kwargs):
        if not self._validar_campos_obligatorios(kwargs):
            return self.obtenerResultado()

        username = kwargs['username']
        password = kwargs['password']
        activo = 1
        nuevo_usuario = User(username=username, password=password, activo=activo)
        resultado_crear = nuevo_usuario.guardar()
        self.Resultado = resultado_crear["Resultado"]
        self.Exito = resultado_crear["Exito"]
        self.MensajePorFallo = resultado_crear["MensajePorFallo"]

        return self.obtenerResultado()
