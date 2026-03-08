from django import forms
from motel import models
from datetime import date

class Room_form(forms.ModelForm):
    class Meta:
        model = models.Rooms
        fields = '__all__'

class CheckAvailabilityForm(forms.Form):
    check_in = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=date.today
    )
    check_out = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=date.today
    )
    adults = forms.IntegerField(min_value=1, initial=1)
    children = forms.IntegerField(min_value=0, initial=0)
    rooms = forms.IntegerField(min_value=1, initial=1)

