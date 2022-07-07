from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms

class UserForm(ModelForm):
    email = forms.EmailField(label="Email")
    is_staff = forms.BooleanField(label="Статус")

    class Meta:
        model=User
        fields =['username',
                 'email',
                 "is_staff"

        ]