from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
ma = Marshmallow()
db = SQLAlchemy()
class Tienda(db.Model):
    __tablename__ = 'tiendas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80))
    direccion = db.Column(db.String(300))

    def __init__(self,nombre,direccion):
        self.nombre = nombre
        self.direccion = direccion

class Inventario(db.Model):
    __tablename__ = 'inventarios'
    id = db.Column(db.Integer, primary_key=True)
    stock = db.Column(db.Integer)
    tienda_id = db.Column(db.Integer,db.ForeignKey('tiendas.id'))
    tienda = db.relationship('Tienda', backref=db.backref('tiendas', lazy='dynamic' ))
    producto_id = db.Column(db.Integer,db.ForeignKey('productos.id'))
    producto = db.relationship('Producto', backref=db.backref('productos', lazy='dynamic' ))

    def __init__(self,stock,tienda_id,producto_id):
        self.stock = stock
        self.tienda_id = tienda_id
        self.producto_id = producto_id


class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), unique=True, nullable=False)
    precio = db.Column(db.Float(precision=2))
    sku = db.Column(db.Integer)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    
    def __init__(self,nombre,precio,sku):
        
        self.nombre = nombre
        self.precio = precio
        self.sku = sku
       


class TiendaSchema(ma.Schema):
    id = fields.Integer()
    nombre = fields.String(required=True)
    direccion = fields.String(required=True)


class ProductoSchema(ma.Schema):
    id = fields.Integer()
    nombre= fields.String(required=True)
    precio = fields.Float(required=True)
    sku = fields.Integer(required=True)
    creation_date = fields.DateTime()

class InventarioSchema(ma.Schema):
    id = fields.Integer()
    stock = fields.Integer(required=True)
    tienda_id = fields.Integer(required=True)
    producto_id = fields.Integer(required=True)