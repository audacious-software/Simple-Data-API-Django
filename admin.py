from django.contrib import admin

from .models import APIToken, APICall

@admin.register(APIToken)
class APITokenAdmin(admin.ModelAdmin):
    list_display = ('responsible_party', 'token',)

    search_fields = ('token', 'responsible_party',)

@admin.register(APICall)
class APICallAdmin(admin.ModelAdmin):
    list_display = ('token', 'when', 'errored',)
    list_filter = ('when', 'errored', 'token',)

    search_fields = ('request', 'response',)
