from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from customer.models import CustomerUser
from django import forms
from django.forms import ModelForm
from customer.models import BookAppointment
from bootstrap_datepicker_plus import DateTimePickerInput

class CustomerCreateForm(UserCreationForm):
    class Meta:
        fields=('username','email','password1','password2')
        model=CustomerUser

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label='Username'
        self.fields['email'].label='Email Address'

class DateInput(forms.DateInput):
    input_type = 'date'

class BookAppointmentForm(ModelForm):
    class Meta:
        model = BookAppointment
        fields = ('name','email','contact','date')
        widgets = {'date': DateInput(),}
