from rest_framework import viewsets
from .models import Worker, Job, Order, Transaction, BalanceTransaction, SMSLog
from .serializers import WorkerSerializer, JobSerializer, OrderSerializer, TransactionSerializer, BalanceTransactionSerializer, SMSLogSerializer
from core.utils.sms import send_sms

class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer

    def perform_update(self, serializer):
        instance = self.get_object()
        old_status = instance.status
        updated_order = serializer.save()

        if (
            old_status != 'bajarildi' and
            updated_order.status == 'bajarildi' and
            updated_order.assigned_worker is not None and
            updated_order.job is not None
        ):
            worker = updated_order.assigned_worker
            commission = updated_order.job.commission

            # 🔥 Avtomatik balansdan yechish (via BalanceTransaction)
            BalanceTransaction.objects.create(
                worker=worker,
                amount=-commission,
                description=f"Buyurtma #{updated_order.id} uchun komissiya"
            )

            # 📝 (ixtiyoriy) Transaction modelga ham yozish
            Transaction.objects.create(
                worker=worker,
                amount=-commission,
                note=f"Buyurtma #{updated_order.id} uchun komissiya yechildi"
            )

        if old_status != 'qabul_qilindi' and updated_order.status == 'qabul_qilindi':
            # Mijozga SMS
            if updated_order.phone and updated_order.assigned_worker:
                customer_msg = (
                    f"Hal bo'ldi!\nBuyurtmangiz qabul qilindi!\n"
                    f"ID: {updated_order.id}\n"
                    f"Usta: {updated_order.assigned_worker.full_name}\n"
                    f"Tel: {updated_order.assigned_worker.phone}\n"
                    "Bizni tanlaganingiz uchun raxmat!"
                )
                send_sms(updated_order.phone, customer_msg)

            # Ustaga SMS
            if updated_order.assigned_worker:
                worker_msg = (
                    f"Hal bo'ldi!\nSizda yangi buyurtma!\n"
                    f"ID: {updated_order.id}\n"
                    f"Mijoz: {updated_order.customer_name}\n"
                    f"Tel: {updated_order.phone}\n"
                    "Mijoz bilan bog'lanishingizni so'raymiz!"
                )
                send_sms(updated_order.assigned_worker.phone, worker_msg)

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by('-created_at')
    serializer_class = TransactionSerializer

class BalanceTransactionViewSet(viewsets.ModelViewSet):
    serializer_class = BalanceTransactionSerializer

    def get_queryset(self):
        queryset = BalanceTransaction.objects.all().order_by('-created_at')
        worker_id = self.request.query_params.get('worker')
        if worker_id:
            queryset = queryset.filter(worker_id=worker_id)
        return queryset

class SMSLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SMSLog.objects.all().order_by('-created_at')
    serializer_class = SMSLogSerializer