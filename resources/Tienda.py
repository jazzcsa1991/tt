from flask import request
from flask_restful import Resource
from Model import db, Tienda, TiendaSchema
import asyncio

tiendas_schema = TiendaSchema(many=True)
tienda_schema = TiendaSchema()

class TiendaResource(Resource):
    """[Endpoint de Tienda que permite consultar, modificar,
     crear y editar uns instancia de Tienda]
        Args:
            data ([CRUD]): [recibe una peticion, get, put, delete o post]
        Returns:
            [json]: [regresa un json con la respuesta de alguno de los posibles resultado de cada peticion]"""
    
    def get(self):
        """[peticion get para la consulta de todos o del dato seleccionado ]
            Args:
                Int ([id]): [identificador de producto seleccionado para su consulta]
            Returns:
                [json]: [json con la informacion solicitada]"""
        tiendas = Tienda.query.all()
        tiendas = tiendas_schema.dump(tiendas).data
        return {'status': 'success', 'data': tiendas}, 200

    def post(self):
        """[peticion post para la creacion de una tienda]
            Args:
                Str ([nombre]): [nombre de la tienda]
                Str ([direccion]): [direccion de la tienda]
            Returns:
                [json]: [json con la informacion solicitada]"""
        json_data = request.get_json(force=True)
        print(json_data)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = tienda_schema.load(json_data)
        if errors:
            return errors, 422
        tienda = Tienda.query.filter_by(nombre=data['nombre']).first()
        if tienda:
            return {'message': 'Tienda already exists'}, 400
        tienda = Tienda(nombre=json_data['nombre'],direccion=json_data['direccion'])
        
        db.session.add(tienda)
        db.session.commit()
        result = tienda_schema.dump(tienda).data
        return { "status": 'success', 'data': result }, 201

    def put(self):
        """[peticion put para la edicion de una tienda]
            Args:
                Str ([nombre]): [nombre de la tienda]
                Str ([direccion]): [direccion de la tienda]
                Int ([id]): [identificador de la tienda]
            Returns:
                [json]: [json con la informacion solicitada]"""
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = tienda_schema.load(json_data)
        if errors:
            return errors, 422
        tienda = Tienda.query.filter_by(id=data['id']).first()
        if not tienda:
            return {'message': 'Tienda does not exist'}, 400
        tienda.nombre = data['nombre']
        db.session.commit()
        result = tienda_schema.dump(tienda).data
        
        return { "status": 'success', 'data': result}, 201

    def delete(self):
        """[peticion delete para la eliminacion  de una tienda]
            Args:
                Str ([nombre]): [nombre de la tienda]
                Str ([direccion]): [direccion de la tienda]
                Int ([id]): [identificador de la tienda]
            Returns:
                [json]: [json con la informacion solicitada]"""
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = tienda_schema.load(json_data)
        if errors:
            return errors, 422

        tienda = Tienda.query.filter_by(id=data['id']).first()
        if not tienda:
            return {'message': 'Tienda does not exist'}, 400
        tienda = Tienda.query.filter_by(id=data['id']).delete()
        db.session.commit()

        result = tienda_schema.dump(tienda).data

        return { "status": 'success', 'data': result}, 201


    

    

   
       

