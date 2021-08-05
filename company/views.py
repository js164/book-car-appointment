from django.shortcuts import render
from django.views.generic import CreateView,ListView,DetailView,DeleteView,UpdateView
from . import forms
from django.contrib.auth import login, logout
from django.urls import reverse,reverse_lazy
from django.views.generic import TemplateView
from . import models
from company.models import Cars,CarDetails
from company.models import User as CompanyUser
from customer.models import CustomerUser,BookAppointment
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import (LoginRequiredMixin,PermissionRequiredMixin)
from datetime import datetime
from django.utils.text import slugify
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django import template
from django.contrib.auth.models import Group
# Create your views here.

User=get_user_model()
register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists() 

class SignUp(CreateView):
    form_class=forms.CompanyUserCreateForm
    success_url=reverse_lazy('login')
    template_name='company/signup.html'

    def form_valid(self, form):
        user = form.save()
        group=Group.objects.get(name='company')
        user.groups.add(group)
        returnVal = super(SignUp, self).form_valid(form)
        return returnVal  

class SuccessLogin(TemplateView):
    template_name='company/successlogin.html'

class Dashboard(LoginRequiredMixin,TemplateView):
    template_name='company/dashboard.html'

class AddCar(LoginRequiredMixin,CreateView):
    fields=('carname','carprice','engine','photo')
    model=Cars
    template_name='company/addcar.html'

    def form_valid(self,form):
        self.object=form.save(commit=False)
        self.object.compuser = str(self.request.user)
        self.object.save()
        return super().form_valid(form)

class AddCarDetails(LoginRequiredMixin,CreateView):
    fields=('milege','seating','fuel','transmission','airbags','photo1','photo2','photo3')
    model=CarDetails
    template_name='company/addcardetails.html'

    def form_valid(self,form):
        self.object=form.save(commit=False)
        carobj=Cars.objects.get(slug=self.kwargs['slug'])
        self.object.car = carobj
        self.object.detailcarname=str(carobj.carname)
        self.object.carprice=str(carobj.carprice)
        self.object.engine=str(carobj.engine)
        self.object.compuser=str(carobj.compuser)
        self.object.compuser=str(carobj.compuser)

        self.object.save()
        return super().form_valid(form)

class Cardelete(LoginRequiredMixin,DeleteView):
    model=Cars
    success_url=reverse_lazy('dashboard')

class CarUpdate(LoginRequiredMixin,UpdateView):
    redirect_field_name='company/cardetails_detail.html'
    template_name='company/addcardetails.html'
    # form_class=PostForm
    fields=('milege','seating','fuel','transmission','airbags','photo1','photo2','photo3')
    model=CarDetails


class CarsList(ListView):
    model=Cars

    def get_queryset(self):
        queryset=super().get_queryset()
        return queryset.filter(compuser=self.request.user.username)
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        queryset=super().get_queryset()
        slug=self.kwargs.get('slug')
        context['messages']="Your Company: "+self.request.user.username
        return context

class CarsDetail(DetailView):
    model=CarDetails


class AppointmentList(LoginRequiredMixin,ListView):
    model=BookAppointment
    template_name='company/bookappointment_list.html'

    def get_queryset(self):
        queryset=super().get_queryset()
        # today = datetime.today().strftime('%Y-%m-%d')
        # appointments=BookAppointment.objects.filter(date__gte=today)
        return queryset.filter(company=self.request.user.id)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.today().strftime('%Y-%m-%d')
        context['upcomingappointments']=BookAppointment.objects.filter(company=CompanyUser.objects.get(username=self.request.user.username)).filter(date__gte=today).count()
        context['pastappointments']= BookAppointment.objects.filter(company=CompanyUser.objects.get(username=self.request.user.username)).count()
        return context
