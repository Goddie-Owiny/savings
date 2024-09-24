from django.urls import path
from . views import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name='savingsApp/login.html'), name="login"), #login route
    path('', dashboard, name='dashboard'),
    path('mem_reg', mem_reg, name='mem_reg'),
    path('member_detail/<int:pk>', member_detail_and_loan, name='member_detail'),
    path('save/<int:id>', save, name='save'),
    # path('loan', loan, name='loan'),

    path('logout/', logout_view, name='logout'), #logout route
] 


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)