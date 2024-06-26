from django.shortcuts import render, redirect, get_object_or_404
from . models import *
from . forms import *
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views here.
@login_required
def dashboard(request):
    user = Member.objects.all().order_by('name')
    return render(request, 'savingsApp/dashboard.html' , {'user': user})

@login_required
def mem_reg(request):
    form = MemberForm()
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print(form)
            return redirect('dashboard')
    
    return render(request, 'savingsApp/mem_reg.html' , {'form': form})



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
    return redirect('/login') # redirect user to the login page
