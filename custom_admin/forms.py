from django import forms
from .models import AdminUser
from motel.models import Rooms, Bookings


class AdminLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'required': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'required': True
        })
    )


class AdminRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'required': True
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password',
            'required': True
        })
    )
    
    class Meta:
        model = AdminUser
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
                'required': True
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
                'required': True
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError("Password and confirm password do not match!")
        
        return cleaned_data


class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = Rooms
        fields = ['room_name', 'room_des', 'room_price', 'room_facilities', 'room_image', 'number_of_rooms']
        widgets = {
            'room_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Room Name'
            }),
            'room_des': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Room Description',
                'rows': 4
            }),
            'room_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Price per night'
            }),
            'room_facilities': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'WiFi, TV, AC, etc.'
            }),
            'room_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'number_of_rooms': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Number of rooms',
                'min': '1'
            }),
        }


class IndividualRoomForm(forms.ModelForm):
    class Meta:
        from motel.models import Room
        model = Room
        fields = ['room_type', 'room_number', 'is_available']
        widgets = {
            'room_type': forms.Select(attrs={'class': 'form-control'}),
            'room_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Room Number'
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class BookingStatusForm(forms.ModelForm):
    class Meta:
        model = Bookings
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

