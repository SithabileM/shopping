from django.db import models
from django.conf import settings
from django.contrib.auth.models import User,AbstractUser,Permission,Group
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime, timedelta
import random


#get current date
now=datetime.now()

#add a month to the current date
monthFromNow=now+timedelta(days=30)

# Create your models here.
#define a model to store the names of different clothing sections

class Sections(models.Model):
    name=models.CharField(unique=True,max_length=100)
    def __str__(self):
        return self.name
#define a model for the clothing items
class ClothingItem(models.Model):
    name=models.CharField(max_length=65)
    description=models.TextField(max_length=1000)
    shortDescription=models.CharField(default="No caption",max_length=30)
    rating=models.FloatField(null=True,blank=True,validators=[MinValueValidator(0.0),MaxValueValidator(5.0)])
    quantity=models.IntegerField(default=0)
    price=models.DecimalField(default=0,max_digits=10, decimal_places=2)
    shippingDate=models.DateField(default=monthFromNow)
    image=models.ImageField(upload_to='media/images/%y',default="OIP.jpg")
    clothingSections=models.ManyToManyField(Sections,max_length=100)
    
    
    def __str__(self):
        return self.shortDescription
    
#Define a model for the user-owned items

class UserOwnedItems(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    clothing_item=models.ForeignKey(ClothingItem,on_delete=models.CASCADE)
    amount_purchased=models.IntegerField(default=1)
    status=models.BooleanField(default=False)
    
#Add a one-to-one field to the User model
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    owned_items=models.ManyToManyField(ClothingItem,blank=True,related_name='owners',related_query_name='owner')
    cart_items=models.ManyToManyField(ClothingItem,blank=True)
    inventory=models.ManyToManyField(ClothingItem,blank=True,related_name="stock")
    bank_balance=models.FloatField(default=round(random.uniform(1.00,1000.00),2))
    
class CartItems(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    item=models.ForeignKey(ClothingItem,null=True,on_delete=models.SET_NULL)
    amount=models.IntegerField(default=1)
    
class Review(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    reviewItem=models.ForeignKey(ClothingItem,on_delete=models.CASCADE)
    review=models.CharField(max_length=250)
    created_at=models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering=['user','reviewItem','review','-created_at']