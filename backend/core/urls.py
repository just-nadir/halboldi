from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (WorkerViewSet, JobViewSet, OrderViewSet,
TransactionViewSet, BalanceTransactionViewSet, SMSLogViewSet)

router = DefaultRouter()
router.register(r'workers', WorkerViewSet)
router.register(r'jobs', JobViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'balance-transactions', BalanceTransactionViewSet, basename='balance-transaction')
router.register(r'sms-logs', SMSLogViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
