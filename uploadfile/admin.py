from django.contrib import admin
from .models import File, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'created_at')
    search_fields = ('username',)
    readonly_fields = ('created_at',)


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'file_name', 'file_size', 'format', 'sender', 'recipient', 'created_at')
    search_fields = ('title', 'file_name')
    list_filter = ('format', 'created_at')
    readonly_fields = ('file_size', 'format', 'created_at')
    fieldsets = (
        ('اطلاعات فایل', {
            'fields': ('file_name', 'title', 'file_address', 'format', 'file_size')
        }),
        ('فرستنده و گیرنده', {
            'fields': ('sender', 'recipient')
        }),
        ('تاریخ', {
            'fields': ('created_at',)
        }),
    )
