from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from  rest_framework.test import APITestCase
from rest_framework import status
import pytest
import json


from .models import CustomUsers
from .serializer import UsersRegisterSerializer



class UserRegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {"email":"Test@gmail.com", "username": "TestCase", "password": "Test2024", "password2": "Test2024"}
        response = self.client.post("/api/userregister/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UserLoginTestCase(APITestCase):

    def test_login(self):
        self.user = CustomUsers.objects.create_user(email = "Test@gmail.com", password ="Test2024")
        self.token = RefreshToken.objects.create(user = self.user)


