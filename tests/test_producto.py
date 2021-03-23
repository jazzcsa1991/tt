import unittest
import json

from app import api
from flask_sqlalchemy import SQLAlchemy
from run import create_app

db = SQLAlchemy()

class TestProductoApi(unittest.TestCase):
    """[Test de algunas de las funcionalidades de de la instancia de producto]

    Case:
        setUpClass : [se preprara la aplicacion para ejecuatr las prueba de los difrerentes casos]
        test_postTest : [test que verifica la creacion exitosa de una instancia de prodcuto]
        test_putTest : [test que verifica la edicion de uns instancia de producto existosa]
        test_deleteTest : [test que verifica la prohibicion de eliminar  un prodcuto que no existe]
    """
    
    @classmethod
    def setUpClass(self):
        print('### Setting up flask server ###')
        app = create_app("config")
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_postTest(self):
        data = json.dumps({
            "nombre":"prueba test",
            "precio":123.45,
            "sku":234
            })
        response = self.app.post('/api/Producto',headers={"Content-Type":"application/json"},data=data)
        self.assertEqual('201 CREATED', response.status)

    def test_putTest(self):
        data = json.dumps({
            "id":1,
            "nombre":"cambio de nombre",
            "precio":123.45,
            "sku":234
            })

        response = self.app.put('api/Producto',headers={"Content-Type":"application/json"},data=data)

        self.assertEqual('201 CREATED', response.status)
    
    def test_deleteTest(self):
        data = json.dumps({
            "id":10,
            "nombre":"",
            "precio":0,
            "sku":0
        })

        response = self.app.delete('/api/Producto',headers={"Content-Type":"application/json"},data=data)
        
        self.assertEqual('400 BAD REQUEST', response.status)
    