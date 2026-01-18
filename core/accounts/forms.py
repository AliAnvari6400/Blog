from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ["user", "first_name", "last_name", "image", "description"]
        widgets = {
            "user": forms.HiddenInput(),
        }
