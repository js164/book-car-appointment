from django import template
from django.db.models.query import QuerySet
from django.views.generic import TemplateView,ListView,RedirectView,DetailView,View
from django.contrib.auth import get_user_model
from company import models
from django.shortcuts import render,redirect
from django.urls import reverse
import company
from customer.models import CustomerUser,BookAppointment
from company.models import User as CompanyUser
from django.http import HttpResponse
from django.utils.text import slugify
from company.models import Cars,CarDetails
from django.contrib import messages
from datetime import datetime

CurrentUser=get_user_model()


class findcar(ListView):
    model=Cars
    template_name="customer/cars_list.html"

    def get_queryset(self):
        queryset=super().get_queryset()
        slug=slugify(str(self.request.GET.get('search')))
        if queryset.filter(slug=slug).count() > 0:
            return queryset.filter(slug=slug)
        elif queryset.filter(companyslug=slug).count() > 0:
            return queryset.filter(companyslug=slug)
        else:
            return super().get_queryset()

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        queryset=super().get_queryset()
        slug=slugify(str(self.request.GET.get('search')))
        if queryset.filter(slug=slug).count() > 0:
            context['messages']="Search For: "+str(self.request.GET.get('search'))
            return context
        elif queryset.filter(companyslug=slug).count() > 0:
            context['messages']="Search For: "+str(self.request.GET.get('search'))
            return context
        else:
            context['messages']="Result Not Found for: "+str(self.request.GET.get('search'))+"\nHere is All Cars:"
            return context

class findcarbybrand(ListView):
    model=Cars
    template_name="customer/cars_list.html"

    def get_queryset(self):
        queryset=super().get_queryset()
        slug=slugify(str(self.kwargs.get('slug')))
        if queryset.filter(companyslug=slug).count() > 0:
            return queryset.filter(companyslug=slug)
        else:
            return super().get_queryset()

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        queryset=super().get_queryset()
        slug=self.kwargs.get('slug')
        context['messages']="Search For: "+self.kwargs.get("slug")
        return context

class HomePage(TemplateView):
    template_name='home.html'

class ThankYou(TemplateView):
    template_name='thankyou.html'

class Dashboard(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {'username': request.user.username }
        try:
            if CustomerUser.objects.get(username=request.user.username):
                # context = {'username': request.user.username, 'totalcars':Cars.objects.get(compuser=request.user.username).count() }
                return render(request, "home.html", context=context)
        except:
            try:
                today = datetime.today().strftime('%Y-%m-%d')
                context = {'username': request.user.username, 'totalcars':Cars.objects.filter(compuser=request.user.username).count(),
                'upcomingappointments':BookAppointment.objects.filter(company=CompanyUser.objects.get(username=request.user.username)).filter(date__gte=today).count(),
                'totalappointments': BookAppointment.objects.filter(company=CompanyUser.objects.get(username=request.user.username)).count()}
                return render(request, "company/dashboard.html", context=context)
            except:
                return render(request, "home.html", context=context)

class AllCarsList(RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        try:
            if CompanyUser.objects.get(username=self.request.user.username):
                return reverse('company:cars')
        except:
            return reverse('customer:cars')

class CarsDetail(RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        try:
            if CompanyUser.objects.get(username=self.request.user.username):
                return reverse('company:cardetailshow',kwargs={'slug':self.kwargs.get('slug')})
        except:
            return reverse('customer:cardetailshow',kwargs={'slug':self.kwargs.get('slug')})

class CompareSelect(View):
    template_name='compareselect.html'

    def get(self, request, *args, **kwargs):
        car_list=CarDetails.objects.all()
        print(car_list)
        return render(request, self.template_name,{'cars':car_list})



class CompareCar(TemplateView):

    def get(self,request):
        slug1= slugify(str(self.request.GET.get('car1dropdown')))
        slug2= slugify(str(self.request.GET.get('car2dropdown')))
        car1=CarDetails.objects.get(slug=slug1)
        car2=CarDetails.objects.get(slug=slug2)
        queryset={'car1':car1,'car2':car2}
        return render(request, "compare.html", context=queryset)

def carbybrandfilter(request):
    if request.method == 'POST':
        slug = request.POST['slug']
        cars=Cars.objects.filter(companyslug=slug)
        carname=[c.carname+" " for c in cars]
        return HttpResponse(carname)
    else:
        return HttpResponse('Error')