from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .models import CustomUser
from django.contrib.auth import get_user_model
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class UserLoginForm(forms.Form):
    username = forms.CharField(label ="")
    password = forms.CharField(label="",widget=forms.PasswordInput)



class UserSignUpForm(CustomUserCreationForm):
    full_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    phone = PhoneNumberField( label="phone" ,widget=PhoneNumberPrefixWidget(initial='+91'),
        required=False)


    class Meta:
        model = User
        fields = ('full_name',  'email','username', 'password1', 'password2','phone' )

    def save(self, commit=True):
        user = super(UserSignUpForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
