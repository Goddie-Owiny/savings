from . models import *
from django.forms import ModelForm


class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = '__all__'


class SavingsForm(ModelForm):
    class Meta: 
        model = Save
        fields = ['member', 'amount', 'save_time']