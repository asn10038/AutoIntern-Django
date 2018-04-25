'''
Contains helper functions used in views.py
'''

import os
import datetime
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from autoIntern.models import Document, Case


def get_document_by_header(doc_file, contr_user, public=True, doc_name=''):
    """
    Parses company name, doc_type, and date from financial document
    """
    content = doc_file.read()
    header = str(content, 'utf-8')
    header = header.split('\n')[:45]
    company,doc_type,doc_date,doc_id = get_form_doc(header)
    company,doc_type,doc_date,doc_id = get_note(company,doc_type,doc_date,doc_id,doc_name,doc_file)

    # if the document id already exists in our system, returns ( false , doc_id string )
    if Document.objects.filter(doc_id=doc_id).exists():
        return False, doc_id
    # if the document isn't in the system yet, saves the new document and returns (true, new document object)
    else:
        new_doc = Document(company=company, doc_type=doc_type,
                           doc_date=doc_date, doc_id=doc_id,
                           file=default_storage.save('static/document_folder/{0}'.format(doc_id),
                            ContentFile(content)),upload_id=contr_user, public=public)
        new_doc.save()
        return True, new_doc


def get_form_doc(header):
    """
    checks the header for html tags that indicate fields in the form document
    """
    company = ''
    doc_type = ''
    doc_date = ''
    for line in header:
        split = line.split(':')
        if '<SEC-DOCUMENT>' in split[0]:
            doc_date = split[1].strip()
            doc_date = doc_date[4:6]+ '-' + doc_date[6:]+'-' + doc_date[:4]
        if 'CONFORMED SUBMISSION TYPE' in split[0]:
            doc_type = split[1].strip()
        if 'COMPANY CONFORMED NAME' in split[0]:
            company = split[1].strip()
            company = company.replace(' ', '_')
            company = company.replace('/', '')
    doc_id = company + '.' + doc_type + '.' + doc_date + '.txt'
    return company, doc_type, doc_date, doc_id


def get_note(company,doc_type,doc_date,doc_id,doc_name,doc_file):
    """
    checks for missing fields formdoc field and returns appropriate identifiers if it is a note
    """
    print('start note')
    if company == '' or doc_type == '' or doc_date == '':
        doc_id = str(doc_file)
        if doc_name != '':
            company = doc_name
        else:
            company = doc_id
        doc_type = 'note'
        doc_date = datetime.datetime.now().strftime("%m-%d-%Y")

    print('end')
    return company, doc_type, doc_date, doc_id

def get_documents():
    """
    Returns all documents in the system
    """
    return Document.objects.all().filter(public=True)


def get_cases(request):
    """
    Returns all cases the current user is a member of
    """
    return Case.objects.all().filter(user_permissions=request.user)


def get_docs_in_case(case_id):
    """
    Returns all documents associated with a particular case_id
    """
    case = Case.objects.get(case_id=case_id)
    documents = []

    for document in case.documents.all():
        documents.append(document)

    return documents


def valid_file_type(file_name):
    """
    Checks if a file is of an approved extension type
    """
    valid_extensions = ['.txt']
    ext = os.path.splitext(file_name)[1]

    if ext in valid_extensions:
        return True

    return False
