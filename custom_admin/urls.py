from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('register/', views.admin_register, name='admin_register'),
    path('logout/', views.admin_logout, name='admin_logout'),
    
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    path('rooms/', views.manage_rooms, name='manage_rooms'),
    path('rooms/add/', views.add_room, name='add_room'),
    path('rooms/edit/<int:room_id>/', views.edit_room, name='edit_room'),
    path('rooms/delete/<int:room_id>/', views.delete_room, name='delete_room'),
    
    path('rooms/individual/', views.manage_individual_rooms, name='manage_individual_rooms'),
    path('rooms/individual/add/', views.add_individual_room, name='add_individual_room'),
    path('rooms/individual/edit/<int:room_id>/', views.edit_individual_room, name='edit_individual_room'),
    path('rooms/individual/delete/<int:room_id>/', views.delete_individual_room, name='delete_individual_room'),
    
    path('users/', views.manage_users, name='manage_users'),
    path('users/toggle/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    
    path('bookings/', views.manage_bookings, name='manage_bookings'),
    path('bookings/update/<int:booking_id>/', views.update_booking_status, name='update_booking_status'),
    path('bookings/delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    
    path('profile/', views.admin_profile, name='admin_profile'),
]

