from .models import UserProfile
from django import forms

class UserProfileCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = UserProfile
        fields = ["age", "gender", "phone", "genre_pref", "username", "password", "first_name", "last_name"]  

