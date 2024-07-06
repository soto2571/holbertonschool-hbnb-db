import unittest
from flask import Flask
from flask_jwt_extended import create_access_token
from src import db, create_app
from src.models.user import User


class UserRoutesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            # Create a test user
            self.user = User(
                email='testuser@example.com',
                first_name='Test',
                last_name='User',
                password='password123',
                is_admin=True
            )
            db.session.add(self.user)
            db.session.commit()
            self.access_token = create_access_token(
                identity=self.user.id, additional_claims={
                    "is_admin": self.user.is_admin})

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_users(self):
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        response = self.client.get('/api/users', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_non_admin_access(self):
        non_admin_user = User(
            email='nonadmin@example.com',
            first_name='Non',
            last_name='Admin',
            password='password123',
            is_admin=False
        )
        with self.app.app_context():
            db.session.add(non_admin_user)
            db.session.commit()
        non_admin_token = create_access_token(
            identity=non_admin_user.id, additional_claims={
                "is_admin": non_admin_user.is_admin})
        headers = {
            'Authorization': f'Bearer {non_admin_token}'
        }
        response = self.client.get('/api/users', headers=headers)
        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
