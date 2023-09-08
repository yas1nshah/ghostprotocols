from django.contrib import admin

from base.models import Car, CarReports, Gallery, DemandList, WeSellYouWin

# Register your models here.
admin.site.register(Car)
admin.site.register(Gallery)
admin.site.register(DemandList)
admin.site.register(WeSellYouWin)
admin.site.register(CarReports)
