from flask import request
import json
from flask_restful import Resource
from Model import db, Producto, ProductoSchema
import asyncio

productos_schema = ProductoSchema(many=True)
producto_schema = ProductoSchema()

class ProductoResource(Resource):
    """[Endpoint de productos que permite consultar, modificar,
     crear y editar uns instancia de Producto]
        Args:
            data ([CRUD]): [recibe una peticion, get, put, delete o post]
        Returns:
            [json]: [regresa un json con la respuesta de alguno de los posibles resultado de cada peticion]"""
 
    def get(self,id=None):
        """[peticion get para la consulta de todos o del dato seleccionado ]
            Args:
                Int ([id]): [identificador de producto seleccionado para su consulta]
            Returns:
                [json]: [json con la informacion solicitada]"""
        id = request.args.get('id')
        if id:
            productos = Producto.query.get(id)
            productos = producto_schema.dump(productos).data
            return {'status': 'success', 'data': productos}, 200
        else:
            productos = Producto.query.all()
            productos = productos_schema.dump(productos).data
            return {'status': 'success', 'data': productos}, 200

    def post(self):
        """[peticion post para la creacion de un producto ]
            Args:
                Str ([nombre]): [nombre del producto]
                Float ([precio]): [precio del prodcuto]
                Int ([sku]): [identificador sku del producto]
            Returns:
                [json]: [json con la informacion solicitada]"""
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = producto_schema.load(json_data)
        if errors:
            return errors, 422
        producto = Producto.query.filter_by(nombre=data['nombre']).first()
        if producto:
            return {'message': 'producto already exists'}, 400
        producto = Producto(nombre=json_data['nombre'],precio=json_data['precio'],sku=json_data['sku'])
        
        db.session.add(producto)
        db.session.commit()
        result = producto_schema.dump(producto).data
        return { "status": 'success', 'data': result }, 201

    def put(self):
        """[peticion put para la edicion de un producto ]
            Args:
                Str ([nombre]): [nombre del producto]
                Float ([precio]): [precio del prodcuto]
                Int ([sku]): [identificador sku del producto]
                Int ([id]): [identificador  del producto]
            Returns:
                [json]: [json con la informacion solicitada]"""
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = producto_schema.load(json_data)
        if errors:
            return errors, 422
        producto = Producto.query.filter_by(id=data['id']).first()
        if not producto:
            return {'message': 'producto does not exist'}, 400
        producto.nombre = data['nombre']
        db.session.commit()
        result = producto_schema.dump(producto).data
        
        return { "status": 'success', 'data': result}, 201

    def delete(self):
        """[peticion delete para la eliminacion de un producto ]
            Args:
                Str ([nombre]): [nombre del producto]
                Float ([precio]): [precio del prodcuto]
                Int ([sku]): [identificador sku del producto]
                Int ([id]): [identificador  del producto]
            Returns:
                [json]: [json con la informacion solicitada]"""
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = producto_schema.load(json_data)
        if errors:
            return errors, 422

        producto = Producto.query.filter_by(id=data['id']).first()
        if not producto:
            return {'message': 'producto does not exist'}, 400
        producto = producto.query.filter_by(id=data['id']).delete()
        db.session.commit()

        result = producto_schema.dump(producto).data

        return { "status": 'success', 'data': result}, 201


    