from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import (ObjectDoesNotExist, ValidationError, 
        MultipleObjectsReturned, EmptyResultSet)
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

from app_user.forms import (PersInfoForm, LoginForm, UserSearchForm,)
from app_user.models import PersInfo
from app_user.utils import ContactedUser

from datetime import datetime, timedelta

import requests
from requests.exceptions import HTTPError
import json

# Create your views here.

class ForceLoginView(LoginRequiredMixin, View):
    login_url = '/login/'


def home(request):
    past_date = datetime.today()
    context = {
        'past_date': past_date,
    }
    return render(request, 'app_user/home.html', context)

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
            # http call here to validate id pair from backend server
            user_gen_id = form.cleaned_data['user_gen_id']
            app_gen_id = form.cleaned_data['app_gen_id']
            url = f'http://dev.workspaceit.com:8081/api/v1/user/valid/key/?user_gen_key={user_gen_id}&app_gen_key={app_gen_id}'
            try:
                response = requests.get(url)
            except (HTTPError, requests.ConnectionError):
                err_msg = "Error. Couldn't connect to the backend server."
                return render(request, self.template, {'err_msg': err_msg})
            if response.status_code == 200:
                r_user = json.loads(response.text)
                print(r_user)
                if not r_user['status']:
                    err_msg = "Not a valid user. Check ID pair."
                    return render(request, self.template, {'err_msg': err_msg})
                else:
                    form.save()
                    success_msg = 'App user saved successfully.'
                    return render(request, self.template, {'success_msg': success_msg})
            else:
                err_msg = "Something went wrong in remote call. Contact Admin."
                return render(request, self.template, {'err_msg': err_msg})
        else:
            context = {
                'form': form,
            }
            return render(request, self.template, context)

# class UsersListView(ListView):
#     """ display truncated user list with option to delete any one """
#     model = PersInfo
#     template_name = 'app_user/users_list.html'

class FilteredUsersListView(ForceLoginView):
    """ display users list based on search criteria """
    template = 'app_user/users_list.html'
    def get(self, request):
        form = UserSearchForm()
        users = PersInfo.objects.all()[:100]
        context = {
            'form': form,
            'users': users,
        }
        return render(request, self.template, context)
    def post(self, request):
        try:
            unit = request.POST['unit']
            rank = request.POST['rank']
            app_gen_id = request.POST.get('app_gen_id', None)
            print(f'app genid: {app_gen_id}')
        except ValueError:
            pass
        if app_gen_id:
            users = PersInfo.objects.filter(app_gen_id=app_gen_id)
        else:
            users = PersInfo.objects.filter(unit=unit, rank=rank)
        form = UserSearchForm()
        context = {
            'users': users,
            'form': form,
        }
        return render(request, self.template, context)

def delete_app_user(request):
    """ delete an app user of given id """
    if request.method == "POST":
        try:
            app_user_id = request.POST['app_user_id']
        except ObjectDoesNotExist:
            return HttpResponse(status=404)
        PersInfo.objects.get(pk=app_user_id).delete()
        return HttpResponse(status=204)

class GetContactsView(ForceLoginView):
    """ Receive the person to be traced  and send API request"""
    template = 'app_user/get_contacts.html'

    def get(self, request):

        context = {

        }
        return render(request, self.template, context)

    def post(self, request):
        try:
            app_gen_id = request.POST.get('app-gen-id')
            app_user = PersInfo.objects.get(app_gen_id=app_gen_id)
        except (ValueError, ObjectDoesNotExist) as e:
            err_msg = "Enter a valid ID." + str(e)
            return render(request, self.template, {'err_msg':err_msg})
        context = {
            'app_user': app_user,
        }
        return render(request, self.template, context)

class GetContactListView(ForceLoginView):
    """ Returns a list of contacted app_users from back end"""
    template = 'app_user/contacted_list.html'

    def post(self, request):
        # print(request.POST)
        try:
            app_user_id = request.POST.get('app-user-id', None)
            from_date = request.POST.get('from-date', None)
            to_date = request.POST.get('to-date', None)
        except ValueError as e:
            err_msg = "Post data error" + str(e)
            return render(request, self.template, {'err_msg': err_msg})
        try:
            source_user = PersInfo.objects.get(pk=app_user_id)
        except ObjectDoesNotExist:
            err_msg = "User doesn't exists."
            return render(request, self.template, {'err_msg': err_msg})
        if app_user_id and from_date and to_date:
            from_date_obj = datetime.strptime(from_date, '%d-%m-%Y')
            from_date_timestamp = int(datetime.timestamp(from_date_obj))
            to_date_obj = datetime.strptime(to_date, '%d-%m-%Y')
            to_date_obj = to_date_obj + timedelta(days=1)
            to_date_timestamp = int(datetime.timestamp(to_date_obj))
            app_gen_key = source_user.app_gen_id
        else:
            err_msg = "Please select both from and to date."
            return render(request, self.template, {'err_msg': err_msg})
        # API call to get the list of contacted pers
        url = f"http://dev.workspaceit.com:8081/api/v1/user/get/contact/?"\
            f"app_gen_key={app_gen_key}&range_start={from_date_timestamp}&range_end={to_date_timestamp}"
        print(url)
        try:
            response = requests.get(url)
        except (HTTPError, requests.ConnectionError):
            err_msg = "Error. Couldn't connect to the backend server."
            return render(request, self.template, {'err_msg': err_msg})
        if response.status_code == 200:
            contact_data = json.loads(response.text)
            # print(contact_data)
            contacted_users = []
            for contact in contact_data['data']:
                try:
                    contacted_user = PersInfo.objects.get(app_gen_id=contact['user_id']) 
                    # print(contacted_user)
                except ObjectDoesNotExist:
                    pass
                else:
                    con_user = ContactedUser(contacted_user, contact['contact_time'])
                    contacted_users.append(con_user)
            # contacted_users = set(contacted_users)
            context = {
                'source': source_user,
                'contacted_users': contacted_users,
                'from_date': from_date,
                'to_date': to_date,
            }
            return render(request, self.template, context)
        else:
            err_msg = "Remote server did not return 200."
            return render(request, self.template, {'err_msg': err_msg})
        
    
