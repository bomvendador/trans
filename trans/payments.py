#-*- encoding:utf-8-*-
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.messages import get_messages
from django.contrib import messages, sessions
from ru.models import SentDoc, PayStatus, PayMethod
from django.contrib.auth.decorators import login_required
import json


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
        context = {
            'data': request.POST
        }
        return render(request, 'success.html', context)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def change_just_paid(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        order_id = json_data['order_id']

        order = SentDoc.objects.get(id=order_id)
        order.just_paid = False
        order.save()