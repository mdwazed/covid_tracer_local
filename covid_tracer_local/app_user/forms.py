from django import forms
from django.db import models
from django.forms import ModelForm

from app_user.models import PersInfo


rank_choices = [
    ('Snk', 'Snk'),
    ('Lcpl', 'Lcpl'),
    ('Cpl', 'Cpl'),
    ('Sgt', 'Sgt'),
    ('WO', 'WO'),
    ('SWO', 'SWO'),
    ('MWO', 'MWO'),
    ('2 Lt', '2 Lt'),
    ('Lt', 'Lt'),
    ('Capt', 'Capt'),
    ('Maj', 'Maj'),
    ('Lt_Col', 'Lt Col'),
    ('Col', 'Col'),
    ('Brig Gen', 'Brig Gen'),
    ('Maj Gen', 'Maj Gen'),
]
    

class LoginForm(forms.Form):
    username = forms.CharField(label='User Name', max_length=20)
    password = forms.CharField(label='Password', max_length=20, widget=forms.PasswordInput)

class PersInfoForm(ModelForm):
    rank = forms.ChoiceField(choices=rank_choices)
    class Meta:
        model = PersInfo
        labels = {
            
        }
        fields = ['user_gen_id', 'app_gen_id', 'pers_num', 'rank', 'name',  'unit', 'mobile_num']