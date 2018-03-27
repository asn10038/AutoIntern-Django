from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from autoIntern.forms import UserForm
from autoIntern import models
from autoIntern.parse_identifiers import GetDocumentByHeader


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

        # User successfully authenticated
        if user is not None:
            login(request, user)
        return HttpResponseRedirect('/')


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
