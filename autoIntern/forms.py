from django.forms import ModelForm
from autoIntern.models import User
from django import forms


class UserForm(ModelForm):
    """Defines the user form in the registration page"""

    class Meta:
        model = User
        fields = {'email':'', 'password':'',
                  'firstName':'','lastName':'',
                   'displayName':'', 'title':'',
                    'group':''}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # elds = {'email':'', 'password':'', 'firstName':'', 'lastName':'', 'displayName':'', 'title':'', 'group':''}
        self.fields['email'].widget.attrs.update({'type':'email',
                                            'class' : 'form-control',
                                            'placeholder' : 'Enter Email'})
        self.fields['password'].widget.attrs.update({'type':'password',
                                                'class' : 'form-control',
                                                'placeholder' : 'Password'})
        self.fields['firstName'].widget.attrs.update({'type':'text',
                                                'class' : 'form-control',
                                                'placeholder' : 'First Name'})
        self.fields['lastName'].widget.attrs.update({'type': 'text',
                                               'class': 'form-control',
                                               'placeholder': 'Last Name'})
        self.fields['displayName'].widget.attrs.update({'type': 'text',
                                                  'class': 'form-control',
                                                  'placeholder': 'Display Name'})
        self.fields['title'].widget.attrs.update({'type': 'text',
                                            'class': 'form-control',
                                            'placeholder': 'Title'})
        self.fields['group'].widget.attrs.update({'type': 'text',
                                            'class': 'form-control',
                                            'placeholder': 'Group'})
