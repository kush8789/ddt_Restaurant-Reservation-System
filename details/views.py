from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookingForm, FeedbackForm
from .models import Menu, Feedback, FeedImage, Category
from django.core import serializers
from .models import Booking
from datetime import datetime
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request, "index.html")


def about(request):
    # feedbacks = Feedback.objects.all()
    feedback_list = Feedback.objects.all()  # Fetch all feedbacks from the database

    paginator = Paginator(feedback_list, per_page=6)  # Show 6 feedbacks per page
    page_number = request.GET.get("page")
    feedbacks = paginator.get_page(page_number)
    total_ratings = sum(feedback.rating for feedback in feedback_list)
    if feedback_list:
        average_rating = total_ratings / len(feedback_list)
    else:
        average_rating = 0
    context = {"feedbacks": feedbacks, "average_rating": average_rating}

    return render(request, "about.html", context)


def menu(request):
    menu_items = Menu.objects.all()
    categories = Category.objects.all()

    # Apply filtering based on user selections
    selected_category = request.GET.get("category")
    sort_by_price = request.GET.get("sort_by_price")
    special = request.GET.get("special")
    recommended = request.GET.get("recommended")
    available = request.GET.get("available")

    if selected_category:
        menu_items = menu_items.filter(category__name=selected_category)
    if sort_by_price == "asc":
        menu_items = menu_items.order_by("price")
    elif sort_by_price == "desc":
        menu_items = menu_items.order_by("-price")
    if special:
        menu_items = menu_items.filter(is_special=True)
    if recommended:
        menu_items = menu_items.filter(is_recommended=True)
    if available:
        menu_items = menu_items.filter(is_available=True)

    context = {
        "menu": menu_items,
        "categories": categories,
    }
    return render(request, "menu.html", context)


def display_menu_item(request, pk=None):
    menu_item = get_object_or_404(Menu, pk=pk)
    menu_images = menu_item.menuimage_set.all()

    context = {
        "menu_item": menu_item,
        "menu_images": menu_images,
    }

    return render(request, "menu_item.html", context)


@login_required
def bookings(request):
    return render(request, "bookings.html")


@login_required
def book(request):
    form = BookingForm()
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user

            # Check if the reservation date is not in the past
            current_date = datetime.today().date()
            reservation_date = booking.reservation_date
            if reservation_date < current_date:
                messages.error(
                    request,
                    "Sorry, you can't do time travel!!",
                    extra_tags="alert alert-warning alert-dismissible fade show",
                )
                return redirect("book")  # Redirect back to booking page

            booking.status = "confirmed"
            booking.save()
            messages.error(
                request,
                "Welcome to Restaurant. Your table has been booked.",
                extra_tags="alert alert-success alert-dismissible fade show",
            )
            return redirect("bookings")
    return render(request, "book.html", {"form": form})


@login_required
def reservations(request):
    date = datetime.today().date()
    user = request.user

    upcoming_bookings = Booking.objects.filter(
        user=user, reservation_date__gte=date
    ).order_by("reservation_date")[:5]
    previous_bookings = Booking.objects.filter(
        user=user, reservation_date__lt=date
    ).order_by("-reservation_date")[:5]

    upcoming_bookings_json = list(upcoming_bookings.values())
    previous_bookings_json = list(previous_bookings.values())

    return JsonResponse(
        {
            "upcoming_bookings": upcoming_bookings_json,
            "previous_bookings": previous_bookings_json,
            "date": date.isoformat(),
        }
    )


@login_required
def today_reservation(request):
    # Handle GET request
    date = request.GET.get("date")
    # user = request.user
    if date:
        bookings = Booking.objects.filter(user=request.user, reservation_date=date)
        booking_json = serializers.serialize("json", bookings)
        return HttpResponse(booking_json, content_type="application/json")
    else:
        return JsonResponse({"message": "No data found"}, status=200)


@login_required
def edit_booking(request, bookingId):
    try:
        booking = Booking.objects.get(bookingId=bookingId, user=request.user)

        if booking.reservation_date < datetime.today().date():
            messages.error(
                request,
                "You can only edit upcoming bookings.",
                extra_tags="alert alert-danger alert-dismissible fade show",
            )
            return redirect("bookings")

        if booking.status != "pending":
            messages.error(
                request,
                "You can only edit bookings with a status of 'pending'.",
                extra_tags="alert alert-danger alert-dismissible fade show",
            )
            return redirect("bookings")

    except Booking.DoesNotExist:
        messages.error(
            request,
            "Booking not found or not editable, please try again.",
            extra_tags="alert alert-danger alert-dismissible fade show",
        )
        return redirect("bookings")

    if request.method == "POST":
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Booking has been successfully updated.",
                extra_tags="alert alert-success alert-dismissible fade show",
            )
            return redirect("bookings")
    else:
        form = BookingForm(instance=booking)

    return render(request, "editbooking.html", {"form": form})


@login_required
def feedback(request, bookingId):
    try:
        booking = get_object_or_404(Booking, user=request.user, bookingId=bookingId)
        print(booking)
        if booking == None:
            return redirect("home")

        # Check if the booking status is "checkedout"
        if booking.status != "checkedout":
            messages.error(
                request,
                "You can only give feedback for checked-out bookings.",
                extra_tags="alert alert-danger alert-dismissible fade show",
            )
            return redirect("bookings")  # Redirect to the homepage or appropriate page

        prevFeed = Feedback.objects.filter(user=request.user, bookingId=booking).first()

        if prevFeed is not None:
            messages.error(
                request,
                "Sorry, You can't give feedback multiple times for the same booking!!",
                extra_tags="alert alert-danger alert-dismissible fade show",
            )
            return redirect("bookings")

    except Booking.DoesNotExist:
        messages.error(
            request,
            "Invalid booking ID or booking not found.",
            extra_tags="alert alert-danger alert-dismissible fade show",
        )
        return redirect("bookings")  # Redirect to the homepage or appropriate page

    if request.method == "POST":
        # message = request.POST.get("message")
        rating = int(request.POST.get("rating"))

        feedback_form = FeedbackForm(request.POST)

        if feedback_form.is_valid():
            # Convert the string value to an integer

            # Create the feedback instance with converted rating
            feedback_instance = feedback_form.save(commit=False)
            feedback_instance.user = request.user
            feedback_instance.bookingId = booking
            feedback_instance.rating = rating
            feedback_instance.save()

            # Handle the feed image upload
            images = request.FILES.getlist("images")
            for image in images:
                FeedImage.objects.create(feedback=feedback_instance, images=image)

            messages.success(
                request,
                "Feedback submitted successfully.",
                extra_tags="alert alert-success alert-dismissible fade show",
            )
            return redirect("home")  # Redirect to the homepage or appropriate page
    else:
        feedback_form = FeedbackForm(
            initial={
                "bookingId": booking.bookingId,
                "checkout": booking.reservation_date,
            },
        )
    # return redirect("bookings")
    return render(
        request,
        "feedbackForm.html",
        {
            "feedbackform": feedback_form,
            "booking": booking,
        },
    )