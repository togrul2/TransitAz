from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(City)

admin.site.register(Station)
admin.site.register(Transport)
# admin.site.register(Ticket)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = '__str__', 'purchased_at'


