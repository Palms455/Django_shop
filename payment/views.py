from django.shortcuts import render, redirect, get_object_or_404
import braintree
from orders.models import Order
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
import weasyprint
from io import BytesIO

def payment_process(request):
    # Получение id заказа из сессии
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        # Получение токена для создания транзакции.
        nonce = request.POST.get('payment_method_nonce', None)
        # Создание и сохранение транзакции.
        result = braintree.Transaction.sale({
        'amount': '{:.2f}'.format(order.get_total_cost()),
        'payment_method_nonce': nonce,
        'options': {
        'submit_for_settlement': True
        }
        })
        if result.is_success:
            # Отметка заказа как оплаченного.
            order.paid = True
            # Сохранение ID транзакции в заказе.
            order.braintree_id = result.transaction.id
            order.save()
            # создание электронного сообщения
            subject = f'My Shop - Заказ № {order.id}'
            message = 'Во вложении документ о Вашем заказе'
            email = EmailMessage(subject, message, settings['EMAIL_HOST_USER'], [order.email])
            # формирование pdf
            html = render_to_string('orders/order/pdf.html', {'order': order})
            out = BytesIO()
            stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
            weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
            # Прикрепляем PDF к письму
            email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')
            email.send()
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # Формирование одноразового токена для JavaScript SDK.
        client_token = braintree.ClientToken.generate()
        return render(request,
        'payment/process.html',
        {'order': order,
        'client_token': client_token})

def payment_done(request):
    return render(request, 'payment/done.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')

