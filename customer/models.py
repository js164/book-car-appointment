from django.db import models
from django.contrib import auth
from django.contrib.auth import get_user_model
from company.models import User as CompanyUser,Cars
from django.urls import reverse
from Cars import settings
from django.contrib.auth.mixins import (LoginRequiredMixin,PermissionRequiredMixin)
# Create your models here.

User=get_user_model()

class CustomerUser(auth.models.User,auth.models.PermissionsMixin):
    def __str__(self):
        return self.username

class BookAppointment(LoginRequiredMixin,models.Model):
    customer=models.ForeignKey(CustomerUser,on_delete=models.CASCADE,null=True)
    company=models.ForeignKey(CompanyUser,on_delete=models.CASCADE,null=True)
    carinstace=models.ForeignKey(Cars,on_delete=models.CASCADE,null=True)
    appointmnetcarname=models.CharField(max_length=30,default='Null',unique=False)
    date=models.DateTimeField()
    name=models.CharField(max_length=30)
    email=models.CharField(max_length=30)
    contact=models.BigIntegerField()

    class Meta:
        ordering=['date']
        permissions =[('view_appointments','Can View Appointments')]

    def get_absolute_url(self):
        slug=self.carinstace.slug
        return reverse('cardetailshow',kwargs={'slug':slug})
