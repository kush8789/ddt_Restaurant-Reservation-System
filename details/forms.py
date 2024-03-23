from django import forms
from .models import Booking, Feedback, FeedImage, MenuImage
from datetime import datetime


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "reservation_date",
            "reservation_time",
            "party_size",
            "special_requests",
        ]
        # exclude = ("user",)

        # Optional: You can customize the field labels, widgets, and other attributes here.
        labels = {
            "reservation_date": "Reservation Date",
            "reservation_time": "Reservation Time",
            "party_size": "Party Size",
        }

        widgets = {
            "first_name": forms.TextInput(
                attrs={"type": "text", "class": "form-control"}
            ),
            "last_name": forms.TextInput(
                attrs={"type": "text", "class": "form-control"}
            ),
            "email": forms.EmailInput(attrs={"type": "email", "class": "form-control"}),
            "phone_number": forms.NumberInput(
                attrs={"type": "number", "class": "form-control"}
            ),
            "reservation_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                    "id": "reservation_date",
                }
            ),
            "reservation_time": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control",
                }
            ),
            "party_size": forms.NumberInput(
                attrs={
                    "type": "number",
                    "class": "form-control",
                    "max": "20",
                    "min": "1",
                }
            ),
            "special_requests": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control",
                }
            ),
        }

    input_formats = {
        "reservation_date": ["%Y-%m-%d"],
        "reservation_time": ["%I:%M %p", "%H:%M"],
    }

    def clean_reservation_date(self):
        reservation_date = self.cleaned_data.get("reservation_date")
        if reservation_date < datetime.today().date():
            raise forms.ValidationError("Reservation date cannot be in the past.")
        return reservation_date

    def clean_reservation_time(self):
        reservation_time = self.cleaned_data.get("reservation_time")
        if reservation_time < datetime.now().time():
            raise forms.ValidationError("Reservation time cannot be in the past.")
        return reservation_time


class FeedbackForm(forms.ModelForm):
    RATING_CHOICES = [
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
        initial="5",
    )

    class Meta:
        model = Feedback
        fields = ["rating", "message"]

        widgets = {
            "message": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control",
                    "placeholder": "Your feedback...",
                },
            ),
        }

class FeedImageForm(forms.ModelForm):
    class Meta:
        model = FeedImage
        fields = ["images"]


class MenuImageForm(forms.ModelForm):
    class Meta:
        model = MenuImage
        fields = ["images"]
