from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import (
    AccountForm,
    ChangePasswordForm,
    LoginForm,
    SingUpForm,
    UserAddressForm,
)
from .models import User


def login_view(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cleaned_data = login_form.cleaned_data
            user = authenticate(
                username=cleaned_data["username"], password=cleaned_data["password"]
            )
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse("home"))
                else:
                    return HttpResponse("The account is blocked")
            else:
                return HttpResponse("Invalid credentials")
    else:
        login_form = LoginForm()

    return render(request, "account/login.html", {"login_form": login_form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("home")


def register(request):
    if request.method == "POST":
        user_form = SingUpForm(request.POST)
        if user_form.is_valid():
            cleaned_data = user_form.cleaned_data
            new_user = user_form.save(commit=False)
            new_user.set_password(cleaned_data["password1"])
            new_user.save()

            user = authenticate(
                username=cleaned_data["username"], password=cleaned_data["password1"]
            )
            login(request, user)

            return redirect(reverse("account:create-profile"))
    else:
        user_form = SingUpForm()

    return render(request, "account/register.html", {"user_form": user_form})


@login_required
def profile_view(request, username):
    user = User.objects.select_related("account").get(username=username)

    return render(request, "account/profile-view.html", {"user": user})


@login_required
def create_profile(request):
    if request.method == "POST":
        profile_form = AccountForm(
            data=request.POST, instance=request.user.account, files=request.FILES
        )
        if profile_form.is_valid():
            profile_form.save()
            logout(request)
            return redirect(reverse("account:login"))
        else:
            return messages.error(request, "Invaild data")
    else:
        profile_form = AccountForm(instance=request.user.account)

    return render(
        request, "account/create-profile.html", {"profile_form": profile_form}
    )


@login_required
def edit_profile(request, username):
    if request.method == "POST":
        profile_form = AccountForm(
            instance=request.user.account, data=request.POST, files=request.FILES
        )
        address_form = UserAddressForm(
            instance=request.user.account.address, data=request.POST
        )
        if profile_form.is_valid() and address_form.is_valid():
            profile_form.save()
            address_form.save()
            messages.success(request, "Data has been saved")
            return redirect("account:profile-view", username=request.user.username)
    else:
        profile_form = AccountForm(instance=request.user.account)
        address_form = UserAddressForm(instance=request.user.account.address)

    return render(
        request,
        "account/edit-profile.html",
        {"profile_form": profile_form, "address_form": address_form},
    )


@login_required
def change_password(request, username):
    if request.method == "POST":
        password_form = ChangePasswordForm(data=request.POST)
        if password_form.is_valid():
            cleaned_data = password_form.cleaned_data
            if not request.user.check_password(cleaned_data["old_password"]):
                messages.error(request, "Invalid current password.")
            elif cleaned_data["new_password"] != cleaned_data["confirm_password"]:
                messages.error(request, "Passwords do not match.")
            else:
                request.user.set_password(cleaned_data["new_password"])
                request.user.save()

                update_session_auth_hash(request, request.user)

                messages.success(request, "Password has been changed")

                return redirect("account:profile-view", username=request.user.username)
    else:
        password_form = ChangePasswordForm()

    return render(
        request, "account/change-password.html", {"password_form": password_form}
    )
