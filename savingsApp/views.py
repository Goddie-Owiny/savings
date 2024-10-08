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
from django.db.models import Sum, ExpressionWrapper, DecimalField, F
from django.db.models.functions import TruncMonth
import pandas as pd   # type: ignore
import plotly.express as px     # type: ignore
from plotly.offline import plot  # type: ignore

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
    pie_chart_layout = go.Layout(title='Savings Breakdown', width=600, height=500)
    pie_chart = go.Figure(data=[pie_chart_data], layout=pie_chart_layout)
    pie_chart_json = pio.to_json(pie_chart)     # convert to json

    # Data for the line chart
    weekly_savings = [150, 635, 175, 800, 190, 510, 360]
    weekly_loans = [75, 232, 85, 20, 44, 23, 50]
    weekly_welfares = [5, 22, 385, 80, 44, 23, 10]
    days_of_week = ['MoN', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']

    # Create the line chart with both savings and loans
    fig = go.Figure()

    # Drawing chart lines
    fig.add_trace(go.Scatter(x=days_of_week, y=weekly_savings, mode='lines+markers', name='Weekly Savings', line=dict(color='#1e3a8a')))   # weekly Savings

    fig.add_trace(go.Scatter(x=days_of_week, y=weekly_loans, mode='lines+markers', name='Weekly Loans', line=dict(color='brown')))      # weekly Loans

    fig.add_trace(go.Scatter(x=days_of_week, y=weekly_welfares, mode='lines+markers', name='Weekly Welfares', line=dict(color='green')))  # weekly welfares

    # Update layout for better visualization
    fig.update_layout(
        title='Line Chart',
        xaxis_title='Days of the Week',
        yaxis_title='Amount (UGX)',
        template='plotly'
    )

    # Displaying the chart
    line_chart_json = pio.to_json(fig) 

    context = {
        'total_members': total_members,
        'total_savings': total_savings,
        'average_savings': average_savings,
        'page_obj': page_obj,
        'pie_chart_json': pie_chart_json,  
        'bar_chart_json': line_chart_json,   # convert to json
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

# @login_required
# def member_detail(request, pk):
#     member = get_object_or_404(Member, id=pk)
#     savings = Save.objects.all()
#     loans = Loan.objects.all()
#     return render(request,'savingsApp/member_detail.html', {'member': member,'savings': savings, 'loans': loans})

@login_required
def member_detail_and_loan(request, pk):
    # Get the member details
    member = get_object_or_404(Member, id=pk)
    member_details = Member.objects.all()
    
    # Filter savings related to the member
    savings = Save.objects.filter(member=member)
    
    # Filter loans related to the member's savings
    loans = Loan.objects.filter(reciever__member=member) 
    
    # Handle the loan form, pre-fill the reciever with the first saving record
    form = LoanForm(reciever=savings.first())
    
    if request.method == 'POST':
        form = LoanForm(request.POST, reciever=savings.first())
        if form.is_valid():
            loan = form.save(commit=False)
            loan.save()
            return redirect('dashboard')

    # Render the template with both member details and loan form
    return render(request, 'savingsApp/member_detail.html', {
        'member': member_details,
        'savings': savings,
        'loans': loans,
        'form': form
    })

@login_required
def save(request, id):
    current_save = get_object_or_404(Save, id=id)
    
    if request.method == 'POST':
        form = SavingsForm(request.POST, member=current_save.member)
        if form.is_valid():
            moreSavings = form.cleaned_data.get('amount')  # Use cleaned_data to get the validated data
            if moreSavings:
                try:
                    current_save.amount += moreSavings  # Assuming current_save.amount is an integer or float
                    current_save.save()
                    return redirect('dashboard')
                except ValueError:
                    return HttpResponseBadRequest('Invalid amount')
    else:
        form = SavingsForm(member=current_save.member)
    
    return render(request, 'SavingsApp/save.html', {'form': form})

#giving loans
# @login_required
# def loan(request):
#     form = LoanForm()
#     if request.method == 'POST':
#         form = LoanForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('dashboard')
    
#     return render(request, 'savingsApp/member_detail.html' , {'form': form})






@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('login'))  # Assuming you have a URL pattern named 'login'
