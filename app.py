from flask import Blueprint
from flask_restful import Api
from resources.Hello import Hello
from resources.Tienda import TiendaResource
from resources.Producto import ProductoResource
from resources.Inventario import InventarioResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)
# Route
api.add_resource(Hello, '/')
api.add_resource(TiendaResource, '/Tienda')
api.add_resource(ProductoResource, '/Producto')
api.add_resource(InventarioResource,'/Inventario')