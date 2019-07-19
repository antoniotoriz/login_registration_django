from django.db import models
from django.db import IntegrityError
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
#DATABASE VALIDATIONS
class UserManager(models.Manager):
    #REGISTRATION VALIDATOR
    def basic_validator(self, postData):
        errors = {}
        result = User.objects.filter(email=postData['email'])
        if len(postData["first_name"]) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData["last_name"]) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if len(postData["email"]) < 5:
            errors["email"] = "Email should be at least 5 characters"
        if len(result) > 0:
            errors['emails'] = "Email already exists"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email_format"] = "Email should be in the name@mail.com format"
        if len(postData["password"]) < 6:
            errors["password"] = "Your password must be at least 6 characters long. Please try another."
        if postData['password'] != postData['confirm_password']:
            errors['password_match'] = "Password does not match with confirm password."
        return errors
    #LOGIN VALIDATOR
    def login_validator(self, postData):
        errors = {}
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Email must be in format "yourname@mail.com"'
        if not User.objects.filter(email=postData['email']):
            errors['emails'] = "Email address not recognized"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters long"
        return errors

#USER DATABASE
class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255, unique=True)
	password = models.CharField(max_length=255)
	birthday = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

