import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email="info@gmail.com", password="testpass"):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class TestModels(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = "info@gmail.com"
        password = "Testpass123"
        user = get_user_model().objects.create_user(email=email, password=password)
        assert user.email == email
        assert user.check_password(password) == True

    def test_email_user_normlized(self):
        """Test the email for a new user is normalized"""
        email = "test@GMAIL.COM"
        user = get_user_model().objects.create_user(email, "test123")
        assert user.email.islower() == True

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with pytest.raises(ValueError) as error:
            get_user_model().objects.create_user(None, "test123")

        assert error.value.args[0] == "Users must have an email address"

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            email="info@gmail.com", password="test123"
        )

        assert user.is_superuser == True
        assert user.is_staff == True

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(user=sample_user(), name="Vegan")
        assert str(tag) == tag.name
    
    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient=models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucomber'
        )
        assert str(ingredient)==ingredient.name
