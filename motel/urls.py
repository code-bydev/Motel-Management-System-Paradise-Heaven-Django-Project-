from django.contrib import admin
from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_signup, name='login'),
    path('bookings/', views.bookings, name='bookings'),
    path('rooms/', views.rooms, name='rooms_list'),
    path('contact/', views.contact, name='contact'),
    path('reservation/', views.reservation, name='reservation'),
    path('logout/', views.logout_view, name='logout'),
    
    path('profile/', views.user_profile, name='user_profile'),
    
    path('payment/', views.payment, name='payment'),
    path('booking-success/', views.booking_success, name='booking_success'),
    path('process-booking/', views.process_booking, name='process_booking'),
    
    path('api/room-details/', views.get_room_details, name='get_room_details'),
    
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    
    path('add-review/<int:room_id>/', views.add_review, name='add_review'),
    path('room-reviews/<int:room_id>/', views.room_reviews, name='room_reviews'),
    
    path('receipt/<int:booking_id>/', views.download_receipt, name='download_receipt'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

