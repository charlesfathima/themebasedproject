from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from .models import CustomPreferences

class ExtendedUserCreationForm(UserCreationForm):
    username=forms.CharField(required=True,max_length=120)
    email=forms.EmailField(required=True)
    first_name=forms.CharField(max_length=120)
    last_name=forms.CharField(max_length=120)
    password1=forms.CharField(max_length=120)
    password2=forms.CharField(max_length=120)
    class Meta:
        model=User
        fields=('username','email','first_name','password1','password2')

    def save(self,commit=True):
        user=super().save(commit=False)
        user.username=self.cleaned_data['username']
        user.email=self.cleaned_data['email']
        user.first_name=self.cleaned_data['first_name']
        user.last_name=self.cleaned_data['last_name']
        user.password1=self.cleaned_data['password1']
        user.password2=self.cleaned_data['password2']
        if commit:
            user.save()

        return user


class CustomPreferencesForm(forms.ModelForm):
    
    preferences=forms.CharField(widget=forms.Textarea(attrs={'rows':2, 'cols': 20}),max_length=160)
    class Meta:
        model=CustomPreferences
        fields=('preferences',)

    """def save(self,commit=True):
        user=super().save(commit=False)
        user.preferences=self.cleaned_data['preferences']
        if commit:
            user.save()

        return user
    """