from flask_restful import Resource
from flask import current_app 

class Hello(Resource):
    """ruta que permite ver en mensaje en navejador que la api esta funcionando
    """
    def get(self):
        return "Api funcionando..."