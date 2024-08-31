from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import logout
from django.db.models import Q
from . models import *
from . forms import *
import plotly.graph_objects as go   # type: ignore
import plotly.io as pio    # type: ignore

# Create your views here.
@login_required
def dashboard(request):
    total_members = Member.objects.count()
    total_savings = Save.objects.aggregate(total_savings=models.Sum('amount'))['total_savings'] or 0
    total_loan = Loan.objects.aggregate(total_loan=models.Sum('amount_borrowed'))['total_loan'] or 0
    average_savings = Save.objects.aggregate(average_savings=models.Avg('amount'))['average_savings'] or 0

    search_query = request.GET.get('search', '')
    if search_query:
        member_list = Member.objects.filter(
            Q(name__icontains=search_query) |
            Q(contact__icontains=search_query)
        ).order_by('id')
    else:
        member_list = Member.objects.all().order_by('id')
    
    paginator = Paginator(member_list, 10)  # Show 10 members per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pie chart data
    pie_chart_labels = ['Total Loans', 'Average Savings']
    pie_chart_values = [total_loan, average_savings]
    pie_chart_colors = ['#374151', '#1e3a8a']
    pie_chart_data = go.Pie(labels=pie_chart_labels, values=pie_chart_values, marker=dict(colors=pie_chart_colors))
    pie_chart_layout = go.Layout(title='Savings Breakdown')
    pie_chart = go.Figure(data=[pie_chart_data], layout=pie_chart_layout)
    pie_chart_json = pio.to_json(pie_chart)     # convert to json

    context = {
        'total_members': total_members,
        'total_savings': total_savings,
        'average_savings': average_savings,
        'page_obj': page_obj,
        'pie_chart_json': pie_chart_json,  
        # other context variables...
    }
    
    return render(request, 'savingsApp/dashboard.html', context)


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
