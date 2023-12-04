from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import EditAccountForm, LoginForm, SingUpForm


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


def register(request):
    if request.method == "POST":
        user_form = SingUpForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password1"])
            new_user.save()
            login(request, new_user)

            return redirect(reverse("account:edit-profile"))
    else:
        user_form = SingUpForm()

    return render(request, "account/register.html", {"user_form": user_form})


@login_required
def edit_profile(request):
    if request.method == "POST":
        account_form = EditAccountForm(
            data=request.POST, instance=request.user.account, files=request.FILES
        )
        if account_form.is_valid():
            account_form.save()
            logout(request)
            return redirect(reverse("account:login"))
        else:
            return HttpResponse("Invalid data")
    else:
        account_form = EditAccountForm(instance=request.user.account)

    return render(request, "account/edit-profile.html", {"account_form": account_form})
