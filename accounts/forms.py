from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UserRegistrationForm(UserCreationForm):
    username=forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={"class": "form-control"})),
    email=forms.EmailField(max_length=30, required=True, widget=forms.EmailInput(attrs={"class": "form-control"})),
    username=forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={"type": "password", "class": "form-control", "id": "password1"})),
    username=forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={"type": "password", "class": "form-control", "id": "password2"})),
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
    
    
class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"type": "password", "class": "form-control", "placeholder": "Password",}))
