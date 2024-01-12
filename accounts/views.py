from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View

from .forms import (
    AccountForm,
    ChangePasswordForm,
    ImageForm,
    LoginForm,
    ResetPasswordForm,
    SingUpForm,
    UserAddressForm,
    UserShippingAddressForm,
)
from .handlers import reset_password_email_handler, upload_image_handler
from .models import User, UserShippingAddress


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
            # ...and remove autofocus after sumbitting
            register_form.fields["username"].widget.attrs.pop("autofocus", None)
    else:
        register_form = SingUpForm()

    return render(request, "account/register.html", {"register_form": register_form})


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
            messages.error(request, "Invaild data")
    else:
        profile_form = AccountForm(instance=request.user.account)

    return render(
        request, "account/create-profile.html", {"profile_form": profile_form}
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


class ShippingAddressView(View):
    # TODO: improve the styles
    template_name = "account/edit-shipping-address.html"

    def get_current_user(self, username):
        return User.objects.prefetch_related("account__shipping_addresses").get(
            username=username
        )

    def get_model_or_none(self, address_id):
        try:
            shipping_address = UserShippingAddress.objects.get(id=address_id)
        except UserShippingAddress.DoesNotExist:
            shipping_address = None

        return shipping_address

    def get_shipping_address_form(self, instance=None, data=None):
        return UserShippingAddressForm(instance=instance, data=data)

    def get(self, request, *args, **kwargs):
        # address_id is None for adding address
        address_id = kwargs.get("address_id", None)

        if address_id:
            shipping_address = self.get_model_or_none(address_id)
            shipping_address_form = self.get_shipping_address_form(
                instance=shipping_address
            )
            return render(
                request,
                self.template_name,
                {
                    "shipping_address_form": shipping_address_form,
                    "shipping_address": shipping_address,
                },
            )
        else:
            shipping_address_form = self.get_shipping_address_form()
            return render(
                request,
                self.template_name,
                {"shipping_address_form": shipping_address_form},
            )

    def post(self, request, *args, **kwargs):
        # address_id is None for adding address
        address_id = kwargs.get("address_id", None)
        action = kwargs["action"]
        username = kwargs["username"]

        shipping_address = self.get_model_or_none(address_id)
        current_user = self.get_current_user(username)

        if action == "add" and not shipping_address:
            shipping_address_form = self.get_shipping_address_form(data=request.POST)
            if shipping_address_form.is_valid():
                shipping_address = shipping_address_form.save(commit=False)
                shipping_address.save()
                current_user.account.shipping_addresses.add(shipping_address)
                messages.info(request, "The shipping address has been added")
                return redirect("account:profile-view", username=username)
        elif action == "edit":
            shipping_address_form = self.get_shipping_address_form(
                instance=shipping_address, data=request.POST
            )
            if shipping_address_form.is_valid():
                shipping_address_form.save()
                messages.info(request, "The shipping address has been edited")
                return redirect("account:profile-view", username=username)
        else:
            shipping_address.delete()
            messages.info(request, "The shipping address has been deleted")
            return redirect("account:profile-view", username=username)

        return render(
            request,
            self.template_name,
            {
                "shipping_address_form": shipping_address_form,
                "shipping_address": shipping_address,
            },
        )


class ProfileView(View):
    template_name = "account/profile-view.html"

    def get_user(self, username):
        return User.objects.prefetch_related(
            "account__address", "account__shipping_addresses"
        ).get(username=username)

    def get_shipping_address(self, user):
        return user.account.shipping_addresses.all()

    def get_image_form(self, user):
        return ImageForm(instance=user.account)

    def get_password_form(self):
        return ChangePasswordForm()

    def get_account_form(self, user):
        return AccountForm(instance=user.account)

    def get_address_form(self, user):
        return UserAddressForm(instance=user.account)

    def get_context_data(self, **kwargs):
        username = kwargs["username"]
        user = self.get_user(username)
        shipping_address = self.get_shipping_address(user)
        image_form = self.get_image_form(user)
        password_form = self.get_password_form()
        account_form = self.get_account_form(user)
        address_form = self.get_address_form(user)

        return {
            "user": user,
            "image_form": image_form,
            "shipping_addresses": shipping_address,
            "password_form": password_form,
            "account_form": account_form,
            "address_form": address_form,
        }

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = request.user
        image_form = ImageForm(request.POST, instance=user.account, files=request.FILES)

        if image_form.is_valid():
            image_form.save()
            upload_image_handler(request, user)
            return redirect("account:profile-view", username=user)
        else:
            messages.error(request, "Invalid image data")
            return self.get(request, *args, **kwargs)


# FIXME: after invalid form the block disappears - it shouldn't go away
class ChangePassword(ProfileView, View):
    # once there is an error the form should be overridden to display errors
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["password_form"] = self.password_form
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        self.password_form = ChangePasswordForm(data=request.POST)
        if self.password_form.is_valid():
            cleaned_data = self.password_form.cleaned_data
            if not user.check_password(cleaned_data["old_password"]):
                messages.error(request, "Invalid current password.")
            elif cleaned_data["new_password"] != cleaned_data["confirm_password"]:
                messages.error(request, "Passwords do not match.")
            else:
                user.set_password(cleaned_data["new_password"])
                request.save()

                update_session_auth_hash(request, user)

                messages.success(request, "Password has been changed")

            return redirect("account:profile-view", username=user)
        else:
            return super().get(request, *args, **kwargs)


class EditAccount(ProfileView, View):
    # once there is an error the form should be overridden to display errors
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["account_form"] = self.account_form
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        self.account_form = AccountForm(instance=user.account, data=request.POST)
        if self.account_form.is_valid():
            self.account_form.save()
            messages.success(request, "Data has been saved")
            return redirect("account:profile-view", username=user)
        else:
            return super().get(request, *args, **kwargs)


class EditAddress(ProfileView, View):
    # once there is an error the form should be overridden to display errors
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["address_form"] = self.address_form
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        self.address_form = UserAddressForm(
            instance=user.account.address, data=request.POST
        )
        if self.address_form.is_valid():
            self.address_form.save()
            messages.success(request, "Data has been saved")
            return redirect("account:profile-view", username=user)
        else:
            return super().get(request, *args, **kwargs)
