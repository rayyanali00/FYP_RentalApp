from django.db import models
from users.models import User

# Create your models here.

class Category(models.Model):
    CATEGORY = (
        ("Furniture","Furniture"),
        ("ElectricAppliances","ElectricAppliances"),
        ("FitnessEquipment","FitnessEquipment"),
        ("Crockery","Crockery")        
    )
    cat_name = models.CharField(max_length=255,null=True,blank=True,choices=CATEGORY)
    
    def __str__(self):
        return self.cat_name

class Sub_Category(models.Model):
    # SUB_CATEGORY = (
    #     ("bed","sofas","diningtable","table","chairs","dressingtable")
    #     ("Air conditioner","Fans","LED","TV","Room lights","Microwave","Electric Kettle","Water dispense")
    #     ("bed","sofas","diningtable","table","chairs","dressingtable")
    #     ("bed","sofas","diningtable","table","chairs","dressingtable")
    # ) 
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, related_name="categories")
    sub_category = models.CharField(max_length=255,null=True, blank=True)

    def __str__(self):
        return self.sub_category
    
class Product(models.Model):
    # CATEGORY = (
    #     ("Furniture","Furniture",("bed","sofas","diningtable","table","chairs","dressingtable")),
    #     ("ElectricAppliances","ElectricAppliances",("Air conditioner","Fans","LED","TV","Room lights","Microwave","Electric Kettle","Water dispense")),
    #     ("FitnessEquipment","FitnessEquipment",("bed","sofas","diningtable","table","chairs","dressingtable")),
    #     ("Crockery","Crockery",("bed","sofas","diningtable","table","chairs","dressingtable"))
    # ) 
    # product_name = models.CharField(max_length=255, null=False, blank=False)
    prod_cat = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    prod_sub = models.ForeignKey(Sub_Category, null=True, blank=True, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255, null=True, blank=True)
    product_desc = models.CharField(max_length=255, null=False, blank=False)
    prod_img = models.ImageField(upload_to="item_pics", default="nothing.jpg")
    product_price = models.FloatField(max_length=255, null=False, blank=False)
    product_quantity = models.IntegerField(null=False)
    timePeriod = models.IntegerField(null=False)

    def __str__(self):
        return self.product_name
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    product_name = models.CharField(max_length=255,null=False, blank=False)
    product_category = models.CharField(max_length=255,null=False, blank=False)
    product_subcategory = models.CharField(max_length=255,null=False, blank=False)
    total_price = models.IntegerField(null=True, blank=True)
    