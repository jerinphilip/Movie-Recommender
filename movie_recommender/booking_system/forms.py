from .models import UserProfile
from django.forms import ModelForm

class UserProfileCreationForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ["age", "gender", "phone", "genre_pref", "username", "password"]  

