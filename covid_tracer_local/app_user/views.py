from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist, ValidationError, MultipleObjectsReturned
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views import View
from django.conf import settings
from django.core import serializers
from django.urls import reverse_lazy 
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import F, Q, Count

from app_user.forms import PersInfoForm

# Create your views here.
def home(request):
    return render(request, 'app_user/home.html')


class AddAppUser(View):
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
