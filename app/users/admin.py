from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import forms as auth_forms
from allauth.account.models import EmailAddress
from .models import User, BillingAddress


class UserChangeForm(auth_forms.UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"


class UserCreationForm(auth_forms.UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class EmailsInline(admin.TabularInline):
    model = EmailAddress
    readonly_fields = ["user"]
    max_num = 8
    extra = 0


admin.site.unregister(EmailAddress)


class BillingAddressInline(admin.TabularInline):
    model = BillingAddress
    readonly_fields = ["country", "street_address", "apartment_address", "zip"]
    max_num = 1
    extra = 0


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "gender")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    list_display = ("get_full_name", "email", "is_staff")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("email",)
    list_display_links = ("get_full_name", "email")
    inlines = [EmailsInline, BillingAddressInline]


class BillingAddressAdmin(admin.ModelAdmin):
    readonly_fields = ["user", "country", "street_address", "apartment_address", "zip"]
    search_fields = ("user",)


admin.site.register(BillingAddress, BillingAddressAdmin)