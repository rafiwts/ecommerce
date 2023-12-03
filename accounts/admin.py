from django.contrib import admin

from .models import Account, AccountType, User, UserAddress


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "get_account_type",
        "is_staff",
        "is_superuser",
        "is_active",
        "id",
    )
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
                    "account",
                    "groups",
                    "user_permissions",
                ]
            },
        )
    ]
    search_fields = ["email", "id", "username"]
    ordering = ["is_superuser", "is_staff", "username"]

    def get_account_type(self, obj):
        return obj.account.account_type if obj.account else None

    get_account_type.short_description = "Account Type"


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "get_full_name",
        "get_full_address",
        "get_account_name",
        "image",
        "created_at",
    )
    ordering = ["last_name", "first_name"]

    @admin.display(description="Full name")
    def get_full_name(self, obj):
        return (
            f"{obj.last_name}, {obj.first_name}"
            if obj.last_name or obj.first_name
            else None
        )

    def get_full_address(self, obj):
        if obj.address:
            address = obj.address
            return (
                f"{address.street}, "
                f"{address.zip_code}, "
                f"{address.city}, "
                f"{address.country}"
            )
        else:
            return None

    get_full_address.short_description = "Adress"

    def get_account_name(self, obj):
        return obj.account_type.name if obj.account_type else None

    get_account_name.short_description = "Account type"


@admin.register(AccountType)
class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "discount_value")
    ordering = ["name"]


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ("street", "zip_code", "city", "state", "country")
    list_filter = ["country", "city"]
    search_fields = ["country", "city", "street"]
    ordering = ["country", "city", "street", "zip_code"]
