"""Declare models for YOUR_APP app."""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import FileExtensionValidator
from django.forms import ModelForm
import datetime  

class UserManager(BaseUserManager):
    

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    school_name = models.CharField(max_length = 150, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

class TestModel(models.Model):
    class_name = models.CharField(max_length=2)
    subject =  models.CharField(max_length=25)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    question_paper = models.FileField(upload_to='questionPaper/',null=False,validators=[FileExtensionValidator(allowed_extensions=['pdf','doc'])])
    test_id = models.CharField(max_length=50,primary_key=True)
    email = models.CharField(max_length=50)
    grading_id = models.CharField(max_length=50)

class StudentModel(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    
class StudentCheck(models.Model):
    email = models.CharField(max_length=50)
    test_id = models.CharField(max_length=50)

class AnswerModel(models.Model):
    test_id = models.CharField(max_length=50)
    answer_paper = models.FileField(upload_to='answerPaper/',null=False,validators=[FileExtensionValidator(allowed_extensions=['pdf','doc'])])
    marks = models.IntegerField(null=True,default=-1)
    name = models.CharField(max_length=50)

















