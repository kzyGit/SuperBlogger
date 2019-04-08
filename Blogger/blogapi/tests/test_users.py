from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from ..models import User
import json


class BaseViewTest(APITestCase):
    client = APIClient()
    login_user = {
        "username": "Tim",
        "password": "Tim@gmail.com"
    }

    def login(self):
        response = self.client.post(
            reverse('login'), data=json.dumps(self.login_user), content_type="application/json")
        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        return self.token

    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="Tim",
            firstname="Tim",
            surname="Tim",
            email="Tim@gmail.com")

        self.new_user = {
            "username": "ann",
            "firstname": "ann",
            "surname": "ann",
            "email": "ann@gmail.com"
        }
        self.create_user = self.client.post(reverse('users'),
                                            data=json.dumps(self.new_user),
                                            content_type="application/json")


class UserTest(BaseViewTest):
    def test_user_signup(self):
        self.assertEqual(self.create_user.status_code, 201)

    def test_get_all_users(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(len(response.data), 2)

    def test_getting_single_user(self):
        response = self.client.get(
            reverse('user', kwargs={
                'pk': self.create_user.data['user_info']['id']}))

        self.assertEqual(response.status_code, 200)

    def test_gettting_non_existent_user(self):
        response = self.client.get(reverse('user', kwargs={'pk': 9}))
        self.assertEqual(response.status_code, 404)

    def test_unathorised_deleting_single_user(self):
        response = self.client.delete(
            reverse('user', kwargs={
                'pk': self.create_user.data['user_info']['id']}))
        self.assertEqual(response.status_code, 401)

    def test_deleting_single_user(self):
        self.login()
        response = self.client.delete(
            reverse('user', kwargs={
                'pk': self.create_user.data['user_info']['id']}))
        self.assertEqual(response.status_code, 204)