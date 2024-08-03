from django.urls import path
from . import views

app_name = 'accounts'  # Define the namespace

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add_staff/', views.add_staff, name='add_staff'),  # Add this line for the new view
]
