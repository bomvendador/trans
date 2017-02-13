#-*- encoding:utf-8-*-
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.messages import get_messages
from django.contrib import messages, sessions
from ru.models import SentDoc, PayStatus, PayMethod
from django.contrib.auth.decorators import login_required
import json
from dashboard_ru import views as dashboard_views


@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        order_id = request.POST.get('LMI_PAYMENT_NO')
        payment_amount = request.POST.get('LMI_PAYMENT_AMOUNT')
        payment_date = request.POST.get('LMI_SYS_PAYMENT_DATE')
        order = SentDoc.objects.get(id=order_id)
        order.payment_amount = payment_amount
        order.payment_date = payment_date
        order.paystatus = PayStatus.objects.get(name='Paid')
        order.paymethod = PayMethod.objects.get(name='PayMaster')
        order.just_paid = True
        order.save()
        email_context = {
            'manager': order.resp.first_name,
            'order': order
        }
        # TODO изменить почту достваки
        dashboard_views.send_email(request, 'payment_recieved.html', 'info@prolingva.ru', 'orders@prolingva.ru', email_context)
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