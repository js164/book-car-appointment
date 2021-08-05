from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from company.models import User

class CompanyUserCreateForm(UserCreationForm):

    class Meta:
        fields=('username','email','password1','password2','myshowroom','contact','address')
        model=User

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label='Car Company Name'
        self.fields['email'].label='Email Address'
        self.fields['myshowroom'].label='Show Room Name'
