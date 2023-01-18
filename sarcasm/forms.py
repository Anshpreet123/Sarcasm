from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class StageForm(forms.Form):
	answer = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'accordion_ans'}))