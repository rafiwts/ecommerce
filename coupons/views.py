from django.contrib import messages
from django.shortcuts import redirect, render

from accounts.models import User

from .forms import CouponForm


def crete_coupon(request):
    if request.method == "POST":
        coupon_form = CouponForm(request.POST)
        if coupon_form.is_valid():
            try:
                user = User.objects.get(username=request.user)
                new_coupon = coupon_form.save(commit=False)
                new_coupon.user = user
                new_coupon.save()
                messages.success(request, "Coupon has been created successfully")
                return redirect("home")
            except User.DoesNotExist:
                messages.error(request, "User does not exist.")
                print("error")
            except Exception as e:
                messages.error(request, f"An error occured: {e}")
                print(e)
    coupon_form = CouponForm()

    return render(
        request,
        "coupon/coupon.html",
        ({"coupon_form": coupon_form}),
    )
