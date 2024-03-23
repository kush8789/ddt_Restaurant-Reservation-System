from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from datetime import date, time
import uuid
from django.core.exceptions import ValidationError

STATUS_CHOICES = (
    ("pending", "Pending"),
    ("confirmed", "Confirmed"),
    ("cancelled", "Cancelled"),
    ("checkedout", "Checkedout"),
)


class Booking(models.Model):
    # Customer Details
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    first_name = models.CharField(null=False, default="", max_length=100)
    last_name = models.CharField(null=False, default="", max_length=100)
    email = models.EmailField(default="", null=False, max_length=100)
    phone_number = models.CharField(default="", null=False, max_length=20)

    # Reservation Details
    reservation_date = models.DateField(default=date.today, null=False)
    reservation_time = models.TimeField()
    party_size = models.PositiveIntegerField(default=2)
    # Special Requests or Comments (optional)
    special_requests = models.TextField(
        blank=True, default="Thankyou for asking!!, No special request for now"
    )

    # Timestamps
    created_at = models.DateField(auto_now=True, editable=False)
    updated_at = models.TimeField(auto_now=True, editable=False)
    # Status of the Booking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    # New field: Booking ID
    bookingId = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.reservation_date} {self.reservation_time}"


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Menu(models.Model):
    category = models.ForeignKey(Category, default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    menu_item_description = models.TextField(
        max_length=1000, default="No description available"
    )
    is_available = models.BooleanField(default=True)
    is_special = models.BooleanField(default=True)
    is_recommended = models.BooleanField(default=True)

    calories = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    fat_content = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    allergens = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.name}__{self.category}"


class MenuImage(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    images = models.ImageField(
        upload_to="menu_images/",
        validators=[FileExtensionValidator(["jpg", "jpeg", "png"])],
        null=True,
        blank=True,
    )
    created_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.menu.name}--{self.menu.category}"


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bookingId = models.ForeignKey(Booking, null=False, on_delete=models.CASCADE)
    feed_date = models.DateField(auto_now=True, null=False)
    rating = models.PositiveIntegerField(default=0)
    message = models.TextField(null=False, max_length=800)

    def __str__(self) -> str:
        return f"{self.user.username}--{self.bookingId}"


class FeedImage(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
    images = models.FileField(
        upload_to="feedimage/",
        validators=[FileExtensionValidator(["jpg", "jpeg", "png"])],
        null=True,
    )
    date = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.feedback.user.username}--{self.date}"
