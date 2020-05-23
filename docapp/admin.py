from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from docapp.models import TicketUser, TicketItem

# Register your models here.
admin.site.register(TicketUser, UserAdmin)
admin.site.register(TicketItem)
