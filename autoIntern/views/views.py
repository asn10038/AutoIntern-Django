# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from autoIntern.forms import UserForm
from autoIntern import models
from autoIntern.parse_identifiers import GetDocumentByHeader

def index(request):
    template = loader.get_template('autoIntern/homePage.html')
    userForm = UserForm()

    context = {'userForm' : userForm, 'user':None}
    return HttpResponse(template.render(context,request))

def register(request):
    """Register Users"""
    userForm = UserForm()
    if request.method == 'POST':
        userForm = UserForm(request.POST)
        if userForm.is_valid():
            user = models.User()
            user = models.User(**userForm.cleaned_data)
            user.save()
            request.session['userEmail'] = user.email
        return HttpResponse(loader.get_template('autoIntern/homePage.html').render({'userForm':userForm, 'user':user}, request))

    if request.method == 'GET':
        return HttpResponse(loader.get_template('autoIntern/homePage.html').render({'userForm': userForm, 'user':None}, request))

def login(request):
    """Defines the login behavior"""
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        template = loader.get_template('autoIntern/homePage.html')
        userForm = UserForm()
        user = None
        context = {'userForm': userForm, 'user': user}
        try:
            user = models.User.objects.get(email=email)
            if password == user.password:
                request.session['userEmail'] = user.email
                context = {'userForm': userForm, 'user': user}
                return HttpResponse(template.render(context,request))

        except:
            return HttpResponse(template.render(context,request))

def logout(request):
    """Defines the logout behavior"""
    if request.method == 'POST':
        template = loader.get_template('autoIntern/homePage.html')
        context = {'userForm': UserForm(), 'user': None}
        request.session['userEmail'] = None
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('/')

def upload(request):
    '''Handles Local file uploads'''
    if request.method == 'POST':
        userForm = UserForm()
        template = loader.get_template('autoIntern/homePage.html')

        # for line in request.FILES['uploadFile']:
        #     print(line)

        #####################################
        user = models.User.objects.get(email=request.session.get("userEmail"))
        context = {'userForm' : UserForm(), 'user' : user}

        new_document = GetDocumentByHeader(request.FILES['uploadFile'], user)
        new_document.save()

        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('/')


