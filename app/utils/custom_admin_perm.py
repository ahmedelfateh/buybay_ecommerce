from django.contrib.admin import ModelAdmin


class CustomAccessAdmin(ModelAdmin):
    """
    Override the default django permission class,
    this make it possible to use admin dashboard with multiple users
    with more restrected measures.
    """

    def has_module_permission(self, request):
        if request.user.is_superuser or request.user.is_staff:
            return True

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.is_staff:
            return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.is_staff:
            return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.is_staff:
            return True

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.is_staff:
            return True
