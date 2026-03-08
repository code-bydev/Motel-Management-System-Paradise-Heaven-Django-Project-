
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Sum, Q
from datetime import datetime, timedelta

from .forms import AdminLoginForm, AdminRegistrationForm, RoomTypeForm, IndividualRoomForm
from .models import AdminUser
from motel.models import Rooms, Room, Bookings, UserAccount


def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')
    
    return render(request, 'custom_admin/login.html')


def admin_register(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            
            if AdminUser.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
                return render(request, 'custom_admin/login.html', {'show_register': True})
            
            if AdminUser.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered!')
                return render(request, 'custom_admin/login.html', {'show_register': True})
            
            admin_user = AdminUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            admin_user.is_staff = True
            admin_user.save()
            
            messages.success(request, 'Admin account created successfully! Please login.')
            return redirect('admin_login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = AdminRegistrationForm()
    
    return render(request, 'custom_admin/login.html', {'show_register': True, 'form': form})


def admin_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('admin_login')


@login_required(login_url='admin_login')
def admin_dashboard(request):
    total_rooms = Rooms.objects.count()
    total_bookings = Bookings.objects.count()
    total_users = UserAccount.objects.count()
    
    total_revenue = Bookings.objects.aggregate(Sum('roomname__room_price'))['roomname__room_price__sum'] or 0
    
    recent_bookings = Bookings.objects.select_related('roomname').order_by('-id')[:5]
    
    available_rooms = Room.objects.filter(is_available=True).count()
    occupied_rooms = Room.objects.filter(is_available=False).count()
    total_individual_rooms = Room.objects.count()
    
    room_categories = Rooms.objects.all()
    
    context = {
        'total_rooms': total_rooms,
        'total_bookings': total_bookings,
        'total_users': total_users,
        'total_revenue': total_revenue,
        'recent_bookings': recent_bookings,
        'available_rooms': available_rooms,
        'occupied_rooms': occupied_rooms,
        'room_categories': room_categories,
        'total_individual_rooms': total_individual_rooms,
    }
    return render(request, 'custom_admin/dashboard.html', context)


@login_required(login_url='admin_login')
def manage_rooms(request):
    rooms = Rooms.objects.all()
    return render(request, 'custom_admin/rooms/list.html', {'rooms': rooms})


@login_required(login_url='admin_login')
def add_room(request):
    if request.method == 'POST':
        form = RoomTypeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room added successfully!')
            return redirect('manage_rooms')
    else:
        form = RoomTypeForm()
    
    return render(request, 'custom_admin/rooms/add.html', {'form': form})


@login_required(login_url='admin_login')
def edit_room(request, room_id):
    room = Rooms.objects.get(id=room_id)
    
    if request.method == 'POST':
        form = RoomTypeForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room updated successfully!')
            return redirect('manage_rooms')
    else:
        form = RoomTypeForm(instance=room)
    
    return render(request, 'custom_admin/rooms/edit.html', {'form': form, 'room': room})


@login_required(login_url='admin_login')
def delete_room(request, room_id):
    room = Rooms.objects.get(id=room_id)
    room.delete()
    messages.success(request, 'Room deleted successfully!')
    return redirect('manage_rooms')


@login_required(login_url='admin_login')
def manage_individual_rooms(request):
    rooms = Room.objects.select_related('room_type').all()
    return render(request, 'custom_admin/rooms/individual_list.html', {'rooms': rooms})


@login_required(login_url='admin_login')
def add_individual_room(request):
    from motel.models import Rooms as RoomTypes
    
    if request.method == 'POST':
        form = IndividualRoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Individual room added successfully!')
            return redirect('manage_individual_rooms')
    else:
        form = IndividualRoomForm()
    
    room_types = RoomTypes.objects.all()
    return render(request, 'custom_admin/rooms/add_individual.html', {
        'form': form, 
        'room_types': room_types
    })


@login_required(login_url='admin_login')
def edit_individual_room(request, room_id):
    from motel.models import Rooms as RoomTypes
    
    room = Room.objects.get(id=room_id)
    
    if request.method == 'POST':
        form = IndividualRoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room updated successfully!')
            return redirect('manage_individual_rooms')
    else:
        form = IndividualRoomForm(instance=room)
    
    room_types = RoomTypes.objects.all()
    return render(request, 'custom_admin/rooms/edit_individual.html', {
        'form': form, 
        'room': room,
        'room_types': room_types
    })


@login_required(login_url='admin_login')
def delete_individual_room(request, room_id):
    room = Room.objects.get(id=room_id)
    room.delete()
    messages.success(request, 'Room deleted successfully!')
    return redirect('manage_individual_rooms')


@login_required(login_url='admin_login')
def manage_users(request):
    users = UserAccount.objects.all().order_by('-date_joined')
    return render(request, 'custom_admin/users.html', {'users': users})


@login_required(login_url='admin_login')
def toggle_user_status(request, user_id):
    user = UserAccount.objects.get(id=user_id)
    user.is_active = not user.is_active
    user.save()
    status = 'activated' if user.is_active else 'deactivated'
    messages.success(request, f'User {status} successfully!')
    return redirect('manage_users')


@login_required(login_url='admin_login')
def delete_user(request, user_id):
    user = UserAccount.objects.get(id=user_id)
    user.delete()
    messages.success(request, 'User deleted successfully!')
    return redirect('manage_users')


@login_required(login_url='admin_login')
def manage_bookings(request):
    bookings = Bookings.objects.select_related('roomname').order_by('-id')
    return render(request, 'custom_admin/bookings.html', {'bookings': bookings})


@login_required(login_url='admin_login')
def update_booking_status(request, booking_id):
    booking = Bookings.objects.get(id=booking_id)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        booking.status = status
        booking.save()
        messages.success(request, 'Booking status updated!')
    
    return redirect('manage_bookings')


@login_required(login_url='admin_login')
def delete_booking(request, booking_id):
    booking = Bookings.objects.get(id=booking_id)
    booking.delete()
    messages.success(request, 'Booking deleted successfully!')
    return redirect('manage_bookings')


@login_required(login_url='admin_login')
def admin_profile(request):
    if request.method == 'POST':
        if 'current_password' in request.POST:
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            if not request.user.check_password(current_password):
                messages.error(request, 'Current password is incorrect!')
            elif new_password != confirm_password:
                messages.error(request, 'New passwords do not match!')
            elif len(new_password) < 8:
                messages.error(request, 'Password must be at least 8 characters!')
            else:
                request.user.set_password(new_password)
                request.user.save()
                messages.success(request, 'Password changed successfully! Please login again.')
                return redirect('admin_login')
        else:
            request.user.first_name = request.POST.get('first_name', request.user.first_name)
            request.user.last_name = request.POST.get('last_name', request.user.last_name)
            request.user.save()
            messages.success(request, 'Profile updated successfully!')
    
    return render(request, 'custom_admin/profile.html')

