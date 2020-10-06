from django_shop.celery import app
from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from django.conf import settings

@shared_task()
def order_created(order_id):
    """Отправка email уведомлений при успешном оформлении заказа"""
    order = Order.objects.get(id=order_id)
    subject = f"Заказ № {order_id}"
    message = f"{order.first_name}, спасибо за покупку! " \
              f"Ваш заказ № {order.id} будет обработан в самое ближайшее время"
    mail_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, [order.email])
    return mail_sent