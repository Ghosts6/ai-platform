from django.contrib import admin
from .models import AgentLog

# Register AgentLog for admin observability
admin.site.register(AgentLog)
