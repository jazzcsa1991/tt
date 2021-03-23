import unittest
import json

from app import api
from flask_sqlalchemy import SQLAlchemy
from run import create_app

db = SQLAlchemy()

class TestInventarioApi(unittest.TestCase):
    """[Test de algunas de las funcionalidades de de la instancia de inventario]

    Case:
        setUpClass : [se preprara la aplicacion para ejecuatr las prueba de los difrerentes casos]
        test_postTest : [test que verifica la creacion exitosa de una instancia de inventario]
        test_putTest : [test que verifica la edicion de uns instancia de invebtario existosa]
        test_postTestDuplicate : [test que verifica la prohibicion de crear un inventario existente]
    """
    
    @classmethod
    def setUpClass(self):
        print('### Setting up flask server ###')
        app = create_app("config")
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_postTest(self):
        data = json.dumps({
            "stock":2,
            "tienda_id":1,
            "producto_id":1
            })
        response = self.app.post('/api/Inventario',headers={"Content-Type":"application/json"},data=data)
        self.assertEqual('201 CREATED', response.status)

    def test_putTest(self):
        data = json.dumps({
            "id":1,
            "stock":5,
            "tienda_id":0,
            "producto_id":0
            })

        response = self.app.put('api/Inventario',headers={"Content-Type":"application/json"},data=data)

        self.assertEqual('201 CREATED', response.status)
    
    def test_postTestDuplicate(self):
        data = json.dumps({
            "stock":2,
            "tienda_id":1,
            "producto_id":1
        })

        response = self.app.post('/api/Inventario',headers={"Content-Type":"application/json"},data=data)
        
        self.assertEqual('400 BAD REQUEST', response.status)
    