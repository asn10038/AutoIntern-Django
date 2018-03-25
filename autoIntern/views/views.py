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
import json
import csv

def index(request):
    template = loader.get_template('autoIntern/homePage.html')
    userForm = UserForm()

    # Check if user is logged in
    if request.session.get("userEmail") == None:
        context = {'userForm' : UserForm(), 'user' : None}
        return HttpResponse(template.render(context, request))
    else:
        user = models.User.objects.get(email=request.session.get("userEmail"))
        doc_ids = get_doc_ids()
        context = {'userForm' : UserForm(), 'user' : user, 'doc_ids': doc_ids}
        return HttpResponse(template.render(context, request))

def get_doc_ids():
    documents = models.Document.objects.all()

    doc_ids = []

    for document in documents:
        doc_ids.append(document.doc_id)

    return doc_ids


def viewDocument(request):
    if request.method == 'GET':
        # If not logged in, redirect
        if request.session.get("userEmail") == None:
            return HttpResponseRedirect('/')

        try:
            userForm = UserForm()
            template = loader.get_template('autoIntern/viewDocument.html')
            user = models.User.objects.get(email=request.session.get("userEmail"))

            cur_doc_id = request.GET['id']
            document = models.Document.objects.get(doc_id=cur_doc_id)
            file = document.file.read().decode('utf-8')
            #"AMAZON_COM_INC.10-Q.20171027.txt")

            doc_ids = get_doc_ids()

            context = {'userForm': UserForm(), 'user' : user, "file" : file, 'doc_ids': doc_ids}
            return HttpResponse(template.render(context, request))

        except:
            userForm = UserForm()
            template = loader.get_template('autoIntern/homePage.html')
            user = models.User.objects.get(email=request.session.get("userEmail"))

            doc_ids = get_doc_ids()

            context = {'userForm': UserForm(), 'user' : user, 'doc_ids': doc_ids}
            return HttpResponse(template.render(context, request))


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
        # Get first 10 documents here and add to context
        context = {'userForm': userForm, 'user': user}
        try:
            user = models.User.objects.get(email=email)
            if password == user.password:
                request.session['userEmail'] = user.email

                doc_ids = get_doc_ids()

                context = {'userForm': userForm, 'user': user, 'doc_ids': doc_ids}
                return HttpResponse(template.render(context,request))

        except:
            return HttpResponse(template.render(context,request))

def logout(request):
    """Defines the logout behavior"""
    if request.method == 'POST':
        template = loader.get_template('autoIntern/homePage.html')
        context = {'userForm': UserForm(), 'user': None}
        request.session['userEmail'] = None
        return HttpResponseRedirect('/')
        #return HttpResponse(template.render(context, request))
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
        doc_ids = get_doc_ids()
        context = {'userForm' : UserForm(), 'user' : user, 'doc_ids': doc_ids}

        new_document = GetDocumentByHeader(request.FILES['uploadFile'], user)
        new_document.save()

        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('/')

def exportTags(request):
    ''' Exports tags associated with document'''
    # Tags to be exported:
    TAGS = ['company', 'doc_type', 'doc_date']

    if request.method == 'POST':
        try:
            path = request.POST['path']
            doc_id = path.split("=", maxsplit=1)[1]
            doc = models.Document.objects.get(doc_id=doc_id)
            vals = doc.__dict__

            #dict_tags => contains tags and corresponding values
            dict_tags = {tag : vals[tag] for tag in TAGS}

            #Create json
            js = json.dumps(dict_tags)
            conv = json.loads(js)

            if 'csv' in request.POST:
                # Create the HttpResponse object with the appropriate CSV header.
                response = HttpResponse(content_type='text/csv; charset=utf8')
                response['Content-Disposition'] = 'attachment; filename="%s_%s_%s_tags.csv"' % (vals[TAGS[0]], vals[TAGS[1]], vals[TAGS[2]])

                writer = csv.writer(response)
                for tag in TAGS:
                    writer.writerow([tag, conv[tag]])

            elif 'txt' in request.POST:
                out = ''
                for k, v in conv.items():
                    out += k
                    out += ': '
                    out += v
                    out += '\r\n'

                # Remove the last, unnecessary newline
                out = out[:-2]

                # Create the HttpResponse object with the appropriate TXT header.
                response = HttpResponse(out, content_type='text/plain; charset=utf8')
                response['Content-Disposition'] = 'attachment; filename="%s_%s_%s_tags.txt"' % (vals[TAGS[0]], vals[TAGS[1]], vals[TAGS[2]])

            elif 'json' in request.POST:
                print ("json")
                response = HttpResponse(js, content_type='application/javascript; charset=utf8')
                response['Content-Disposition'] = 'attachment; filename="%s_%s_%s_tags.json"' % (vals[TAGS[0]], vals[TAGS[1]], vals[TAGS[2]])

            else:
                print('else')
                return HttpResponseRedirect('/')

            return response

        except:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')