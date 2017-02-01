#-*- encoding:utf-8-*-
from django.shortcuts import render, redirect
from django.http import HttpResponse


def payment_success(request):
    if request.method == 'POST':
        context = {
            'data': request.POST
        }
    return HttpResponse(context)