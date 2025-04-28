from django.db import models
from datetime import date

class Worker(models.Model):
    full_name = models.CharField(max_length=100)
    specialties = models.CharField(max_length=255)  # "santexnik,elektrik"
    birth_date = models.DateField()
    phone = models.CharField(max_length=20)
    experience = models.PositiveIntegerField()
    rating = models.FloatField(default=0)
    @property
    def balance(self):
        return sum(t.amount for t in self.balancetransaction_set.all())


    @property
    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

    def __str__(self):
        return self.full_name


class Job(models.Model):
    title = models.CharField(max_length=100)
    commission = models.FloatField()  # Ustadan yechiladigan komissiya

    def __str__(self):
        return self.title


class Order(models.Model):
    STATUS_CHOICES = [
        ('yangi', 'Yangi'),
        ('qabul_qilindi', 'Qabul qilindi'),
        ('bajarilmoqda', 'Bajarilmoqda'),
        ('bajarildi', 'Bajarildi'),
        ('bekor', 'Bekor qilindi'),
    ]

    customer_name = models.CharField(max_length=100)
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='yangi')
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_worker = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True)
    cancel_reason = models.TextField(null=True, blank=True)  # <-- YANGI

    def __str__(self):
        return f"{self.customer_name} - {self.job}"



class Transaction(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='transactions')
    amount = models.FloatField()  # manfiy bo‘lsa chiqim, musbat bo‘lsa kirim
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.worker.full_name} - {self.amount} so'm"

class BalanceTransaction(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    amount = models.FloatField()  # Manfiy bo‘lsa — chiqim, musbat bo‘lsa — kirim
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.worker} | {self.amount} | {self.created_at}"

class SMSLog(models.Model):
    phone = models.CharField(max_length=20)
    message = models.TextField()
    success = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone} | {'✅' if self.success else '❌'} | {self.created_at.strftime('%Y-%m-%d %H:%M')}"
