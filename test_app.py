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
        self.database_name = "castingagency_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)

       
        setup_db(self.app, self.database_path)

        self.ASSISTANT_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxfLXJvdGtFNktRS3Jla3NVaVllMyJ9.eyJpc3MiOiJodHRwczovL2Rldi0yYW84cTVuby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjI1NWQ4Zjg5MDQ4ODYwMDY5MDBlYzdlIiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTY0OTc5MzU3OSwiZXhwIjoxNjQ5ODAwNzc5LCJhenAiOiJDZVNrSnJWMm42OG9lSEs0ZzE1MkNMQkliTFd4TWRvZyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.DMugGqVhmov64JCemsHcagnBcI7hkeo3ZMa_fvJsnoxOd6ciLUV7FH8Rx74BwQ4W8c_AGdWzFosJUiw7mQWFXzuWq_GYxxV-zw4hMCdt45vivylfI2l98CiM4GF2AplNoGz1x7z-uAm3tsMp6VtiMHuhTUQ9tgAmKaEN3ixzUgBysulNfZ_4xFzTgexlTnDLPcn_wJ0XMkGUIJ1ttzrC7zRI_quvr_p7FnAbekwmSfjXlPy6fKovxD7oEgg2nDi4bjEfYu0pq7NuMXDfD6A20CuzEj1MQ081bc5AMrSj_JmTvACexoTbBdo6OC275rdD9PNFVYm3WFqvluPyZJXjKQ"
        self.DIRECTOR_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxfLXJvdGtFNktRS3Jla3NVaVllMyJ9.eyJpc3MiOiJodHRwczovL2Rldi0yYW84cTVuby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjI1NWQ4YmFkNzc4MmIwMDZmMzEwMjY5IiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTY0OTc5MzQzNywiZXhwIjoxNjQ5ODAwNjM3LCJhenAiOiJDZVNrSnJWMm42OG9lSEs0ZzE1MkNMQkliTFd4TWRvZyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.E1_V8C_sGJTBE7MZa0tAgRSUndK0u4uUoJ_VRtDa89kGP5k5XtyQ7SlMiYAXvBpKuRj2gX5jHycJEXreTE1J5fPu-bEb1aSMVj97zFY8uv-sfAPhsdRn8dJkaA39AvSKfOQ0jtiWBpznfHrBYy602f1hzSvNOtyFuLwALuWZq-mm0fgnkJx0VGjq0hvyrjcNSP6wjPRfepKqIUCYcLf33WbljtAbeGXImlP7FVwzMj-RByUsKEDwwP-0yFFzGxUbB4ZcplmEl1GeAbc-2i86xFpkNim4VDh7V-TfWMXDr0lR19uI_SWHxSNV6CC0Ejj6o40YkEvmnR4yalYD3ilh7g"
        self.PRODDUCER_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxfLXJvdGtFNktRS3Jla3NVaVllMyJ9.eyJpc3MiOiJodHRwczovL2Rldi0yYW84cTVuby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE1Nzc4MjdjYWMzN2YwMDY4NDQzY2Q1IiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTY0OTc5MjkyMCwiZXhwIjoxNjQ5ODAwMTIwLCJhenAiOiJDZVNrSnJWMm42OG9lSEs0ZzE1MkNMQkliTFd4TWRvZyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.TrCwPSInSa9baFnxiv21HVeQ95xZ-qNJCX0Ypovp-oble-upqpuPyVVoGh4tbHMAtVNSWOo3TdR72kexu4rTygC8fFTnRL4pj7_qv2l2R8plQqJZXCFk02CMKWCE-KflSYxaHMIHlvQGDvDVUDTeVMnVXq66F_Kw-fCOoiW1a1ggO9Lf8p4T6qy_o4MdFlJ4fDQz-rZqk4WEtOleyXV_IB76393rOxhmEdQNQ2d4cT67fk5TeLMZBELhrV4MduO0MNizRjYhVjU3drAvOFYx6YeNoZn-5jHUn98T4ZCm_yMDCeDCF-9L7qvEjDrv_n93-KRMuHMdUmZaiKMhkANW6g"


    
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

# # GET Endpoints: 

    #GET Actors
    def test_get_actors(self):
        res = self.client().get('/actors', headers={"Authorization": "Bearer {}".format(self.ASSISTANT_TOKEN)})
                             
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        #self.assertTrue(data['actors'])
        self.assertTrue(len(data['actors']))
        self.assertTrue(data['total_actors'])

#     #GET Actors Fail
#     def test_401_get_actors(self):
#         res = self.client().get('/actors')
#         data = json.loads(res.data)

#         self.assertEqual(res.status_code, 401)
#         self.assertEqual(data['success'], False)

#     #GET Movies
#     def test_get_movies(self):
#         res = self.client().get('movies',
#                                 headers={'Authorization': 'Bearer '
#                                          + str(self.casting_assistant)})
#         data = json.loads(res.data)

#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(data['success'], True)
#         self.assertTrue(data['movies'])

#     #GET Movies Fail
#     def test_401_get_movies(self):
#         res = self.client().get('/movies',
#                                 headers={})
#         data = json.loads(res.data)

#         self.assertEqual(res.status_code, 401)
#         self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == '__main__':
    unittest.main()