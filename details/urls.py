from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("book/", views.book, name="book"),
    path("reservations/", views.reservations, name="reservations"),
    path("menu/", views.menu, name="menu"),
    path("menu_item/<int:pk>/", views.display_menu_item, name="menu_item"),
    path("bookings/", views.bookings, name="bookings"),
    path("today_reservation/", views.today_reservation, name="today_reservation"),
    path("editbooking/<uuid:bookingId>/", views.edit_booking, name="edit_booking"),
    path("feedback/<uuid:bookingId>/", views.feedback, name="feedback"),
]
