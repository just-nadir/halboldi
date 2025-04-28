from django.contrib import admin
from .models import Worker, Job, Order, Transaction, SMSLog

admin.site.register(Worker)
admin.site.register(Job)
admin.site.register(Order)
admin.site.register(Transaction)
admin.site.register(SMSLog)
