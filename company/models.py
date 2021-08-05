from django.db import models
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.shortcuts import redirect
from django.utils.text import slugify
from django import template

register=template.Library()

class User(auth.models.User,auth.models.PermissionsMixin):
    myshowroom=models.CharField(max_length=20,default='')
    slug=models.SlugField(allow_unicode=True,unique=True,null=True)
    contact=models.BigIntegerField()
    address=models.TextField(blank=False,default='')

    def save(self,*args,**kwargs):
        self.slug=slugify(self.username)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.username

class Cars(models.Model):
    carname=models.CharField(max_length=30,primary_key = True)
    slug=models.SlugField(allow_unicode=True,unique=True,null=True)
    carprice=models.IntegerField()
    engine=models.IntegerField()
    compuser=models.CharField(max_length=20,default='')
    companyslug=models.SlugField(allow_unicode=True,unique=False,null=True)
    photo = models.ImageField(upload_to='cars/')
    created_at=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-created_at']

    def save(self,*args,**kwargs):
        self.slug=slugify(self.carname)
        self.companyslug=slugify(self.compuser)
        print(self.companyslug)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('company:cardetails',kwargs={'slug':self.slug})


fual_type = (
    ('Petrol','Petrol'),
    ('Diesel', 'Diesel'),
    ('Electric','Electric')
)
transmission_type=(
    ('Manual','Manual'),
    ('Automatic','Automatic')
)

class CarDetails(models.Model):
    car=models.OneToOneField(Cars,on_delete=models.CASCADE)
    detailcarname=models.CharField(max_length=30,default='Null')
    slug=models.SlugField(allow_unicode=True,unique=True,null=True)
    carprice=models.IntegerField()
    engine=models.IntegerField()
    compuser=models.CharField(max_length=20,default='')
    companyslug=models.SlugField(allow_unicode=True,unique=False,null=True)
    milege=models.FloatField()
    seating=models.IntegerField()
    fuel=models.CharField(max_length=8,choices=fual_type,default='Petrol')
    transmission=models.CharField(max_length=10,choices=transmission_type,default='Manual')
    airbags=models.IntegerField()
    photo1 = models.ImageField(upload_to='cars/',default='path/to/my/default/image.jpg')
    photo2 = models.ImageField(upload_to='cars/',default='path/to/my/default/image.jpg')
    photo3 = models.ImageField(upload_to='cars/',default='path/to/my/default/image.jpg')

    def save(self,*args,**kwargs):
        self.slug=slugify(self.detailcarname)
        self.companyslug=slugify(self.compuser)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('company:cardetailshow',kwargs={'slug':self.slug})

    def __str__(self):
        return self.car.carname
