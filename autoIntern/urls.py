from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .views import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'register/', views.register, name='register'),
    url(r'userLogin/', views.userLogin, name = 'login'),
    url(r'userLogout/', views.userLogout, name='logout'),
    url(r'upload/',views.upload, name='upload'),
    url(r'viewDocument', views.viewDocument, name='viewDocument'),
    url(r'viewCase', views.viewCase, name='viewCase'),
    url(r'exportTags/', views.exportTags, name='exportTags'),
    url(r'addUsers/', views.addUsers, name='addUsers'),
    url(r'removeUsers/', views.removeUsers, name='removeUsers'),
    url(r'createCase/', views.createCase, name='createCase'),
    url(r'createTag/',views.createTag, name='createTag'),
    url(r'changePassword/', auth_views.PasswordChangeView.as_view(
        template_name='registration/passwordChangeForm.html',
        success_url='/',), name='changePassword')
]
