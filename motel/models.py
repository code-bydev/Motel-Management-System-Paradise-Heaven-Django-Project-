from django.db import models
from datetime import date
from django.utils import timezone

class Rooms(models.Model):
    room_name = models.CharField(max_length=255)
    room_des = models.TextField()
    room_price = models.IntegerField()
    room_facilities = models.TextField(default="WiFi,TV,AC")
    room_image = models.ImageField(upload_to='rooms/', blank=True, null=True)
    number_of_rooms = models.IntegerField(default=1, help_text="Number of rooms available in this category")


    def __str__(self):
        return self.room_name
    
class Room(models.Model):
    room_type = models.ForeignKey(Rooms,on_delete=models.CASCADE)
    room_number = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.room_type


class UserAccount(models.Model):
    username = models.CharField(max_length=255,default='')
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, default='')
    address = models.TextField(blank=True, default='')
    city = models.CharField(max_length=100, blank=True, default='')
    state = models.CharField(max_length=100, blank=True, default='')
    postal_code = models.CharField(max_length=20, blank=True, default='')
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.name

class Bookings(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHODS = [
        ('card', 'Credit/Debit Card'),
        ('upi', 'UPI'),
        ('netbanking', 'Net Banking'),
        ('wallet', 'Digital Wallet'),
    ]
    
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal = models.IntegerField()
    phone = models.IntegerField(default='0')
    email = models.EmailField()
    roomname = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    check_in = models.DateField(null=True, blank=True)
    check_out = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, blank=True, default='')
    transaction_id = models.CharField(max_length=100, blank=True, default='')
    total_amount = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Booking #{self.id} - {self.firstName} {self.lastName}"


class RoomReview(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    booking = models.ForeignKey(Bookings, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], help_text="1-5 stars")
    review_text = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review for {self.room.room_name} by {self.user.name}"

