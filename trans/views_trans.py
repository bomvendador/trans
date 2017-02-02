#-*- encoding:utf-8-*-
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.messages import get_messages
from django.contrib import messages, sessions
from ru.models import SentDoc, PayStatus, PayMethod



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
        order.save()

        # request.ses

        messages.add_message(request, messages.INFO, 'payment')

        context = {
            'data': request.POST
        }
        return HttpResponseRedirect('/ru/dashbrd/order_details/', args=(order_id))