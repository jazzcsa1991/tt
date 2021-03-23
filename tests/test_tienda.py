import unittest
import json
from app import api
from flask_sqlalchemy import SQLAlchemy
from run import create_app

db = SQLAlchemy()

class TestTiendaApi(unittest.TestCase):
    """[Test de algunas de las funcionalidades de de la instancia de tienda]

    Case:
        setUpClass : [se preprara la aplicacion para ejecuatr las prueba de los difrerentes casos]
        test_postTest : [test que verifica la creacion exitosa de una instancia de tienda]
        test_putTest : [test que verifica la edicion de uns instancia de tienda existosa]
        test_deleteTest : [test que verifica la prohibicion de eliminar  una tienda que no existe]
    """

    @classmethod
    def setUpClass(self):
        
        print('### Setting up flask server ###')
        app = create_app("config")
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_postTest(self):
        
        cases = [{
            "nombre":"prueba test",
            "direccion":"direcccion de prueba"
            },{
            "nombre":"prueba test2",
            "direccion":"direcccion de prueba2"
            }]

        for case in cases:
            data = json.dumps(case)
            response = self.app.post('/api/Tienda',headers={"Content-Type":"application/json"},data=data)
            self.assertEqual('201 CREATED', response.status)

    def test_putTest(self):
        
        data = json.dumps({
            "id":2,
            "nombre":"cambio",
            "direccion":"direcccion de prueba15"
        })

        response = self.app.put('/api/Tienda',headers={"Content-Type":"application/json"},data=data)
        
        self.assertEqual('201 CREATED', response.status)

    def test_deleteTest(self):
        data = json.dumps({
            "id":10,
            "nombre":"",
            "direccion":""
        })
        
        response = self.app.delete('/api/Tienda',headers={"Content-Type":"application/json"},data=data)
        
        self.assertEqual('400 BAD REQUEST', response.status)
    


