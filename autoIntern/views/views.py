from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from autoIntern.forms import UserForm
from autoIntern import models
from autoIntern.parse_identifiers import GetDocumentByHeader
import json
import csv


def index(request):
    # Check if user is logged in
    if request.user.is_authenticated:
        context = {'doc_ids': get_doc_ids()}
    else:
        context = {'userForm': UserForm()}

    return render(request, 'autoIntern/homePage.html', context)


def userLogin(request):
    """Login Users"""
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        context = {'userForm': UserForm()}

        # User successfully authenticated
        if user is not None:
            login(request, user)
            context = {'doc_ids': get_doc_ids()}
        return render(request, 'autoIntern/homePage.html', context)


def userLogout(request):
    """Defines the logout behavior"""
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect('/')


def register(request):
    """Register Users"""
    userForm = UserForm()
    if request.method == 'POST':
        userForm = UserForm(request.POST)
        if userForm.is_valid():
            user = userForm.save()
        return HttpResponseRedirect('/')
    if request.method == 'GET':
        return HttpResponseRedirect('/')


# TODO: Move
def get_doc_ids():
    documents = models.Document.objects.all()

    doc_ids = []

    for document in documents:
        doc_ids.append(document.doc_id)

    return doc_ids


@login_required(redirect_field_name='', login_url='/')
def viewDocument(request):
    if request.method == 'GET':
        try:
            cur_doc_id = request.GET['id']
            document = models.Document.objects.get(doc_id=cur_doc_id)
            file = document.file.read().decode('utf-8')
            context = {"file": file}
            return render(request, 'autoIntern/viewDocument.html', context)
        except:
            context = {'doc_ids': get_doc_ids()}
            return render(request, 'autoIntern/viewDocument.html', context)


@login_required(redirect_field_name='', login_url='/')
def upload(request):
    '''Handles Local file uploads'''
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')

        user = User.objects.get(username=request.user)

        new_document = GetDocumentByHeader(request.FILES['uploadFile'], user)
        new_document.save()

        context = {'doc_ids': get_doc_ids()}

        return render(request, 'autoIntern/homePage.html', context)
    else:
        return HttpResponseRedirect('/')


# TODO: This should be simplified
@login_required(redirect_field_name='', login_url='/')
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
                response = HttpResponse(js, content_type='application/javascript; charset=utf8')
                response['Content-Disposition'] = 'attachment; filename="%s_%s_%s_tags.json"' % (vals[TAGS[0]], vals[TAGS[1]], vals[TAGS[2]])

            else:
                return HttpResponseRedirect('/')

            return response
        except:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')
