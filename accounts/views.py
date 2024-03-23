from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .forms import UserRegistrationForm, UserAuthenticationForm
from django.contrib import messages


# Create your views here.
def register_view(request):
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Registration completed successfully!!",
                extra_tags="alert alert-success alert-dismissible fade show",
            )
            return redirect("home")
        else:
            messages.error(
                request,
                "Please enter details properly!!",
                extra_tags="alert alert-danger alert-dismissible fade show",
            )
    return render(request, "registration.html", {"form": form})


def login_view(request):
    next = request.GET.get("next")
    if request.method == "POST":
        form = UserAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if next == None:
                return redirect(
                    "home"
                )  # Redirect to the home page after successful login
            return redirect(next)  # Redirect to the home page after successful login

    else:
        form = UserAuthenticationForm()
    return render(request, "login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("home") 