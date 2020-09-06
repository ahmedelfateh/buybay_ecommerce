from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from app.users.forms import UserChangeForm, UserCreationForm

from allauth.account.models import EmailAddress

User = get_user_model()

# @admin.unregister(EmailAddress)
class EmailsInline(admin.TabularInline):
    model = EmailAddress
    readonly_fields = ["user"]
    max_num = 8
    extra = 0


admin.site.unregister(EmailAddress)


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]
    inlines = [EmailsInline]