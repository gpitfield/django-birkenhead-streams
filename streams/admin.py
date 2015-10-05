from django.contrib import admin
from .models import Stream

class StreamAdmin(admin.ModelAdmin):
	list_display = ['title', 'timestamp', 'status', 'archive']

admin.site.register(Stream, StreamAdmin)
