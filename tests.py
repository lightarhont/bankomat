import os
import unittest
import json

from app import app, db

import views

class TestCase(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:speed1@localhost/banktest'
        self.c = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    def test_deposit(self):
        response = self.c.post('/deposit', data=dict(currency='RUB', value=100, quantity=10))
        r = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 200
        assert r['success'] == True
        response = self.c.post('/withdraw', data=dict(currency='RUB', amount=500))
        r = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 200
        assert r['success'] == True

if __name__ == '__main__':
    unittest.main()