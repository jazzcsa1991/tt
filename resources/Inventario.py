from flask import request
from flask_restful import Resource
from Model import db, Inventario, InventarioSchema, Tienda, Producto
import asyncio

inventarios_schema = InventarioSchema(many=True)
inventario_schema = InventarioSchema()

class InventarioResource(Resource):
    """[Endpoint de inventario que permite consultar, modificar,
     crear y editar uns instancia de Inventario]
        Args:
            data ([CRUD]): [recibe una peticion, get, put, delete o post]
        Returns:
            [json]: [regresa un json con la respuesta de alguno de los posibles resultado de cada peticion]"""
    def get(self,id=None):
        
        """[peticion get para la consulta de todos o del dato seleccionado ]
            Args:
                Int ([id]): [identificador de inventario seleccionado para su consulta]
            Returns:
                [json]: [json con la informacion solicitada]"""
        id = request.args.get('id')
        if id:
            inventarios = Inventario.query.get(id)
            inventarios = inventario_schema.dump(inventarios).data
            return {'status': 'success', 'data': inventarios}, 200
        else:
            inventarios = Inventario.query.all()
            inventarios = inventarios_schema.dump(inventarios).data
            return {'status': 'success', 'data': inventarios}, 200

    def post(self):
        """[peticion post para la creacion de un inventario a partir de una funciona asincrona]
            Args:
                Int ([stock]): [numero de piezas que el producto tiene o tendra disponible]
                Int ([tienda_id]): [identificador de la instancia de tienda a la que pertencece el inventario]
                Int ([producto_id]): [identificador de la instancia de producto a la que hace referencia el inventario]
            Returns:
                [json]: [json con la informacion solicitada]"""

        async def create(data):
            inventario = Inventario.query.filter_by(tienda_id=data['tienda_id'],producto_id=data['producto_id']).first()
            if inventario:
                return {'message': 'Inventario already exists'}, 400
            inventario = Inventario(producto_id=data['producto_id'],tienda_id=data['tienda_id'],stock=data['stock'])
            result = inventario_schema.dump(inventario).data
            db.session.add(inventario)
            db.session.commit()
            return { "status": 'success', 'data': result }, 201

        json_data = request.get_json(force=True)
        
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = inventario_schema.load(json_data)
        if errors:
            return errors, 422
        
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(create(data))
        return result
        

    def put(self):
        """[peticion put para la edicion de un inventario a partir de una funciona asincrona]
            Args:
                Int ([stock]): [numero de piezas que el producto tiene o tendra disponible]
                Int ([tienda_id]): [identificador de la instancia de tienda a la que pertencece el inventario]
                Int ([producto_id]): [identificador de la instancia de producto a la que hace referencia el inventario]
            Returns:
                [json]: [json con la informacion solicitada]"""

        async def change(data):
            inventario = Inventario.query.filter_by(id=data['id']).first()
            if not inventario:
                return {'message': 'inventario does not exist'}, 400
            inventario.stock = data['stock']
            db.session.commit()
            result = inventario_schema.dump(inventario).data
        
            return { "status": 'success', 'data': result}, 201

        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = inventario_schema.load(json_data)
        if errors:
            return errors, 422
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(change(data))
        return result
        

    def delete(self):
        """[peticion delete para la eliminacion de un inventario a partir de una funciona asincrona]
            Args:
                Int ([stock]): [numero de piezas que el producto tiene o tendra disponible]
                Int ([tienda_id]): [identificador de la instancia de tienda a la que pertencece el inventario]
                Int ([producto_id]): [identificador de la instancia de producto a la que hace referencia el inventario]
            Returns:
                [json]: [json con la informacion solicitada]"""

        async def delete(data):
            inventario = Inventario.query.filter_by(id=data['id']).first()
            if not inventario:
                return {'message': 'Inventario does not exist'}, 400
            inventario = Inventario.query.filter_by(id=data['id']).delete()
            db.session.commit()

        result = inventario_schema.dump(inventario).data

        return { "status": 'success', 'data': result}, 201

        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = inventario_schema.load(json_data)
        if errors:
            return errors, 422

        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(delete(data))
        return result

        


    

    