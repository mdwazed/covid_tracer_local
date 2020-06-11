from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist, ValidationError, MultipleObjectsReturned
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views import View
from django.conf import settings
from django.core import serializers
from django.urls import reverse_lazy 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import F, Q, Count

from app_user.forms import PersInfoForm, LoginForm
from app_user.models import PersInfo

# Create your views here.
def home(request):
    return render(request, 'app_user/home.html')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')

def login_view(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'app_user/login.html', {'form': form})

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            form = LoginForm(request.POST)
            msg = 'Login Failed'
            context = {
                'form': form,
                'msg': msg,
            }
            return render(request, 'app_user/login.html', context)

class AddAppUserView(View):
    """ add pers info of a new app user """
    template = 'app_user/add_single_user.html'
    def get(self, request):
        form = PersInfoForm()
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request):
        form = PersInfoForm(request.POST)
        if form.is_valid():
            form.save()
            success_msg = 'App user saved successfully.'
            return render(request, self.template, {'success_msg': success_msg})
        else:
            context = {
                'form': form,
            }
            return render(request, self.template, context)

class UsersListView(ListView):
    """ display truncated user list with option to delete any one """
    model = PersInfo
    template_name = 'app_user/users_list.html'


def delete_app_user(request):
    """ delete an app user of given id """
    if request.method == "POST":
        try:
            app_user_id = request.POST['app_user_id']
        except ObjectDoesNotExist:
            return HttpResponse(status=404)
        PersInfo.objects.get(pk=app_user_id).delete()
        return HttpResponse(status=204)

def search_app_user(request):
    """ Display an app user for admin purpose """
    pass
        
    
