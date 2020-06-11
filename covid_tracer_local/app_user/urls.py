

from django.urls import path, include

from app_user import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_app_user/', views.AddAppUserView.as_view(), name='add_app_user'),
    path('users_list/', views.UsersListView.as_view(), name='users_list'),
    path('delete_app_user/', views.delete_app_user, name='delete_app_user'),
]