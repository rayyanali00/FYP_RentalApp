from django.db import models
from django.contrib.auth.models import AbstractUser,User
from PIL import Image

# Create your models here.
class User(AbstractUser):
    USER_ROLE_CHOICES = (
        ("Admin","admin"),
        ("General","general"),
    )
    user_role = models.CharField(max_length=120, choices=USER_ROLE_CHOICES, default="General")

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="item_pics", default="default.jpg")
    
    def __str__(self):
        return self.user.username