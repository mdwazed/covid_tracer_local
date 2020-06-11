

from django.urls import path, include

from app_user import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_app_user', views.AddAppUser.as_view(), name='add_app_user'),
]