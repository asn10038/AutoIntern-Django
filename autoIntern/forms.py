from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms


class UserForm(ModelForm):
    """Defines the user form in the registration page"""

    class Meta:
        model = User
        fields = {'username': '', 'email': '',
                  'first_name': '', 'last_name': '',
                  'password': ''}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'type': 'text',
                                                     'class': 'form-control',
                                                     'placeholder': 'Enter Username'})
        self.fields['email'].widget.attrs.update({'type': 'email',
                                                  'class' : 'form-control',
                                                  'placeholder' : 'Enter Email'})
        self.fields['first_name'].widget.attrs.update({'type': 'text',
                                                       'class': 'form-control',
                                                       'placeholder' : 'First Name'})
        self.fields['last_name'].widget.attrs.update({'type': 'text',
                                                      'class': 'form-control',
                                                      'placeholder': 'Last Name'})
        self.fields['password'].widget.attrs.update({'type': 'password',
                                                      'class': 'form-control',
                                                      'placeholder': 'Password'})
    def validate_password(self):
        pass

    def save(self):
        user = User.objects.create_user(self.cleaned_data['username'],
                                        self.cleaned_data['email'],
                                        self.cleaned_data['password'])
        user.first_name = self.cleaned_data['first_name'].capitalize()
        user.last_name = self.cleaned_data['last_name'].capitalize()
        user.save()

        return user
