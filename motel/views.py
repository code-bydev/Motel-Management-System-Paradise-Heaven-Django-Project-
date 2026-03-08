from django.shortcuts import render,redirect
from django.http import JsonResponse
from motel import forms
from motel.models import Rooms, Room, Bookings
from django.contrib import messages
from .models import UserAccount
from .forms import CheckAvailabilityForm
from django.contrib.auth import get_user_model
from django.db.models import Q
from datetime import datetime

def index(request):
    form = CheckAvailabilityForm()
    if request.method == 'POST':
        form = CheckAvailabilityForm(request.POST)
        if form.is_valid():
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']  
            adults = form.cleaned_data['adults']
            children = form.cleaned_data['children']
            rooms_needed = form.cleaned_data['rooms']
            
            from datetime import date
            if check_in < date.today():
                messages.error(request, 'Check-in date cannot be in the past. Please select a valid date.')
                return render(request, 'index.html', {'form': form})
            
            if check_out <= check_in:
                messages.error(request, 'Check-out date must be after check-in date.')
                return render(request, 'index.html', {'form': form})
            
            # Get all bookings that overlap with the requested dates
            overlapping_bookings = Bookings.objects.filter(
                Q(check_in__lt=check_out) & Q(check_out__gt=check_in),
                status__in=['confirmed', 'checked_in']
            )
            
            # Count how many rooms are booked for each room category
            booked_counts = {}
            for booking in overlapping_bookings:
                room_id = booking.roomname_id
                if room_id in booked_counts:
                    booked_counts[room_id] += 1
                else:
                    booked_counts[room_id] = 1
            
            # Filter rooms that have availability
            available_rooms = []
            for room in Rooms.objects.all():
                booked = booked_counts.get(room.id, 0)
                available = room.number_of_rooms - booked
                if available >= rooms_needed:
                    available_rooms.append(room)
            
            if available_rooms:
                messages.success(request, f'Found {len(available_rooms)} available rooms!')
                return render(request, 'available_rooms.html', {
                    'available_rooms': available_rooms,
                    'check_in': check_in,
                    'check_out': check_out,
                    'adults': adults,
                    'children': children,
                    'rooms_needed': rooms_needed
                })
            else:
                messages.error(request, 'No rooms available for the selected dates. Please try different dates.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    
    return render(request,'index.html', {'form': form})

def contact(request):
    return render(request,'contact.html')

def rooms(request):
    roomsdata = Rooms.objects.all()[:6]
    for room in roomsdata:
        reviews = room.reviews.filter(is_approved=True)
        if reviews.exists():
            room.avg_rating = sum(r.rating for r in reviews) / reviews.count()
            room.review_count = reviews.count()
        else:
            room.avg_rating = 0
            room.review_count = 0
    
    data = {
        'roomsdata' : roomsdata 
    }
    return render(request,'rooms_list.html',data)

def bookings(request):
    roomsdata = Rooms.objects.all()
    
    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal = request.POST.get('postal')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        roomname_id = request.POST.get('roomname')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        
        try:
            room = Rooms.objects.get(id=roomname_id)
        except Rooms.DoesNotExist:
            messages.error(request, 'Selected room not found.')
            return render(request, 'booking.html', {'Rooms': room})
        
        from datetime import datetime
        try:
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            messages.error(request, 'Invalid date format. Please select valid dates.')
            return render(request, 'booking.html', {'Rooms': room})
        
        from datetime import date
        if check_in_date < date.today():
            messages.error(request, 'Check-in date cannot be in the past.')
            return render(request, 'booking.html', {'Rooms': room})
        
        if check_out_date <= check_in_date:
            messages.error(request, 'Check-out date must be after check-in date.')
            return render(request, 'booking.html', {'Rooms': room})
        
        booking = Bookings.objects.create(
            firstName=firstName,
            lastName=lastName,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            postal=postal,
            phone=phone,
            email=email,
            roomname=room,
            check_in=check_in_date,
            check_out=check_out_date,
            status='confirmed'
        )
        
        messages.success(request, f'Booking confirmed! Your booking ID is #{booking.id}')
        return redirect('index')
    
    room = roomsdata.first() if roomsdata else None
    return render(request, 'booking.html', {'Rooms': room, 'roomsdata': roomsdata})

def login_signup(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        if 'insert' in request.POST:
            name = request.POST.get('name')

            if UserAccount.objects.filter(email=email).exists():
                messages.error(request, "Email already registered.")
            else:
                user = UserAccount.objects.create(name=name, email=email, password=password)
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                messages.success(request, "Account created successfully.")
                return redirect('index')

        elif 'login' in request.POST:
            try:
                user = UserAccount.objects.get(email=email)
                if user.password == password:
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('index')
                else:
                    messages.error(request, "Invalid password.")
            except UserAccount.DoesNotExist:
                messages.error(request, "Email not found.")

        return redirect('login')

    return render(request, 'login.html')

def reservation(request):
    roomsdata = Rooms.objects.all()
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal = request.POST.get('zip')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        room_name = request.POST.get('room')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        
        try:
            room = Rooms.objects.get(room_name=room_name)
        except Rooms.DoesNotExist:
            messages.error(request, 'Selected room not found.')
            return render(request, 'reservation.html', {'roomsdata': roomsdata})
        
        from datetime import datetime
        try:
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            messages.error(request, 'Invalid date format. Please select valid dates.')
            return render(request, 'reservation.html', {'roomsdata': roomsdata})
        
        from datetime import date
        if check_in_date < date.today():
            messages.error(request, 'Check-in date cannot be in the past.')
            return render(request, 'reservation.html', {'roomsdata': roomsdata})
        
        if check_out_date <= check_in_date:
            messages.error(request, 'Check-out date must be after check-in date.')
            return render(request, 'reservation.html', {'roomsdata': roomsdata})
        
        booking = Bookings.objects.create(
            firstName=first_name,
            lastName=last_name,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            postal=postal,
            phone=phone,
            email=email,
            roomname=room,
            check_in=check_in_date,
            check_out=check_out_date,
            status='confirmed'
        )
        
        messages.success(request, f'Booking confirmed! Your booking ID is #{booking.id}')
        return redirect('index')
    
    return render(request, 'reservation.html', {'roomsdata': roomsdata})

def admin_users_view(request):
    users = UserAccount.objects.all()
    return render(request, 'admin-user.html', {'users': users})

def deactivate_user(request, user_id):
    user = get_user_model(UserAccount, id=user_id)
    user.is_active = False
    user.save()
    messages.success(request, f"{user.email} has been deactivated.")
    return redirect('admin_users')

def logout_view(request):
    request.session.pop('user_id', None)
    request.session.pop('user_name', None)    
    return redirect('login')


def user_profile(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        messages.error(request, 'Please login to view your profile.')
        return redirect('login')
    
    try:
        user = UserAccount.objects.get(id=user_id)
    except UserAccount.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('login')
    
    user_bookings = Bookings.objects.filter(email=user.email).order_by('-created_at')
    
    if request.method == 'POST':
        if request.FILES.get('profile_image'):
            profile_image = request.FILES['profile_image']
            if profile_image.size > 5 * 1024 * 1024:
                messages.error(request, 'Image size must be less than 5MB.')
                return render(request, 'profile.html', {'user': user, 'bookings': user_bookings})
            user.profile_image = profile_image
            messages.success(request, 'Profile picture updated!')
        
        user.name = request.POST.get('name', user.name)
        user.phone = request.POST.get('phone', user.phone)
        user.address = request.POST.get('address', user.address)
        user.city = request.POST.get('city', user.city)
        user.state = request.POST.get('state', user.state)
        user.postal_code = request.POST.get('postal_code', user.postal_code)
        
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if current_password and new_password:
            if user.password != current_password:
                messages.error(request, 'Current password is incorrect.')
                return render(request, 'profile.html', {'user': user, 'bookings': user_bookings})
            elif new_password != confirm_password:
                messages.error(request, 'New passwords do not match.')
                return render(request, 'profile.html', {'user': user, 'bookings': user_bookings})
            elif len(new_password) < 4:
                messages.error(request, 'Password must be at least 4 characters.')
                return render(request, 'profile.html', {'user': user, 'bookings': user_bookings})
            else:
                user.password = new_password
                messages.success(request, 'Password changed successfully!')
        
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('user_profile')
    
    return render(request, 'profile.html', {'user': user, 'bookings': user_bookings})


def payment(request):
    if request.method == 'POST':
        booking_data = request.session.get('booking_data')
        
        if not booking_data:
            messages.error(request, 'No booking data found. Please try again.')
            return redirect('bookings')
        
        payment_method = request.POST.get('payment_method', 'card')
        
        try:
            room = Rooms.objects.get(id=booking_data['room_id'])
            
            from datetime import datetime
            check_in_date = datetime.strptime(booking_data['check_in'], '%Y-%m-%d').date()
            check_out_date = datetime.strptime(booking_data['check_out'], '%Y-%m-%d').date()
            
            nights = (check_out_date - check_in_date).days
            if nights < 1:
                nights = 1
            base_price = room.room_price * nights
            gst = int(base_price * 0.18)
            total_amount = base_price + gst
            
            transaction_id = f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}{room.id}"
            
            booking = Bookings.objects.create(
                firstName=booking_data['firstName'],
                lastName=booking_data['lastName'],
                address1=booking_data['address1'],
                address2=booking_data.get('address2', ''),
                city=booking_data['city'],
                state=booking_data['state'],
                postal=booking_data['postal'],
                phone=booking_data['phone'],
                email=booking_data['email'],
                roomname=room,
                check_in=check_in_date,
                check_out=check_out_date,
                status='confirmed',
                payment_method=payment_method,
                transaction_id=transaction_id,
                total_amount=total_amount
            )
            
            request.session.pop('booking_data', None)
            
            request.session['last_booking_id'] = booking.id
            
            messages.success(request, f'Payment successful! Your booking ID is #{booking.id}')
            return redirect('booking_success')
            
        except Rooms.DoesNotExist:
            messages.error(request, 'Room not found.')
            return redirect('bookings')
        except Exception as e:
            messages.error(request, f'Error processing payment: {str(e)}')
            return redirect('bookings')
    
    booking_data = request.session.get('booking_data')
    
    if not booking_data:
        messages.error(request, 'No booking data found.')
        return redirect('bookings')
    
    try:
        from datetime import datetime
        check_in = datetime.strptime(booking_data['check_in'], '%Y-%m-%d').date()
        check_out = datetime.strptime(booking_data['check_out'], '%Y-%m-%d').date()
        nights = (check_out - check_in).days
        if nights < 1:
            nights = 1
        
        room = Rooms.objects.get(id=booking_data['room_id'])
        base_price = room.room_price * nights
        gst = int(base_price * 0.18)
        total_amount = base_price + gst
        
        return render(request, 'payment.html', {
            'booking_data': booking_data,
            'room': room,
            'nights': nights,
            'base_price': base_price,
            'gst': gst,
            'total_amount': total_amount
        })
    except Rooms.DoesNotExist:
        messages.error(request, 'Room not found.')
        return redirect('bookings')


def get_room_details(request):
    room_id = request.GET.get('room_id')
    
    if not room_id:
        return JsonResponse({'error': 'Room ID is required'}, status=400)
    
    try:
        room = Rooms.objects.get(id=room_id)
        
        room_image_url = ''
        if room.room_image:
            room_image_url = room.room_image.url
        
        facilities = []
        if room.room_facilities:
            facilities = [f.strip() for f in room.room_facilities.split(',')]
        
        reviews = room.reviews.filter(is_approved=True)
        if reviews.exists():
            avg_rating = sum(r.rating for r in reviews) / reviews.count()
            review_count = reviews.count()
        else:
            avg_rating = 0
            review_count = 0
        
        return JsonResponse({
            'success': True,
            'room': {
                'id': room.id,
                'room_name': room.room_name,
                'room_des': room.room_des,
                'room_price': room.room_price,
                'room_facilities': facilities,
                'room_image': room_image_url,
                'number_of_rooms': room.number_of_rooms,
                'avg_rating': round(avg_rating, 1),
                'review_count': review_count
            }
        })
    except Rooms.DoesNotExist:
        return JsonResponse({'error': 'Room not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def process_booking(request):
    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal = request.POST.get('postal')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        roomname_id = request.POST.get('roomname')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        
        if not all([firstName, lastName, address1, city, state, postal, phone, email, roomname_id, check_in, check_out]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('bookings')
        
        try:
            room = Rooms.objects.get(id=roomname_id)
        except Rooms.DoesNotExist:
            messages.error(request, 'Selected room not found.')
            return redirect('bookings')
        
        from datetime import datetime
        try:
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            messages.error(request, 'Invalid date format.')
            return redirect('bookings')
        
        from datetime import date
        if check_in_date < date.today():
            messages.error(request, 'Check-in date cannot be in the past.')
            return redirect('bookings')
        
        if check_out_date <= check_in_date:
            messages.error(request, 'Check-out date must be after check-in date.')
            return redirect('bookings')
        
        nights = (check_out_date - check_in_date).days
        if nights < 1:
            nights = 1
        base_price = room.room_price * nights
        gst = int(base_price * 0.18)
        total_amount = base_price + gst
        
        transaction_id = f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}{room.id}"
        
        booking = Bookings.objects.create(
            firstName=firstName,
            lastName=lastName,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            postal=postal,
            phone=phone,
            email=email,
            roomname=room,
            check_in=check_in_date,
            check_out=check_out_date,
            status='confirmed',
            payment_method='cash',
            transaction_id=transaction_id,
            total_amount=total_amount
        )
        
        request.session['last_booking_id'] = booking.id
        
        messages.success(request, f'Booking confirmed! Your booking ID is #{booking.id}')
        return redirect('booking_success')
    
    return redirect('bookings')


def booking_success(request):
    booking_id = request.session.get('last_booking_id')
    
    if not booking_id:
        messages.error(request, 'No booking found.')
        return redirect('index')
    
    try:
        booking = Bookings.objects.get(id=booking_id)
    except Bookings.DoesNotExist:
        messages.error(request, 'Booking not found.')
        return redirect('index')
    
    return render(request, 'booking_success.html', {
        'booking': booking,
        'booking_id': booking_id
    })


def cancel_booking(request, booking_id):
    user_id = request.session.get('user_id')
    
    if not user_id:
        messages.error(request, 'Please login to cancel a booking.')
        return redirect('login')
    
    try:
        booking = Bookings.objects.get(id=booking_id)
        user = UserAccount.objects.get(id=user_id)
    except (Bookings.DoesNotExist, UserAccount.DoesNotExist):
        messages.error(request, 'Booking or user not found.')
        return redirect('user_profile')
    
    if booking.email != user.email:
        messages.error(request, 'You are not authorized to cancel this booking.')
        return redirect('user_profile')
    
    if booking.status in ['checked_in', 'checked_out', 'cancelled']:
        messages.error(request, f'Cannot cancel a {booking.status} booking.')
        return redirect('user_profile')
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, f'Booking #{booking.id} has been cancelled successfully.')
        return redirect('user_profile')
    
    return render(request, 'cancel_booking.html', {'booking': booking})


def add_review(request, room_id):
    from motel.models import RoomReview
    
    user_id = request.session.get('user_id')
    
    if not user_id:
        messages.error(request, 'Please login to add a review.')
        return redirect('login')
    
    try:
        user = UserAccount.objects.get(id=user_id)
        room = Rooms.objects.get(id=room_id)
    except (UserAccount.DoesNotExist, Rooms.DoesNotExist):
        messages.error(request, 'Room or user not found.')
        return redirect('index')
    
    has_booking = Bookings.objects.filter(
        roomname=room,
        email=user.email,
        status__in=['checked_in', 'checked_out']
    ).exists()
    
    if not has_booking:
        messages.error(request, 'You must have a completed stay to review this room.')
        return redirect('rooms_list')
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')
        
        if not rating:
            messages.error(request, 'Please select a rating.')
            return redirect('add_review', room_id=room_id)
        
        existing_review = RoomReview.objects.filter(room=room, user=user).first()
        
        if existing_review:
            existing_review.rating = rating
            existing_review.review_text = review_text
            existing_review.save()
            messages.success(request, 'Your review has been updated!')
        else:
            RoomReview.objects.create(
                room=room,
                user=user,
                rating=rating,
                review_text=review_text
            )
            messages.success(request, 'Your review has been submitted!')
        
        return redirect('rooms_list')
    
    return render(request, 'add_review.html', {'room': room})


def room_reviews(request, room_id):
    from motel.models import RoomReview
    
    try:
        room = Rooms.objects.get(id=room_id)
        reviews = RoomReview.objects.filter(room=room, is_approved=True)
        
        if reviews.exists():
            avg_rating = sum(r.rating for r in reviews) / reviews.count()
        else:
            avg_rating = 0
        
        return render(request, 'room_reviews.html', {
            'room': room,
            'reviews': reviews,
            'avg_rating': round(avg_rating, 1)
        })
    except Rooms.DoesNotExist:
        messages.error(request, 'Room not found.')
        return redirect('index')


def download_receipt(request, booking_id):
    user_id = request.session.get('user_id')
    
    if not user_id:
        messages.error(request, 'Please login to download receipt.')
        return redirect('login')
    
    try:
        booking = Bookings.objects.get(id=booking_id)
        user = UserAccount.objects.get(id=user_id)
    except (Bookings.DoesNotExist, UserAccount.DoesNotExist):
        messages.error(request, 'Booking or user not found.')
        return redirect('index')
    
    if booking.email != user.email:
        messages.error(request, 'You are not authorized to download this receipt.')
        return redirect('user_profile')
    
    nights = (booking.check_out - booking.check_in).days
    if nights < 1:
        nights = 1
    base_price = booking.roomname.room_price * nights
    gst = int(base_price * 0.18)
    
    return render(request, 'receipt.html', {
        'booking': booking,
        'nights': nights,
        'base_price': base_price,
        'gst': gst
    })

