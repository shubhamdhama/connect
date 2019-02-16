from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=39, required=False,
                                 help_text="Optional. Enter First Name")
    last_name = forms.CharField(max_length=39, required=False,
                                help_text="Optional. Enter last Name")
    email = forms.CharField(max_length=254,
                            help_text="Required. Enter your email")

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email',
                  'password1', 'password2')
