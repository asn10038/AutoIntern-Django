from django.conf.urls import url
from .views import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'register/', views.register, name='register'),
    url(r'login/', views.login, name='login'),
    url(r'logout/', views.logout, name='logout'),
    url(r'upload/',views.upload, name='upload'),
    url(r'viewDocument', views.viewDocument, name='viewDocument')
]
