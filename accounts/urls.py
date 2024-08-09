from django.urls import path
from . import views
from .views import profile_view
from .views import profile_view, all_profiles

app_name = 'accounts'  # Define the namespace

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add_staff/', views.add_staff, name='add_staff'), 
    path('profile/', views.profile_view, name='profile'), # Add this line for the new view
    path('profile/<int:user_id>/', views.profile_view, name='profile_with_id'),  # URL pattern for user profiles with user_id
    path('all_profiles/', views.all_profiles, name='all_profiles'),
]
    