#-*- encoding:utf-8-*-
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        context = {
            'data': request.POST
        }
    return HttpResponse(request.POST)