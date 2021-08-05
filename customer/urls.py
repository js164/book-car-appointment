from django.conf.urls import url
from . import views

app_name='customer'

urlpatterns=[
    url(r'signup/$',views.SignUp.as_view(),name='signup'),
    url(r'booktestdrive/(?P<slug>[-\w]+)/$',views.BookTestDrive.as_view(),name='booktestdrive'),
    url(r'allcars/',views.CarsList.as_view(),name='cars'),
    url(r'detailshow/(?P<slug>[-\w]+)/$',views.CarsDetail.as_view(),name='cardetailshow'),
    url(r'lowtohigh/',views.LowtoHigh.as_view(),name='lowtohigh'),
    url(r'hightolow/',views.HightoLow.as_view(),name='hightolow'),
]
