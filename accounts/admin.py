from django.contrib import admin

from .models import Account, AccountType, User, UserAddress, UserShippingAddress


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_staff", "is_superuser", "is_active")
    list_filter = ["is_staff", "is_active"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "username",
                    "email",
                    "password",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ]
            },
        )
    ]
    search_fields = ["email", "id", "username"]
    ordering = ["-is_superuser", "-is_staff", "username"]
    list_select_related = ["account"]


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "client_id",
        "get_full_name",
        "date_of_birth",
        "image",
        "created_at",
        "user_id",
        "account",
    )
    ordering = ["last_name", "first_name"]
    list_select_related = ["account", "user", "address"]

    @admin.display(description="Full name")
    def get_full_name(self, obj):
        return (
            f"{obj.last_name}, {obj.first_name}"
            if obj.last_name or obj.first_name
            else None
        )

    def get_account_name(self, obj):
        return obj.account_type.name if obj.account_type else None

    get_account_name.short_description = "Account type"


@admin.register(AccountType)
class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "discount_value")
    ordering = ["discount_value"]
    list_select_related = ["account"]


class BaseAddressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "street",
        "zip_code",
        "city",
        "state",
        "country",
        "account_id",
    )
    list_filter = ["country", "city"]
    search_fields = ["country", "city", "street"]
    ordering = ["country", "city", "street", "zip_code"]
    list_select_related = ["account"]


@admin.register(UserAddress)
class UserAddressAdmin(BaseAddressAdmin):
    pass


@admin.register(UserShippingAddress)
class UserShippingAddressAdmin(BaseAddressAdmin):
    pass
