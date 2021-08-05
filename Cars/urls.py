"""Cars URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static,serve
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.HomePage.as_view(),name='HomePage'),
    path('company/',include(('company.urls','company'),namespace='company')),
    path('company/',include('django.contrib.auth.urls')),
    path('thankyou/',views.ThankYou.as_view(),name='thankyou'),
    path('customer/',include(('customer.urls','customer'),namespace='customer')),
    path(r'accounts/login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path(r'accounts/logout/',auth_views.LogoutView.as_view(),name='logout'),
    path(r'dashboard/',views.Dashboard.as_view(),name='dashboard'),
    path('findcar/',views.findcar.as_view(),name='findcar'),
    path('allcars/',views.AllCarsList.as_view(),name='cars'),
    path('compare/',views.CompareCar.as_view(),name='compare'),
    path('detailshow/(?P<slug>[-\w]+)/$',views.CarsDetail.as_view(),name='cardetailshow'),
    path('carbybrand/(?P<slug>[-\w]+)/$',views.findcarbybrand.as_view(),name='carbybrand'),
    path('compareselect/',views.CompareSelect.as_view(),name='compareselect'),
    path(r'^brandfilter$',views.carbybrandfilter,name='carbybrandfilter'),
    re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
