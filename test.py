from unittest import TestCase

from app import app
from models import db, Pet

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adoption_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class AdoptionTests(TestCase):
    def setUp(self):
        """Add sample user."""
        Pet.query.delete()
        pet = Pet(name='Rex',species="dog",photo_url="https://montco.today/wp-content/uploads/sites/2/2019/01/generic-dog-photo.jpg",age=2,notes='good boy')

        db.session.add(pet)
        db.session.commit()
        
        self.pet_id = pet.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()


    def test_home(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('adopted animals', html)

    def test_search(self):
        with app.test_client() as client:
            resp = client.get("/pets")
            self.assertEqual(resp.status_code, 302)
    
    def test_pet_details(self):
        with app.test_client() as client:
            resp = client.get(f"/pets/{self.pet_id}")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Rex', html)
    
    def test_add_pet(self):
        with app.test_client() as client:
            resp = client.get("/add_pet")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Pet Name', html)

    def test_delete(self):
        with app.test_client() as client:
            resp = client.get(f"/delete/{self.pet_id}")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 302)
            self.assertNotIn('Rex', html)

