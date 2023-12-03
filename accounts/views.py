from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import SingUpForm
from .models import Account


def register(request):
    if request.method == "POST":
        user_form = SingUpForm(request.POST)
        if user_form.is_valid():
            user_form.check_email()
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password1"])
            new_user.save()

            account = Account.objects.create(user=new_user)
            account.save()

            return redirect(reverse("login"))
    else:
        user_form = SingUpForm()
    return render(request, "registration/register.html", {"user_form": user_form})
