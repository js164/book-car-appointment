from django.shortcuts import render
from django.views.generic import CreateView,ListView,DetailView
from customer import forms
from django.urls import reverse_lazy
from customer.models import BookAppointment,CustomerUser
from company.models import CarDetails,Cars
from company.models import User as CompanyUser
from django.shortcuts import get_object_or_404
from customer.forms import BookAppointmentForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import (LoginRequiredMixin,PermissionRequiredMixin)
from django.contrib.auth.models import Group

# Create your views here.
class SignUp(CreateView):
    form_class=forms.CustomerCreateForm
    success_url=reverse_lazy('login')
    template_name='customer/signup.html'

    def form_valid(self, form):
        user = form.save()
        group=Group.objects.get(name='company')
        user.groups.add(group)
        returnVal = super(SignUp, self).form_valid(form)
        return returnVal  

cardetailsobj=None

class BookTestDrive(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    form_class=forms.BookAppointmentForm
    template_name='customer/bookappointment_form.html'

    def form_valid(self,form,*args,**kwargs):
        self.object=form.save(commit=False)
        self.object.appointmnetcarname = str(self.kwargs['slug'])
        carobj=Cars.objects.get(slug=self.kwargs['slug'])
        self.object.company=CompanyUser.objects.get(username=carobj.compuser)
        self.object.customer=CustomerUser.objects.get(username=self.request.user.username)
        self.object.carinstace=carobj
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['showroomname']=str(CompanyUser.objects.get(username=Cars.objects.get(slug=self.kwargs['slug']).compuser).myshowroom)
        context['contact']=(CompanyUser.objects.get(username=Cars.objects.get(slug=self.kwargs['slug']).compuser).contact)
        context['address']=str(CompanyUser.objects.get(username=Cars.objects.get(slug=self.kwargs['slug']).compuser).address)
        return context

    # def get_success_url(self):
        # messages.success(self.request, 'Yours Test Drive Appointment Sucessfully Booked...')
    success_message = 'Yours Test Drive Appointment Sucessfully Booked...'


class CarsList(ListView):
    model=Cars
    template_name='customer/cars_list.html'

class LowtoHigh(ListView):
    model=Cars
    template_name='customer/cars_list.html'
    # ordering = ['-carprice']
    def get_ordering(self):
        ordering = self.request.GET.get('ordering', 'carprice')
        return ordering

class HightoLow(ListView):
    model=Cars
    template_name='customer/cars_list.html'
    # ordering = ['carprice']
    def get_ordering(self):
        ordering = self.request.GET.get('ordering', '-carprice')
        return ordering


class CarsDetail(DetailView):
    model=CarDetails
    template_name='customer/cardetails_detail.html'
