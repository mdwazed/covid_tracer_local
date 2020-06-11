from django import forms
from django.db import models
from django.forms import ModelForm

from app_user.models import PersInfo


rank_choices = [
    ('snk', 'Snk'),
    ('lcpl', 'Lcpl')
]
    


class PersInfoForm(ModelForm):
    rank = forms.ChoiceField(choices=rank_choices)
    class Meta:
        model = PersInfo
        labels = {
            
        }
        fields = ['user_gen_id', 'app_gen_id', 'pers_num', 'rank', 'name',  'unit', 'mobile_num']