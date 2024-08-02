from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import logout
from . models import *
from . forms import *

# Create your views here.
@login_required
def dashboard(request):
    member_list = Member.objects.all().order_by('id')
    paginator = Paginator(member_list, 10)  # Show 10 members per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'savingsApp/dashboard.html', {'page_obj': page_obj} )

@login_required
@login_required
def mem_reg(request):
    form = MemberForm()
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            # Render the form with errors
            return render(request, 'savingsApp/mem_reg.html', {'form': form})
  
    return render(request, 'savingsApp/mem_reg.html', {'form': form})



@login_required
def save(request, id):
    current_save = get_object_or_404(Save, id=id)
    if request.method == 'POST':
        form = SavingsForm(request.POST)
        if form.is_valid():
            moreSavings = form.cleaned_data.get('amount')  # Use cleaned_data to get the validated data
            if moreSavings:
                try:
                    current_save.amount += moreSavings  # Assuming current_save.amount is an integer or float
                    current_save.save()
                    print(current_save.amount)
                    print(current_save)
                    return redirect('dashboard')
                except ValueError:
                    return HttpResponseBadRequest('Invalid quantity')
    else:
        form = SavingsForm()
    return render(request, 'SavingsApp/save.html', {'form': form})

#giving loans
@login_required
def loan(request):
    form = LoanForm()
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    
    return render(request, 'savingsApp/give_loan.html' , {'form': form})






@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('login'))  # Assuming you have a URL pattern named 'login'
