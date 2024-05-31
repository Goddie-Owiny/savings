from django.shortcuts import render
from . models import *

# Create your views here.
def dashboard(request):
    user = Member.objects.all()
    return render(request, 'savingsApp/dashboard.html' , {'user': user})