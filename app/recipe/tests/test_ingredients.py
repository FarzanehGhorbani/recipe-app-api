from unicodedata import name
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENT_URLS = reverse("recipe:ingredient-list")


class PublicIngredientPublicTests(TestCase):
    """Test the Publicly availabe ingredients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint."""
        res = self.client.get(INGREDIENT_URLS)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED


class PrivateIngredientApiTests(TestCase):
    """Test the private ingredients API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("info@gmail.com", "testpass")
        self.client.force_authenticate(self.user)

    def test_retrieve_ingrediet_list(self):
        """Test retrieving a list of ingredients"""
        Ingredient.objects.create(user=self.user, name="Kale")
        Ingredient.objects.create(user=self.user, name="Salt")

        res = self.client.get(INGREDIENT_URLS)
        ingreidients = Ingredient.objects.all().order_by("-name")
        serializer = IngredientSerializer(ingreidients, many=True)
        assert res.status_code == status.HTTP_200_OK
        assert res.data == serializer.data

    def test_ingredient_limited_to_user(self):
        """Test that only ingredients for the authenticated user are returned"""
        user2 = get_user_model().objects.create_user("test@gmail.com", "testpass")
        Ingredient.objects.create(user=user2, name="Vinger")
        ingredient = Ingredient.objects.create(user=self.user, name="Tumeric")
        res = self.client.get(INGREDIENT_URLS)
        assert res.status_code == status.HTTP_200_OK
        assert len(res.data) == 1
        assert res.data[0]["name"] == ingredient.name
