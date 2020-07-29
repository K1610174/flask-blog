import unittest

from flask import url_for, request
from flask_testing import TestCase

from application import app, db, bcrypt
from application.models import Users, Posts
from wtforms.validators import ValidationError
from os import getenv

class TestBase(TestCase):

    def create_app(self):

        # pass in configurations for test database
        config_name = 'testing'
        app.config.update(SQLALCHEMY_DATABASE_URI=getenv('TEST_DB_URI'),
                SECRET_KEY=getenv('TEST_SECRET_KEY'),
                WTF_CSRF_ENABLED=False,
                DEBUG=True
                )
        return app

    def setUp(self):
        """
        Will be called before every test
        """
        # ensure there is no data in the test database when the test starts
        db.session.commit()
        db.drop_all()
        db.create_all()

        # create test admin user
        hashed_pw = bcrypt.generate_password_hash('admin2016')
        admin = Users(first_name="admin", last_name="admin", email="admin@admin.com", password=hashed_pw)

        # create test non-admin user
        hashed_pw_2 = bcrypt.generate_password_hash('test2016')
        employee = Users(first_name="test", last_name="user", email="test@user.com", password=hashed_pw_2)

        # save users to database
        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()

class TestViews(TestBase):

    def test_homepage_view(self):
        """
        Test that homepage is accessible without login
        """
        response = self.client.get(url_for('home'))
        self.assertEqual(response.status_code, 200)

    def test_aboutpage_view(self):
        """
        Test that aboutpage is accessible without login
        """
        response = self.client.get(url_for('about'))
        self.assertEqual(response.status_code, 200)

    def test_registerpage_view(self):
        """
        Test that registerpage is accessible without login
        """
        response = self.client.get(url_for('register'))
        self.assertEqual(response.status_code, 200)

    def test_loginpage_view(self):
        """
        Test that the login page is accessible
        """
        response = self.client.get(url_for('login'))
        self.assertEqual(response.status_code, 200)

class TestLogout(TestBase):

    def test_logout(self):
        """
        Test if user can logout
        """
        with self.client:
            self.client.post(
                    url_for('login'),
                    data=dict(
                        email='admin@admin.com',
                        password='admin2016'
                    ),
                    follow_redirects=True
            )
            response=self.client.get(
                    url_for('logout',follow_redirects=True)
                    )
            self.assertEqual(response.status_code, 302)


class TestRegister(TestBase):

    def test_register_new_user(self):
        """
        Test that a new user can register
        """
        with self.client:
            response = self.client.post(
                    url_for('register'),
                    data=dict(
                        first_name='Admin',
                        last_name='Admin',
                        email='admin@admin.com',
                        password='admin2016',
                        confirm_password='admin2016'
                        ),
                    follow_redirects=True
                    )
            self.assertEqual(response.status_code, 200)

    def test_validation_register_user(self):
        """

        """
        with self.client:
             response = self.client.post(
                    url_for('register'),
                    data=dict(
                        first_name='admin',
                        last_name='admin',
                        email='admin@admin.com',
                        password='admin2016',
                        confirm_password='admin2016'
                        ),
                    follow_redirects=True
                    )
             self.assertIn(b'Email already in use',response.data)



class TestPosts(TestBase):

    def test_add_new_post(self):
        """
        Test that when I add a new post, I am redirected to the homepage with the new post visible
        """
        with self.client:
            self.client.post(
                    url_for('login'), 
                    data=dict(
                        email='admin@admin.com',
                        password='admin2016'
                    ),
                    follow_redirects=True
            )
            response = self.client.post(
                url_for('post'),
                data=dict(
                    title="Test Title",
                    content="Test Content"
                ),
                follow_redirects=True
            )
            self.assertIn(b'Test Title', response.data)

    def test_redirect_postpage(self):
        """
        Test that when I try to access /post I am redirected to the correct page
        """
        with self.client:
            response=self.client.get('/post',follow_redirects=True)
            self.assertEqual(response.status_code, 200)

class TestUpdateAccount(TestBase):

    def test_update_account_page(self):
        """
        Test that the logged in user can update their account.
        """
        with self.client:
            self.client.post(
                    url_for('login'),
                    data=dict(
                        email='admin@admin.com',
                        password='admin2016'
                    ),
                    follow_redirects=True
            )
            response = self.client.post(
                url_for('account'),
                data=dict(
                    first_name="Admin",
                    last_name="One",
                    email="admin@admin.com"
                ),
                follow_redirects=True
            )
            self.assertIn(b'Admin', response.data)
            self.assertEqual(response.status_code, 200)

class TestAccountDelete(TestBase):

    def test_delete_account(self):
        """
        Test that the logged in user can delete their account.
        """
        with self.client:
            self.client.post(
                    url_for('login'),
                    data=dict(
                        email='admin@admin.com',
                        password='admin2016'
                    ),
                    follow_redirects=True
            )
            response = self.client.post(
                url_for('account_delete'),follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)


