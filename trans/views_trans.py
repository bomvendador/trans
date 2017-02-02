#-*- encoding:utf-8-*-
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.messages import get_messages
from django.contrib import messages


@csrf_exempt
def payment_success(request):
    if request.method == 'POST':

        messages.add_message(request, messages.INFO, 'payment')

        context = {
            'data': request.POST
        }
    return render(request, 'success.html', context)