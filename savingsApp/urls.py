from django.urls import path
from . views import *


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('mem_reg', mem_reg, name='mem_reg'),
    path('save/<int:id>', save, name='save'),
    path('loan', loan, name='loan'),
] 
