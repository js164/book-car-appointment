from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='company'

urlpatterns=[
    url(r'signup/$',views.SignUp.as_view(),name='signup'),
    url(r'successlogin/',views.SuccessLogin.as_view(),name='successlogin'),
    url(r'dashboard/',views.Dashboard.as_view(),name='dashboard'),
    url(r'addcar/',views.AddCar.as_view(),name='addcar'),
    url(r'cardetails/(?P<slug>[-\w]+)/$',views.AddCarDetails.as_view(),name='cardetails'),
    url(r'allcars/',views.CarsList.as_view(),name='cars'),
    url(r'detailshow/(?P<slug>[-\w]+)/$',views.CarsDetail.as_view(),name='cardetailshow'),
    url(r'appointments/',views.AppointmentList.as_view(),name='appointments'),
    url(r'deletecar/(?P<slug>[-\w]+)/$',views.Cardelete.as_view(),name='deletecar'),
    url(r'updatecar/(?P<slug>[-\w]+)/$',views.CarUpdate.as_view(),name='updatecar'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
