from django.urls import path
from . views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name='savingsApp/login.html'), name="login"), #login route
    path('', dashboard, name='dashboard'),
    path('mem_reg', mem_reg, name='mem_reg'),
    path('save/<int:id>', save, name='save'),
    path('loan', loan, name='loan'),

    path('logout/', logout_view, name='logout'), #logout route
] 
