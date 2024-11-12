from unittest import TestCase
from app import app
from models import db, Cupcake

CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 5,
    "image": "http://test.com/cupcake2.jpg"
}

class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5433/cupcakes_test'
        app.config['SQLALCHEMY_ECHO'] = False
        app.config['TESTING'] = True
        self.client = app.test_client()

        with app.app_context():
            db.drop_all()
            db.create_all()

            self.cupcake = Cupcake(**CUPCAKE_DATA)
            db.session.add(self.cupcake)
            db.session.commit()

            self.cupcake_id = self.cupcake.id

    def tearDown(self):
        """Clean up fouled transactions."""
        with app.app_context():
            db.session.rollback()
            db.drop_all()

    def test_list_cupcakes(self):
        """Test getting list of cupcakes."""
        with app.app_context():
            resp = self.client.get("/api/cupcakes")
            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcakes": [{
                    "id": self.cupcake_id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg"
                }]
            })

    def test_get_cupcake(self):
        """Test getting a single cupcake."""
        with app.app_context():
            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake_id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg"
                }
            })

    def test_create_cupcake(self):
        """Test creating a cupcake."""
        with app.app_context():
            url = "/api/cupcakes"
            resp = self.client.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            data = resp.json
            # don't know what ID we'll get, make sure it's an int
            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']

            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 5,
                    "image": "http://test.com/cupcake2.jpg"
                }
            })

    def test_update_cupcake(self):
        """Test updating a cupcake."""
        with app.app_context():
            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = self.client.patch(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake_id,
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 5,
                    "image": "http://test.com/cupcake2.jpg"
                }
            })

    def test_delete_cupcake(self):
        """Test deleting a cupcake."""
        with app.app_context():
            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = self.client.delete(url)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json, {"message": "Deleted"})