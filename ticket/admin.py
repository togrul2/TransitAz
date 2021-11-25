from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(City)

admin.site.register(BusStation)
admin.site.register(Bus)
admin.site.register(BusTicket)

admin.site.register(TrainStation)
admin.site.register(Train)
admin.site.register(TrainTicket)
