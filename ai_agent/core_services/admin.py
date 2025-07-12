from django.contrib import admin
from .models import AgentLog, ContactMessage

# Register AgentLog for admin observability
admin.site.register(AgentLog)
admin.site.register(ContactMessage)