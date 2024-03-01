from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView

from .forms import (
    ChangePasswordForm,
    CreateProfileForm,
    EditAccoutForm,
    ImageForm,
    LoginForm,
    ResetPasswordForm,
    SingUpForm,
    UserAddressForm,
    UserShippingAddressForm,
)
from .handlers import reset_password_email_handler, upload_image_handler
from .models import ResetPasswordLink, User, UserShippingAddress


def handle_login(request, login_form):
    cleaned_data = login_form.cleaned_data
    authenticated_user = authenticate(
        username=cleaned_data["username"], password=cleaned_data["password"]
    )
    if authenticated_user and authenticated_user.is_active:
        login(request, authenticated_user)
        return True
    elif authenticated_user and not authenticated_user.is_active:
        messages.error(request, "The account is inactive. Please contact our support!")
        return False
    else:
        messages.warning(request, "Invalid credentials. Try again!")
        return False


def handle_reset_password(request, password_form):
    email = password_form.cleaned_data["email"]
    user = User.objects.filter(email=email).first()

    if user:
        created_link = reset_password_email_handler(request, user, email)

        if created_link:
            # if link has been created
            link = ResetPasswordLink(link=created_link, user=user)
            link.save()

        return redirect("account:login")
    else:
        messages.error(request, "User with his email address not found!")


def login_view(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        password_form = ResetPasswordForm(request.POST)
        if login_form.is_valid():
            user_is_authenticated = handle_login(request, login_form)
            if user_is_authenticated:
                return redirect("home")

        elif password_form.is_valid():
            handle_reset_password(request, password_form)

    login_form = LoginForm()
    password_form = ResetPasswordForm()

    return render(
        request,
        "account/login.html",
        {"login_form": login_form, "password_form": password_form},
    )


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
        profile_form = CreateProfileForm(
            data=request.POST, instance=request.user.account, files=request.FILES
        )
        if profile_form.is_valid():
            profile_form.save()
            logout(request)
            messages.info(request, "The user has been created! You can login in now!")
            return redirect(reverse("account:login"))
        else:
            messages.error(request, "Invaild data")
    else:
        profile_form = CreateProfileForm(instance=request.user.account)

    return render(
        request, "account/create-profile.html", {"profile_form": profile_form}
    )


def reset_password_confirmation(request, uidb64, token):
    reset_url = request.build_absolute_uri(
        reverse(
            "account:reset-password-confirmation",
            kwargs={"uidb64": uidb64, "token": token},
        )
    )
    existing_link = ResetPasswordLink.objects.get(link=reset_url)

    if existing_link.has_expired():
        return HttpResponse("Link does not exist anymore", status=404)

    uid = force_str(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(User, pk=uid)
    # TODO: add validation
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

                messages.info(request, "Password has been changed.")
                existing_link.expired = True
                existing_link.save()

                return redirect("account:login")
    else:
        password_form = ChangePasswordForm()

    return render(
        request,
        "account/reset-password-confirmation.html",
        ({"password_form": password_form, "token": token, "uidb64": uidb64}),
    )


class ProfileView(View):
    template_name = "account/profile-view.html"

    def get_user(self, username):
        try:
            return User.objects.prefetch_related(
                "account__address", "account__shipping_addresses"
            ).get(username=username)
        except User.DoesNotExist:
            raise Http404("User does not exist")

    def get_shipping_address_data(self, user):
        shipping_addresses = user.account.shipping_addresses.all()
        return shipping_addresses

    def get_image_form(self, user):
        return ImageForm(instance=user.account)

    def get_password_form(self):
        return ChangePasswordForm()

    def get_account_form(self, user):
        return EditAccoutForm(instance=user.account)

    def get_address_form(self, user):
        return UserAddressForm(instance=user.account.address)

    def get_shipping_address_form(self, user):
        return UserShippingAddressForm(instance=user.account)

    def get_context_data(self, **kwargs):
        username = self.request.user
        user = self.get_user(username)
        shipping_address_data = self.get_shipping_address_data(user)
        image_form = self.get_image_form(user)
        password_form = self.get_password_form()
        account_form = self.get_account_form(user)
        address_form = self.get_address_form(user)
        shipping_address_form = self.get_shipping_address_form(user)

        return {
            "user": user,
            "image_form": image_form,
            "shipping_address_data": shipping_address_data,
            "password_form": password_form,
            "account_form": account_form,
            "address_form": address_form,
            "shipping_address_form": shipping_address_form,
        }

    def get(self, request, username, *args, **kwargs):
        if request.user.username == username:
            user = self.get_user(username)
            context = self.get_context_data(user=user, **kwargs)
            return render(request, self.template_name, context)
        else:
            raise Http404("Something went wrong!")


class ChangeProfileImage(ProfileView, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        self.image_form = ImageForm(
            request.POST, instance=user.account, files=request.FILES
        )

        if self.image_form.is_valid():
            self.image_form.save()
            upload_image_handler(request, user)
            return redirect("account:profile-view", username=user)
        else:
            messages.error(request, "Invalid image data")
            return self.get(request, *args, **kwargs)


class ChangePassword(ProfileView, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        self.password_form = ChangePasswordForm(data=request.POST)
        if self.password_form.is_valid():
            cleaned_data = self.password_form.cleaned_data

            if not user.check_password(cleaned_data["old_password"]):
                # FIXME: this can only be validated via server not client
                messages.error(request, "Invalid current password. Try again!")
            else:
                user.set_password(cleaned_data["new_password"])
                user.save()
                update_session_auth_hash(request, user)

                messages.info(request, "Password has been changed")

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
        self.account_form = EditAccoutForm(instance=user.account, data=request.POST)
        if self.account_form.is_valid():
            self.account_form.save()
            messages.success(request, "Data has been saved")
            return redirect("account:profile-view", username=user)
        else:
            return super().get(request, *args, **kwargs)


class EditAddress(ProfileView, View):
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


class BaseShippingAddressView(ProfileView):
    model = UserShippingAddress
    form_class = UserShippingAddressForm
    error_info = "Something went wrong! The shipping address could not be saved"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shipping_address_form"] = self.form
        return context

    def form_invalid(self, form, *args, **kwargs):
        self.form = form
        messages.info(self.request, self.error_info)
        return super().get(self.request, *args, **kwargs)

    def get_success_url(self):
        return reverse("account:profile-view", args=[self.request.user.username])


class ShippingAddressCreateView(BaseShippingAddressView, CreateView):
    success_info = "The shipping address has been added"

    def form_valid(self, form):
        self.form = form
        current_user = self.get_user(self.request.user)
        shipping_address = form.save(commit=False)
        shipping_address.save()
        current_user.account.shipping_addresses.add(shipping_address)
        messages.info(self.request, self.success_info)
        return super().form_valid(form)


class ShippingAddressUpdateView(BaseShippingAddressView, UpdateView):
    success_info = "The shipping address has been updated"

    def get_object(self, queryset=None):
        address_id = self.kwargs.get("address_id")
        return get_object_or_404(UserShippingAddress, id=address_id)

    def form_valid(self, form):
        self.form = form
        form.save()
        messages.info(self.request, self.success_info)
        return super().form_valid(form)


# FIXME: order of inheritance has been switched cause otherwise form_invalid is called
class ShippingAddressDeleteView(DeleteView, BaseShippingAddressView):
    model = UserShippingAddress
    success_info = "The shipping address has been updated"

    def get_object(self, queryset=None):
        address_id = self.kwargs.get("address_id")
        return get_object_or_404(UserShippingAddress, id=address_id)

    def form_valid(self, form):
        shipping_address = self.get_object()
        shipping_address.delete()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("account:profile-view", args=[self.request.user.username])
