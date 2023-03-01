from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import gettext_lazy as _

from system.admin import UserAdmin as BaseUserAdmin
from .models import User, AttributeLifeTable, ColumnLifeTable, LifeTable, Cell, Answer


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_student",
                    "course",
                    "period",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )
    form = UserChangeForm
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)


admin.site.register(User, UserAdmin)
admin.site.register(AttributeLifeTable)
admin.site.register(ColumnLifeTable)
admin.site.register(LifeTable)
admin.site.register(Cell)
admin.site.register(Answer)
