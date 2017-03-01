#-*- encoding:utf-8-*-
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.messages import get_messages
from django.contrib import messages, sessions
from ru.models import SentDoc, PayStatus, PayMethod, Payment, PriceLevel
from django.contrib.auth.decorators import login_required
import json
from dashboard_ru import views as dashboard_views
from datetime import datetime, timedelta

from decimal import Decimal

import logging
logger = logging.getLogger('django-debug')
from django.utils import timezone

@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        order_id = request.POST.get('LMI_PAYMENT_NO')
        payment_amount = request.POST.get('LMI_PAYMENT_AMOUNT')
        payment_date = request.POST.get('LMI_SYS_PAYMENT_DATE')
        price_level = request.POST.get('price_level')
        # logger.debug(u'price_level = ' + price_level)
        order = SentDoc.objects.get(id=order_id)
        if price_level == u'Стандарт':
            price_to_be_paid = order.price
            order.price_level = PriceLevel.objects.get(name=u'Стандарт')
        if price_level == u'Бизнес':
            price_to_be_paid = order.price_business
            order.price_level = PriceLevel.objects.get(name=u'Бизнес')

        if price_level == u'Профи':
            price_to_be_paid = order.price_profi
            order.price_level = PriceLevel.objects.get(name=u'Профи')

        if price_to_be_paid:
            if price_to_be_paid == Decimal(payment_amount):
                order.paystatus = PayStatus.objects.get(name='Paid')
            else:
                if Decimal(payment_amount) > 0:
                    order.paystatus = PayStatus.objects.get(name='Partially_paid')
        payment = Payment()
        payment.order = order
        payment.amount = payment_amount
        payment.method = PayMethod.objects.get(name='PayMaster')
        payment.price_level = PriceLevel.objects.get(name=price_level)
        payment_date_local = datetime.strptime(payment_date, '%Y-%m-%dT%H:%M:%S') + timedelta(hours=3)
        payment.date = payment_date_local
        order.payment_date = payment_date_local
        order.paystatus = PayStatus.objects.get(name='Paid')
        order.just_paid = True
        order.save()
        payment.save()
        # date = datetime.strptime(order.payment_date, '%Y-%m-%dT%H:%M:%S')
        date_ = payment_date_local.strftime("%d.%m.%Y, %H:%M")

        email_context = {
            'manager': order.resp,
            'order': order,
            'payment_date': date_,
            'payment': payment
        }
        # TODO изменить почту достваки
        dashboard_views.send_email(request, 'payment_recieved.html', 'info@prolingva.ru', ['orders@prolingva.ru'], email_context)
        dashboard_views.send_email(request, 'payment_recieved_admin.html', 'info@prolingva.ru', ['payments@prolingva.ru'], email_context)
        # dashboard_views.send_email(request, 'payment_recieved.html', 'info@prolingva.ru', order.user.email, email_context)

        # request.ses

        messages.add_message(request, messages.INFO, 'payment_success')
        url = '/ru/dashbrd/order_details/' + order_id
        context = {
            'data': request.POST
        }
        return HttpResponseRedirect(url)


@csrf_exempt
def payment_failure(request):
    if request.method == 'POST':
        order_id = request.POST.get('LMI_PAYMENT_NO')
        order = SentDoc.objects.get(id=order_id)
        order.payment_failure = True
        order.save()
        url = '/ru/dashbrd/order_details/' + order_id

        return HttpResponseRedirect(url)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def change_just_paid(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        order_id = json_data['order_id']

        order = SentDoc.objects.get(id=order_id)
        order.just_paid = False
        order.save()


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def change_payment_failure(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        order_id = json_data['order_id']

        order = SentDoc.objects.get(id=order_id)
        order.payment_failure = False
        order.save()