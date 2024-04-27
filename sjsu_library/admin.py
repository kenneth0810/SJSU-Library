from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserRegisterForm, CustomUserChangeForm
from .models import LibUser, Book, BorrowedBook

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserRegisterForm
    form = CustomUserChangeForm

    model = LibUser

    list_display = ('email', 'first_name', 'last_name', 'id_number' , 'is_librarian', 'is_active',
                    'is_staff', 'is_superuser', 'last_login',)
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'id_number', 'is_librarian', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'id_number', 'is_librarian', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email', 'first_name', 'last_name', 'id_number')
    ordering = ('first_name', 'last_name', 'email', 'id_number')

admin.site.register(LibUser, CustomUserAdmin)
admin.site.register(Book)
admin.site.register(BorrowedBook)