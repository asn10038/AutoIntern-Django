from django.db import models
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from autoIntern.models import Document, Case
from django.core.exceptions import ObjectDoesNotExist
import os
import datetime


def GetDocumentByHeader( doc_file, contr_user, public=True, doc_name = ''):
    content = doc_file.read()
    header = str(content,'utf-8')
    header = header.split('\n')[:45]
    is_formdoc = True
    company = ''
    doc_type = ''
    doc_date = ''
    for line in header:
        split =  line.split(':')
        if '<SEC-DOCUMENT>' in split[0]:
            doc_date = split[1].strip()
        if 'CONFORMED SUBMISSION TYPE' in split[0]:
            doc_type = split[1].strip()
        if 'COMPANY CONFORMED NAME' in split[0]:
            company = split[1].strip()
            company = company.replace(' ', '_')
            company = company.replace('/','')


    doc_id = company+'.'+ doc_type + '.' + doc_date + '.txt'

    # checks for the case that file is not a formdoc
    if company == '' or doc_type == '' or doc_date =='':
        is_formdoc = False
        doc_id = str(doc_file)
        if doc_name != '':
            company = doc_name
        else:
            company = doc_id
        doc_type = 'note'
        doc_date = datetime.datetime.now().strftime("%Y%m%d")


    if DNE_Doc_or_Fail(doc_id):
        new_doc = Document(company=company, doc_type=doc_type,
                           doc_date=doc_date, doc_id=doc_id, file=default_storage.save('static/document_folder/{0}'.format(doc_id),ContentFile(content)),
                           upload_id = contr_user, public=public)
        new_doc.save()
        return(True, new_doc)
    else:
        return(False, doc_id)

def DNE_Doc_or_Fail(doc_id):
    try:
        doc = Document.objects.get(doc_id= doc_id)
        return(False)
    except ObjectDoesNotExist:
        return(True)

def get_documents():
    return Document.objects.all().filter(public=True)

def get_cases(request):
    return Case.objects.all().filter(user_permissions=request.user)

def get_docs_in_case(case_id):
    case = Case.objects.get(case_id = case_id)
    documents = []

    for document in case.documents.all():
        documents.append(document)
    return documents

def valid_file_type(file_name):
    ext = os.path.splitext(file_name)[1]
    valid_extensions = ['.txt']
    if not ext in valid_extensions:
        return(False)
    else:
        return(True)