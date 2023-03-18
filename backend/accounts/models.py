from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _




# Create your models here.

class CustomUserManager(BaseUserManager):
  def create_user(self, email, password=None, **extra_fields):
    if not email:
      raise ValueError("The Email field must be set")
    email = self.normalize_email(email)
    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save()
    return user
  
  def create_superuser(self, email, password=None, **extra_fields):
    extra_fields.setdefault("is_staff", True)
    extra_fields.setdefault("is_superuser", True)
    
    if extra_fields.get("is_staff") is not True:
      raise ValueError("Superuser must have is_staff=True.")
    if extra_fields.get("is_superuser") is not True:
      raise ValueError("Superuser must have is_superuser=True")
    
    return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField(_("email address"), unique=True)
  name = models.CharField(_("name"), null=True, blank=True,  max_length=100)
  did = models.CharField(max_length=255, unique=True, null=True, blank=True)
  is_active = models.BooleanField(_("active"), default=True)
  is_staff = models.BooleanField(_("staff"), default=False)
  
  objects = CustomUserManager()
  
  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = []
  
  def __str__(self):
    return self.email