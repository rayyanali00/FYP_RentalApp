from django.db import models
from users.models import User

# Create your models here.
class Product(models.Model):
    CATEGORY = (
        ("Furniture","Furniture",("bed","sofas","diningtable","table","chairs","dressingtable")),
        ("ElectricAppliances","ElectricAppliances",("Air conditioner","Fans","LED","TV","Room lights","Microwave","Electric Kettle","Water dispense")),
        ("FitnessEquipment","FitnessEquipment",("bed","sofas","diningtable","table","chairs","dressingtable")),
        ("Crockery","Crockery",("bed","sofas","diningtable","table","chairs","dressingtable"))
    ) 
    product_name = models.CharField(max_length=255, null=False, blank=False)
    product_desc = models.CharField(max_length=255, null=False, blank=False)
    product_price = models.CharField(max_length=255, null=False, blank=False)
    product_quantity = models.IntegerField(null=False)
    prod_category = models.CharField(max_length=255, null=False, blank=False, choices=CATEGORY[0])
    prod_sub_category = models.CharField(max_length=255, null=False, blank=False, choices=CATEGORY[2])
