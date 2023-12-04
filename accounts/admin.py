from django.contrib import admin

from .models import Account, AccountType, User, UserAddress


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


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_full_name",
        "get_full_address",
        "date_of_birth",
        "image",
        "created_at",
        "user_id",
        "account_type_id",
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
        try:
            address = UserAddress.objects.get(account=obj.id)
        except UserAddress.DoesNotExist:
            return None

        return (
            f"{address.street}, "
            f"{address.zip_code}, "
            f"{address.city}, "
            f"{address.country}"
        )

    get_full_address.short_description = "Adress"

    def get_account_name(self, obj):
        return obj.account_type.name if obj.account_type else None

    get_account_name.short_description = "Account type"


@admin.register(AccountType)
class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "discount_value")
    ordering = ["discount_value"]


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ("street", "zip_code", "city", "state", "country", "account_id")
    list_filter = ["country", "city"]
    search_fields = ["country", "city", "street"]
    ordering = ["country", "city", "street", "zip_code"]
