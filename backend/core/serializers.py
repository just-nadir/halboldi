from rest_framework import serializers
from .models import Worker, Job, Order, Transaction, BalanceTransaction, SMSLog 

class WorkerSerializer(serializers.ModelSerializer):
    age = serializers.ReadOnlyField()
    balance = serializers.ReadOnlyField()  # qo‘shilsin

    class Meta:
        model = Worker
        fields = '__all__'



class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    job_commission = serializers.FloatField(source='job.commission', read_only=True)
    worker_name = serializers.CharField(source='assigned_worker.full_name', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class BalanceTransactionSerializer(serializers.ModelSerializer):
    worker_name = serializers.CharField(source='worker.full_name', read_only=True)

    class Meta:
        model = BalanceTransaction
        fields = ['id', 'worker', 'worker_name', 'amount', 'description', 'created_at']

class SMSLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSLog
        fields = '__all__'