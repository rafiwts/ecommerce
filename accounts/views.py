from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from .forms import (
    AccountForm,
    ChangePasswordForm,
    LoginForm,
    ResetPasswordForm,
    SingUpForm,
    UserAddressForm,
)
from .handlers import reset_password_email_handler
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
                    messages.error(
                        request, "The account is inactive. Please contact our support!"
                    )
            else:
                messages.error(request, "Invalid credentials. Try again!")

            login_form = LoginForm()
    else:
        login_form = LoginForm()

    return render(request, "account/login.html", {"login_form": login_form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("home")


def register(request):
    if request.method == "POST":
        register_form = SingUpForm(request.POST)
        if register_form.is_valid():
            cleaned_data = register_form.cleaned_data
            new_user = register_form.save(commit=False)
            new_user.set_password(cleaned_data["password1"])
            new_user.save()

            user = authenticate(
                username=cleaned_data["username"], password=cleaned_data["password1"]
            )
            login(request, user)

            return redirect(reverse("account:create-profile"))
        else:
            # if form is invalid, return message error...
            messages.error(request, "Invalid input! Try again!")
            # ... and remove autofocus after sumbitting
            register_form.fields["username"].widget.attrs.pop("autofocus", None)
    else:
        register_form = SingUpForm()

    return render(request, "account/register.html", {"register_form": register_form})


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
def edit_account(request, username):
    user = request.user
    if request.method == "POST":
        account_form = AccountForm(
            instance=user.account, data=request.POST, files=request.FILES
        )
        if account_form.is_valid():
            account_form.save()
            messages.success(request, "Data has been saved")
            return redirect("account:profile-view", username=username)
    else:
        account_form = AccountForm(instance=user.account)
    return render(request, "account/edit-account.html", {"account_form": account_form})


@login_required
def edit_address(request, username):
    account = request.user.account
    if request.method == "POST":
        address_form = UserAddressForm(instance=account.address, data=request.POST)
        if address_form.is_valid():
            print(address_form.cleaned_data)
            address_form.save()
            messages.success(request, "Data has been saved")
            return redirect("account:profile-view", username=username)
    else:
        address_form = UserAddressForm(instance=account.address)
    return render(request, "account/edit-address.html", {"address_form": address_form})


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

                return redirect("account:profile-view", username=username)
    else:
        password_form = ChangePasswordForm()

    return render(
        request, "account/change-password.html", {"password_form": password_form}
    )


def reset_password(request):
    if request.method == "POST":
        password_form = ResetPasswordForm(request.POST)
        if password_form.is_valid():
            email = password_form.cleaned_data["email"]
            user = User.objects.filter(email=email).first()

            if user:
                reset_password_email_handler(request, user, email)
                return redirect("account:login")
            else:
                messages.error(request, "User with this email address not found")
    else:
        password_form = ResetPasswordForm()

    return render(
        request, "account/reset-password.html", {"password_form": password_form}
    )


def reset_password_confirmation(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(User, pk=uid)
    if request.method == "POST":
        password_form = ChangePasswordForm(data=request.POST)
        if password_form.is_valid():
            cleaned_data = password_form.cleaned_data
            new_password1 = cleaned_data["new_password"]
            new_password2 = cleaned_data["confirm_password"]
            if new_password1 != new_password2:
                messages.error(request, "Passwords do not match.")
            else:
                user.set_password(new_password1)
                user.save()

                messages.success(
                    request,
                    "Password has been changed. You can "
                    "log in again using a new password",
                )

                return redirect("account:login")
    else:
        password_form = ChangePasswordForm()

    return render(
        request,
        "account/reset-password-confirmation.html",
        ({"password_form": password_form, "token": token, "uidb64": uidb64}),
    )
