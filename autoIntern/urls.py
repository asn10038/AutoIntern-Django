"""Hooks urls up to backend functions in views"""
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from autoIntern import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'register/', views.register, name='register'),
    url(r'userLogin/', views.user_login, name='login'),
    url(r'userLogout/', views.user_logout, name='logout'),
    url(r'upload/', views.upload, name='upload'),
    url(r'viewDocument', views.view_document, name='viewDocument'),
    url(r'viewCase', views.view_case, name='viewCase'),
    url(r'exportTags/', views.export_tags, name='exportTags'),
    url(r'exportTagsCase/', views.export_tags_case, name='exportTagsCase'),
    url(r'addUsers/', views.add_users, name='addUsers'),
    url(r'removeUsers/', views.remove_users, name='removeUsers'),
    url(r'createCase/', views.create_case, name='createCase'),
    url(r'createTag/', views.create_tag, name='createTag'),
    url(r'changePassword/', auth_views.PasswordChangeView.as_view(
        template_name='registration/passwordChangeForm.html',
        success_url='/',), name='changePassword'),
    url(r'static/autoInternBase.css', views.get_css, name='getcss'),
    url(r'static/autoInternBase.js', views.get_js, name='getjs')
]
