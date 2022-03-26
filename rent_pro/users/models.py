from django.db import models
from django.contrib.auth.models import AbstractUser,User
from PIL import Image

# Create your models here.
class User(AbstractUser):
    USER_ROLE_CHOICES = (
        ("Admin","admin"),
        ("General","general"),
    )
    username = None
    # username = models.CharField(max_length=255,null=True,blank=True)
    user_role = models.CharField(max_length=120, choices=USER_ROLE_CHOICES, default="General")
    first_name = models.CharField(max_length=100, blank=False, null=True)
    last_name = models.CharField(max_length=100, blank=False, null=True)
    email = models.EmailField(max_length=255, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    profile_image = models.ImageField(upload_to="item_pics", default="default.jpg")
    
    def __str__(self):
        return self.user.email