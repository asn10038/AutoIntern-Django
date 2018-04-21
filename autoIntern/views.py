from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from autoIntern.forms import UserForm
from autoIntern import models
from autoIntern.helpers import get_document_by_header, get_documents, \
    get_cases, get_docs_in_case, valid_file_type
import json
import csv
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.template import Library


def index(request):
    """ Handles requests for index"""

    # Check if user is logged in
    if request.user.is_authenticated:
        context = {'documents': get_documents(), 'cases' : get_cases(request)}
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
    if request.method == 'GET':
        return HttpResponseRedirect('/')


def userLogout(request):
    """Defines the logout behavior"""
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect('/')
    if request.method == 'GET':
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


@login_required(redirect_field_name='', login_url='/')
def viewDocument(request):
    if request.method == 'GET':
        try:
            cur_doc_id = request.GET['id']
            document = models.Document.objects.get(doc_id=cur_doc_id)

            raw = document.file.read().decode('utf-8')
            if document.doc_type != 'note':
                raw = raw.split('\n')[50:] # remove top level of junk
            file = ''
            tags = []
            for line in raw:
                # Can we remove the new body css this way too?
                if "<body" in line and "style=" in line:
                    file += '<body>'
                elif ".js" not in line and ".css" not in line:
                    file += line
            try:
                tags = models.Data.objects.filter(document__doc_id=cur_doc_id)
            except Exception as e:
                print(e)
            try:
                jsonTags = serialize('json', tags)
                context = {'file': file, 'tags': jsonTags}
            except Exception as e:
                print(e)
                context = {'file': file}
            return render(request, 'autoIntern/viewDocument.html', context)
        except:
            return HttpResponseRedirect('/error/')


@login_required(redirect_field_name='', login_url='/')
def viewCase(request):
    try:
        if request.method == 'GET':
            cur_case_id = request.GET['id']
        if request.method == 'POST':
            cur_case_id = request.POST['case_id']

        case = models.Case.objects.get(case_id=cur_case_id)
        user = User.objects.get(username=request.user)

        user_perms = models.Permissions.objects.all().filter(case=case, user=user)

        #If user types in case ID, redirect
        if user_perms.count() == 0:
            return HttpResponseRedirect('/')

        context = {'documents': get_docs_in_case(cur_case_id),
                   'case_name': case.case_name, 'case_id': cur_case_id}

        # If manager, add to context
        if user_perms.filter(user_type=models.Permissions.MANAGER_USER).count() > 0:
            context['is_manager'] = True
            users = User.objects.all()
            case_users_perms = models.Permissions.objects.filter(case=case)
            case_usernames = []
            case_users = []       # List of users that can be removed

            for u in case_users_perms:
                if u.user_type != models.Permissions.MANAGER_USER:
                    case_users.append(u.user)
                case_usernames.append(u.user.username)

            users_not_in_case = [user for user in users if user.username not in case_usernames
                                 and user.username != 'admin']
            context['users'] = users_not_in_case
            context['case_users'] = case_users

        else:
            context['is_manager'] = False

        return render(request, 'autoIntern/viewCase.html', context)

    except:
        return HttpResponseRedirect('/error')


@login_required(redirect_field_name='', login_url='/')
def createTag(request):
    if request.method == 'POST':
        try:
            cur_doc_id = request.POST['currentDocumentId']

            currentUser = request.user
            newTagLabel = request.POST['newTagLabel']
            newTagValue = request.POST['newTagContent']
            newTagIndex = newTagLineNum = 420 # Not needed
            rangySelection = request.POST['serializedRangySelection']

            document = models.Document.objects.get(doc_id=cur_doc_id)

            newTag = models.Data(creator_id=currentUser,
                                 value=newTagValue,
                                 label=newTagLabel,
                                 line=newTagLineNum,
                                 index=newTagIndex,
                                 document_id=cur_doc_id,
                                 rangySelection=rangySelection)
            newTag.save()

            return HttpResponseRedirect('/viewDocument?id='+cur_doc_id)

        except:
            return HttpResponseRedirect('/error')


@login_required(redirect_field_name='', login_url='/')
def upload(request):
    """Handles Local file uploads"""
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        new_document = None
        filename = str(request.FILES['uploadFile'])

        if not valid_file_type(filename):
            context = {'documents': get_documents(), 'cases': get_cases(request), 'non_text': True}
            return render(request, 'autoIntern/homepage.html', context)

        try:
            if 'public' in request.POST:
                if 'document_name' in request.POST:
                    new_document = get_document_by_header(request.FILES['uploadFile'], user, False,
                                                          request.POST['document_name'])
                else:
                    new_document = get_document_by_header(request.FILES['uploadFile'], user, False)

            else:
                new_document = get_document_by_header(request.FILES['uploadFile'], user)
        except:
            return HttpResponseRedirect('/error')

        case = None
        cur_case_id = None
        user_perms = None
        if 'case_id' in request.POST:
            case = models.Case.objects.get(case_id=request.POST['case_id'])
            cur_case_id = case.case_id
            user_perms = models.Permissions.objects.all().filter(case=cur_case_id, user=user)

        # new_document[0] is True/False on if the doc exists already
        if new_document[0] == False and 'case_id' in request.POST:
            case_name = case.case_name
            existing_doc = models.Document.objects.get(doc_id=new_document[1])
            case.documents.add(existing_doc)
            context = {'documents': get_docs_in_case(cur_case_id),
                       'case_name': case_name, 'case_id': cur_case_id,
                       'upload_fail': True}
            if user_perms.filter(user_type=models.Permissions.MANAGER_USER).count() > 0:
                context['is_manager'] = True
            else:
                context['is_manager'] = False
            return render(request, 'autoIntern/viewCase.html', context)
        elif new_document[0] == False:
            context = {'documents': get_documents(), 'cases': get_cases(request),
                       'upload_fail': True}
            return render(request, 'autoIntern/homePage.html', context)
        elif 'case_id' in request.POST:
            case.documents.add(new_document[1])
            context = {'documents': get_docs_in_case(cur_case_id),
                       'case_name': case.case_name, 'case_id': case.case_id}
            if user_perms.filter(user_type=models.Permissions.MANAGER_USER).count() > 0:
                context['is_manager'] = True
            else:
                context['is_manager'] = False
            return render(request, 'autoIntern/viewCase.html', context)
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


@login_required(redirect_field_name='', login_url='/')
def exportTags(request):
    """ Exports tags associated with document"""
    # Identifiers for documents:
    IDS = ['company', 'doc_type', 'doc_date']
    if request.method == 'POST':
        try:
            path = request.POST['path']
            doc_id = path.split("=", maxsplit=1)[1]
            doc = models.Document.objects.get(doc_id=doc_id)

            #doc_ids => contains document identifiers
            vals = doc.__dict__
            doc_ids = {tag: vals[tag] for tag in IDS}

            #data_tags => contains document tags
            data = models.Data.objects.all().filter(document=doc)
            data_tags = {tag.label: tag.value for tag in data}

            #Combine
            dict_tags = {**doc_ids, **data_tags}

            #Create json
            js = json.dumps(dict_tags)
            conv = json.loads(js)

            if 'csv' in request.POST:
                # Create the HttpResponse object with the appropriate CSV header.
                response = HttpResponse(content_type='text/csv; charset=utf8')
                response['Content-Disposition'] = 'attachment; filename="%s_%s_%s_tags.csv"' % \
                                                  (vals[IDS[0]], vals[IDS[1]], vals[IDS[2]])

                writer = csv.writer(response)
                for tag in dict_tags:
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
                response['Content-Disposition'] = 'attachment; filename="%s_%s_%s_tags.txt"' % \
                                                  (vals[IDS[0]], vals[IDS[1]], vals[IDS[2]])

            elif 'json' in request.POST:
                response = HttpResponse(js, content_type='application/javascript; charset=utf8')
                response['Content-Disposition'] = 'attachment; filename="%s_%s_%s_tags.json"' % \
                                                  (vals[IDS[0]], vals[IDS[1]], vals[IDS[2]])
            else:
                return HttpResponseRedirect('/')

            return response
        except:
            return HttpResponseRedirect('/error')
    else:
        return HttpResponseRedirect('/')


@login_required(redirect_field_name='', login_url='/')
def exportTagsCase(request):
    """ Exports tags across documents"""
    # Identifiers for documents:
    IDS = ['company', 'doc_type', 'doc_date']
    if request.method == 'POST':
        try:
            doc_ids = request.POST.getlist('doc_ids[]')

            all_tags = {}

            for id in doc_ids:
                doc = models.Document.objects.get(doc_id=id)
                vals = doc.__dict__

                doc_tags = {tag: vals[tag] for tag in IDS}

                # data_tags => contains document tags
                data = models.Data.objects.all().filter(document=doc)
                data_tags = {tag.label: tag.value for tag in data}

                # Combine
                dict_tags = {**doc_tags, **data_tags}

                all_tags[id] = dict_tags

            # Create set of all possible labels
            labels = set()
            for dict in all_tags:
                labels.update(all_tags[dict].keys())

            # Create the HttpResponse object with the appropriate CSV header.
            response = HttpResponse(content_type='text/csv; charset=utf8')
            response['Content-Disposition'] = 'attachment; filename="tags_across_documents.csv"'

            header = ['']
            header.extend(doc_ids)

            writer = csv.writer(response)
            writer.writerow(header)

            for label in labels:
                row = [label]

                for id in doc_ids:
                    curr_tags = all_tags[id]
                    if label in curr_tags:
                        row.append(curr_tags[label])
                    else:
                        row.append('')

                writer.writerow(row)

            return response

        except:
            return HttpResponseRedirect('/error')
    else:
        return HttpResponseRedirect('/')


@login_required(redirect_field_name='', login_url='/')
def createCase(request):
    """ Handles creation of new case"""
    currUser = User.objects.get(username=request.user)
    new_case_name = request.POST['caseName']
    cases = models.Case.objects.all().filter(case_name=new_case_name)
    while cases.count() != 0:
        if new_case_name == request.POST['caseName']:
            new_case_name += '(1)'
        else:
            new_int = int(new_case_name[-2]) + 1
            new_case_name = new_case_name[:-3] + "(" + str(new_int) + ")"
        cases = models.Case.objects.all().filter(case_name=new_case_name)

    new_case = models.Case(case_name=new_case_name)

    new_case.save()
    new_case.user_permissions.add(currUser)

    new_perm = models.Permissions(user=currUser, case=new_case,
                                  user_type=models.Permissions.MANAGER_USER)
    new_perm.save()

    return HttpResponseRedirect('/')


@login_required(redirect_field_name='', login_url='/')
def addUsers(request):
    """ Adds user(s) to specified case """
    try:
        ids = request.POST.getlist('ids[]')
        case_id = request.POST['case_id']

        case = models.Case.objects.get(case_id=case_id)
        currUser = User.objects.get(username=request.user)

        # If non-manager tries to call function => shouldn't happen since button only seen by managers
        user_type = models.Permissions.objects.get(case=case, user=currUser).user_type
        if user_type != models.Permissions.MANAGER_USER:
            return HttpResponseRedirect('/')

        for id in ids:
            user = User.objects.get(username=id)
            case.user_permissions.add(user)

            new_perm = models.Permissions(user=user, case=case, user_type=models.Permissions.BASE_USER)
            new_perm.save()

        context = {'documents': get_docs_in_case(case_id),
                   'case_name': case.case_name, 'case_id': case_id}

        return viewCase(request)
    except:
        return HttpResponseRedirect('/error')


@login_required(redirect_field_name='', login_url='/')
def removeUsers(request):
    """ Removes user(s) from specified case"""
    try:
        ids = request.POST.getlist('ids[]')
        case_id = request.POST['case_id']

        case = models.Case.objects.get(case_id=case_id)
        currUser = User.objects.get(username=request.user)

        # If non-manager tries to call function => shouldn't happen since button only seen by managers
        if models.Permissions.objects.get(case=case, user=currUser).user_type != models.Permissions.MANAGER_USER:
            return HttpResponseRedirect('/')

        for id in ids:
            user = User.objects.get(username=id)
            case.user_permissions.remove(user)

            models.Permissions.objects.filter(case=case, user=user).delete()

        context = {'documents': get_docs_in_case(case_id),
                   'case_name': case.case_name, 'case_id': case_id}

        return viewCase(request)
    except:
        return HttpResponseRedirect('/error')


#Don't need to be logged in to view the css or js files
def getCss(request):
    """Super hacky way to serve the css content of the site"""
    css = ''
    try:
        with open('./static/autoInternBase.css') as css:
            string = css.read()
        return HttpResponse(string)
    except:
        return HttpResponseRedirect('/error')

def getJs(request):
    """Super hacky way to serve the js content of the site"""
    js = ''
    try:
        with open('./static/autoInternBase.js') as js:
            string = js.read()
        return HttpResponse(string)
    except:
        return HttpResponseRedirect('/error')

def showError(request):
    """ Renders the error page """
    context = {}
    return render(request, 'autoIntern/error.html', context)