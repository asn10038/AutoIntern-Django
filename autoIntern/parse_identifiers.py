
from django.db import models
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from autoIntern.models import Document



def GetDocumentByHeader( doc_file, contr_user):
    content = doc_file.read()
    header = str(content,'utf-8')
    header = header.split('\n')[:45]
    # print(header)
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
    new_doc = Document(company= company , doc_type= doc_type, doc_date= doc_date,
                                doc_id =  doc_id, file = default_storage.save('static/document_folder/{0}'.format(doc_id),
                                ContentFile(content)), upload_id = contr_user)
    return(new_doc)