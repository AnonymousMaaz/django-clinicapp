from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import StaffForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import UserProfile, MedicalRecord
from bookings.models import Booking
from django.http import HttpResponseForbidden

def register(request):
    next_url = request.GET.get('next', 'home')
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )
                user.save()
                
                # Create UserProfile instance
                UserProfile.objects.create(user=user)

                login(request, user)
                return redirect(next_url)
        else:
            messages.error(request, 'Form is not valid')
    else:
        form = StaffForm()

    return render(request, 'accounts/register.html', {'form': form, 'next': next_url})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def add_staff(request):
    form = None  # Initialize form variable

    if request.method == 'POST':
        action = request.POST.get('action')
        search_query = request.POST.get('search_query')

        if action == 'search':
            if search_query:
                try:
                    staff = User.objects.get(email=search_query)
                    form = StaffForm(instance=staff)  # Populate the form with the staff details
                    return render(request, 'accounts/add_staff.html', {'form': form, 'staff': staff})
                except User.DoesNotExist:
                    messages.error(request, 'No staff found with that email.')

        elif action == 'delete':
            if search_query:
                try:
                    staff = User.objects.get(email=search_query)
                    staff.delete()
                    messages.success(request, 'Staff deleted successfully.')
                    return redirect('accounts:add_staff')  # Redirect to clear the form and messages
                except User.DoesNotExist:
                    messages.error(request, 'Staff not found.')

        elif action == 'add':
            form = StaffForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Staff added successfully.')
                return redirect('accounts:add_staff')  # Redirect to clear the form and messages
            else:
                messages.error(request, 'Error in form submission.')
                # Debugging info
                print("Form errors:", form.errors)  # Print form errors to console/log

    # Handle GET request and initial display
    if form is None:
        form = StaffForm()

    return render(request, 'accounts/add_staff.html', {'form': form})

@login_required
def profile_view(request, user_id=None):
    if user_id:
        user = get_object_or_404(User, pk=user_id)
        if not request.user.is_superuser and user != request.user:
            return HttpResponseForbidden("You do not have permission to view this profile.")
    else:
        user = request.user

    profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST' and (user == request.user or request.user.is_superuser):
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
            profile.save()
            messages.success(request, 'Profile picture updated successfully.')
            return redirect('accounts:profile')

    transactions = Booking.objects.filter(user=user)
    medical_records = MedicalRecord.objects.filter(user=user)

    context = {
        'profile': profile,
        'transactions': transactions,
        'medical_records': medical_records
    }

    return render(request, 'accounts/profile.html', context)

@user_passes_test(lambda u: u.is_superuser)
def all_profiles(request):
    profiles = UserProfile.objects.all()
    return render(request, 'accounts/all_profiles.html', {'profiles': profiles})