import os
import sys
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movie, Actor, db_drop_and_create_all
from app import create_app

sys.path.insert(0, '..')

class CastingAgencyTestCase(unittest.TestCase):
    #This class represents the Casting Agency test case

    def setUp(self):
        #Define test variables and initialize app.
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "castingagency"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)

        # self.assistent = os.getenv('ASSISTANT_TOKEN')
        # self.director = os.getenv('DIRECTOR_TOKEN')
        # self.producer = os.getenv('PRODDUCER_TOKEN')

        setup_db(self.app, self.database_path)

        self.casting_assistant = {
            "Authorization": "Bearer {}".format(os.environ.get('ASSISTANT_TOKEN'))
        }
        self.casting_director = {
            "Authorization": "Bearer {}".format(os.environ.get('DIRECTOR_TOKEN'))
        }
        self.casting_producer = {
            "Authorization": "Bearer {}".format(os.environ.get('PRODDUCER_TOKEN'))
        }


    
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        #Executed after each test
        pass

    # General Test - Server status
    def test_server_status(self):
        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

# GET Endpoints: 

    #GET Actors
    def test_get_actors(self):
        res = self.client().get('/actors', headers={'Authorization': 'Bearer ' + str(self.casting_assistant)})
                             
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    #GET Actors Fail
    def test_401_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    #GET Movies
    def test_get_movies(self):
        res = self.client().get('movies',
                                headers={'Authorization': 'Bearer '
                                         + str(self.casting_assistant)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    #GET Movies Fail
    def test_401_get_movies(self):
        res = self.client().get('/movies',
                                headers={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == '__main__':
    unittest.main()