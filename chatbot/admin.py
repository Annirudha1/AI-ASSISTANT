from django.contrib import admin
from .models import Chat

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'answer', 'timestamp')
    list_filter = ('user', 'timestamp')
    search_fields = ('question', 'answer', 'user__username')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
