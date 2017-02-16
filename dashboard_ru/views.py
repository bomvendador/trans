# -*- encoding:utf-8-*-
import json
import re, os
from string import punctuation

from custom_def import *

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from ru.models import SentDoc, SentFiles, UserProfile, Language, OrderStatus, PayMethod, Translator, Translator_Lang, \
    TranslationFiles, Role, Manager, OrderComments, Admin, PaymentDetails, Client, TranslationType, TranslationTheme, \
    PayStatus, BackCall, BackCallComments, Testimonials, Company, Property, Invoice, OrderCommentsClients, OrderCommentsClientsAnswer

from django.utils.dateparse import parse_date, parse_datetime
from django.db.models import Sum

from django.core.mail import EmailMessage, send_mail
from django.template.loader import get_template
from templated_email import send_templated_mail, InlineImage

from trans import settings

import logging

from django.contrib.messages import get_messages
from django.contrib import messages, sessions

import datetime

logger = logging.getLogger('django-debug')


def get_user_userprofile(request):
    user = User.objects.get(id=request.user.id)
    user_profile = UserProfile.objects.get(user=user)
    context = {
        'user': user,
        'user_profile': user_profile
    }
    return context


def get_data_proc(request):
    user = User.objects.get(id=request.user.id)
    user_profile = UserProfile.objects.get(user=user)
    new_orders = SentDoc.objects.filter(status=OrderStatus.objects.get(name=u'Новый'))
    client = None
    context = {}
    if user_profile.role.role_name != u'Клиент':
        new_calls_count = BackCall.objects.filter(new=True).count()
        context.update({
            'new_calls_count': new_calls_count
        })
    if user_profile.role.role_name == u'Менеджер':
        new_count = SentDoc.objects.filter(resp=user).filter(
            status=OrderStatus.objects.get(name=u'Назначен менеджер')).count()
        # print('Менеджер нов = ' + str(new_count))
    else:
        # print('role ' + str(user_profile.role.id))
        if user_profile.role.role_name == u'Суперадмин' or user_profile.role.role_name == u'Админ':
            new_count = SentDoc.objects.filter(status=OrderStatus.objects.get(name=u'Новый')).count()
            new_testimonials = Testimonials.objects.filter(new=True).count()
            context.update({
                'new_testimonials': new_testimonials
            })
        else:
            new_count = 0
        if user_profile.role.role_name == u'Клиент':
            try:
                client = Client.objects.get(user=user)
            except Client.DoesNotExist:
                client = None
    context.update({
        'user': user,
        'sent_docs': new_orders,
        'new_count': new_count,
        'user_profile': user_profile,
        'client': client
    })
    return context


def login_board(request):
    if request.user.is_authenticated():
        # print('not logged')
        return redirect('ru:dashboard_ru:base_board', user_id=request.user.id)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        logger.debug(email + password)
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:
                # print('logged')
                login(request, user)
                user_profile = UserProfile.objects.get(user=user)
                if user_profile.role.role_name == u'Клиент':
                    client = Client.objects.get(user=user)
                    client.visited_times += 1
                    client.save()
                # logger.debug('id = ' + str(user.id))
                # return redirect('ru:dashboard_ru:base_board', user_id=user.id)
                return HttpResponse(user.id)
        else:
            return HttpResponse('error')
    return render(request, 'sign_in_board.html')


def sign_up_board(request):
    return render(request, 'sign_up_board.html')


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def base_board(request, user_id):
    # print(user_id)
    user = User.objects.get(id=user_id)
    new_count = 0
    # user_role = UserProfile.objects.get(user=user)
    context = get_data_proc(request)

    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = None
    if user_profile.role.role_name == u'Суперадмин' or user_profile.role.role_name == u'Админ':
        # print('Супер')
        sent_docs = SentDoc.objects.all()
        try:
            new_count = SentDoc.objects.filter(status=OrderStatus.objects.get(name=u'Новый')).count()
            # print(new_count)
        except SentDoc.DoesNotExist:
            new_count = 0

    elif user_profile.role.role_name == u'Менеджер':
        try:
            new_count = SentDoc.objects.filter(status=OrderStatus.objects.get(name=u'Назначен менеджер')).filter(
                resp=user).count()
            # print(new_count)
        except SentDoc.DoesNotExist:
            new_count = 0
        try:
            sent_docs = SentDoc.objects.filter(user=user)
        except SentDoc.DoesNotExist:
            sent_docs = None
    elif user_profile.role.role_name == u'Клиент':
        # try:
        # new_count = SentDoc.objects.filter(status=OrderStatus.objects.get(name='Назначен менеджер')).filter(resp=user).count()
        # print(new_count)
        # except SentDoc.DoesNotExist:
        sum_paid = SentDoc.objects.filter(user=request.user).filter(payment_amount__isnull=False).aggregate(
            Sum('payment_amount'))
        update_client_statistics(request.user)
        new_count = 0
        print(sum_paid)
        client = Client.objects.get(user=request.user)
        orders_for_payment = SentDoc.objects.filter(user=user).filter(price__isnull=False).exclude(
            paystatus=PayStatus.objects.get(name='Paid'))

        context.update({
            'client': client,
            'sum_paid': sum_paid['payment_amount__sum'],
            'orders_for_payment': orders_for_payment
        })
        try:
            sent_docs = SentDoc.objects.filter(user=user)
        except SentDoc.DoesNotExist:
            sent_docs = None
    else:
        try:
            sent_docs = SentDoc.objects.filter(user=user)
        except SentDoc.DoesNotExist:
            sent_docs = None

    context.update({
        'user': user,
        'sent_docs': sent_docs,
        'user_profile': user_profile,
        'new_count': new_count

    })
    return render(request, 'base_board.html', context)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def get_sent_docs(request):
    user = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user=user)
    # if superadmin
    sent_docs = None
    context = {}
    new_count = 0
    if user_profile.role.role_name == u'Суперадмин' or user_profile.role.role_name == u'Админ':
        new_testimonials = Testimonials.objects.filter(new=True).count()
        context.update({
            'new_testimonials': new_testimonials
        })

        new_calls_count = BackCall.objects.filter(new=True).count()
        context.update({
            'new_calls_count': new_calls_count
        })
        context.update({
            'new_calls_count': new_calls_count
        })
        sent_docs = SentDoc.objects.all()
        # sent_docs_files = SentFiles.
        try:
            new_count = SentDoc.objects.filter(status=OrderStatus.objects.get(name=u'Новый')).count()
        except SentDoc.DoesNotExist:
            new_count = 0
    elif user_profile.role.role_name == u'Менеджер':
        try:
            sent_docs = SentDoc.objects.filter(resp=user).order_by('id')
            new_count = new_count = SentDoc.objects.filter(
                status=OrderStatus.objects.get(name=u'Назначен менеджер')).filter(resp=user).count()
        except SentDoc.DoesNotExist:
            sent_docs = None

    elif user_profile.role.role_name == u'Клиент':
        sent_docs = SentDoc.objects.filter(user=user).order_by('id')
        # orders_for_payment = SentDoc.objects.filter(user=user).filter(price__isnull=False).exclude(paystatus=PayStatus.objects.get(name='Paid'))
        # context.update({'orders_for_payment': orders_for_payment})
    context.update({
        'sent_docs': sent_docs,
        'user_profile': user_profile,
        'new_count': new_count

    })
    return render(request, 'sent_docs.html', context)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def get_new_sent_docs(request):
    # if request.method == 'POST':
    user = User.objects.get(id=request.user.id)
    user_profile = UserProfile.objects.get(user=user)
    # if superadmin
    sent_docs = None
    new_count = 0
    if user_profile.role.role_name == u'Суперадмин' or user_profile.role.role_name == u'Админ':
        sent_docs = SentDoc.objects.filter(status=OrderStatus.objects.get(name=u'Новый'))
        # sent_docs_files = SentFiles.
        try:
            new_count = SentDoc.objects.filter(status=OrderStatus.objects.get(name=u'Новый')).count()
        except SentDoc.DoesNotExist:
            new_count = 0
    elif user_profile.role.role_name == u'Менеджер':
        try:
            sent_docs = SentDoc.objects.filter(resp=user).filter(
                status=OrderStatus.objects.get(name=u'Назначен менеджер')).order_by('id')
            new_count = sent_docs.count()

        except SentDoc.DoesNotExist:
            sent_docs = None

    context = {
        'sent_docs': sent_docs,
        'user_profile': user_profile,
        'new_count': new_count,
        'new_orders': 1
    }
    return render(request, 'sent_docs.html', context)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def get_in_progress_sent_docs(request):
    # if request.method == 'POST':
    user = User.objects.get(id=request.user.id)
    user_profile = UserProfile.objects.get(user=user)
    # if superadmin
    new_count = 0
    if user_profile.role.role_name == u'Суперадмин' or user_profile.role.role_name == u'Админ':
        sent_docs = SentDoc.objects.all().exclude(status=OrderStatus.objects.get(name=u'Выполнен')).exclude(
            status=OrderStatus.objects.get(name=u'Новый'))
        # sent_docs_files = SentFiles.
        try:
            new_count = SentDoc.objects.filter(status=OrderStatus.objects.get(name=u'Новый')).count()
        except SentDoc.DoesNotExist:
            new_count = 0
    if user_profile.role.role_name == u'Менеджер':
        sent_docs = SentDoc.objects.all().filter(resp=user).exclude(
            status=OrderStatus.objects.get(name=u'Выполнен')).exclude(
            status=OrderStatus.objects.get(name=u'Назначен менеджер'))
    if user_profile.role.role_name == u'Клиент':
        sent_docs = SentDoc.objects.all().filter(user=user).exclude(status=OrderStatus.objects.get(name=u'Выполнен'))

    context = {
        'sent_docs': sent_docs,
        'user_profile': user_profile,
        'new_count': new_count,
        'in_progress_orders': 1
    }
    return render(request, 'sent_docs.html', context)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def get_complete_sent_docs(request):
    # if request.method == 'POST':
    user = User.objects.get(id=request.user.id)
    user_profile = UserProfile.objects.get(user=user)
    # if superadmin
    new_count = 0
    if user_profile.role.role_name == u'Суперадмин' or user_profile.role.role_name == u'Админ':
        sent_docs = SentDoc.objects.all().filter(status=OrderStatus.objects.get(name=u'Выполнен'))
        # sent_docs_files = SentFiles.
        try:
            new_count = SentDoc.objects.filter(status=OrderStatus.objects.get(name=u'Новый')).count()
        except SentDoc.DoesNotExist:
            new_count = 0
        context = {
            'sent_docs': sent_docs,
            'user_profile': user_profile,
            'new_count': new_count,
            'orders_complete': 1
        }
        return render(request, 'sent_docs.html', context)
    elif user_profile.role.role_name == u'Менеджер':
        sent_docs = SentDoc.objects.all().filter(status=OrderStatus.objects.get(name=u'Выполнен')).filter(resp=user)
        try:
            new_count = SentDoc.objects.filter(status=OrderStatus.objects.get(name=u'Назначен менеджер')).filter(
                resp=user).count()
        except SentDoc.DoesNotExist:
            new_count = 0

        context = {
            'sent_docs': sent_docs,
            'user_profile': user_profile,
            'new_count': new_count,
            'orders_complete': 1
        }
        return render(request, 'sent_docs.html', context)
    elif user_profile.role.role_name == u'Клиент':
        sent_docs = SentDoc.objects.all().filter(status=OrderStatus.objects.get(name=u'Выполнен')).filter(user=user)
        context = {
            'sent_docs': sent_docs,
            'user_profile': user_profile,
            'new_count': new_count,
            'orders_complete': 1
        }
        return render(request, 'sent_docs.html', context)
    return HttpResponse()


def logout_board(request):
    if request.user is not None:
        logout(request)
        return redirect('ru:dashboard_ru:login_board')


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def get_new_orders(request):
    user = User.objects.get(id=request.user.id)
    user_profile = UserProfile.objects.get(user=user)
    if user_profile.role.role_name == u'Суперадмин':
        context = get_data_proc(request)
        context.update({
            'new_orders': 1
        })
        # context = {
        #     'sent_docs': new_orders,
        #     'new_count': new_count,
        #     'user_profile': user_profile
        # }
        return render(request, 'sent_docs.html', context)
    else:
        return HttpResponse('Нет прав')


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def add_new_order(request):
    context = get_data_proc(request)
    sent_docs = SentDoc.objects.all()
    user_profile = UserProfile.objects.get(user=request.user)
    clients = Client.objects.all()
    if user_profile.role.role_name == u'Менеджер':
        new_count = sent_docs.filter(status=1).filter(resp=request.user).count()

        context.update({'clients': clients})
    else:
        context.update({'clients': clients})
        if user_profile.role.role_name == u'Суперадмин' or user_profile.role.role_name == u'Админ':
            new_count = sent_docs.filter(status=1).count()
        else:
            new_count = None

    context.update({
        'new_order': True,
        'langs': Language.objects.all().order_by('name'),
        'new_count': new_count
    })
    return render(request, 'new_order.html', context)


# @login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def update_manager_statistics(user):
    try:
        manager = Manager.objects.get(user=user)
        orders_in_progress_manager = SentDoc.objects.filter(status=OrderStatus.objects.get(name=u'В работе')).filter(
            resp=user).count()
        orders_new = SentDoc.objects.filter(status=OrderStatus.objects.get(name=u'Назначен менеджер')).filter(
            resp=user).count()
        orders_complete = SentDoc.objects.filter(status=OrderStatus.objects.get(name=u'Выполнен')).filter(
            resp=user).count()
        manager.orders_in_progress = orders_in_progress_manager
        manager.orders_new = orders_new
        manager.orders_complete = orders_complete

        manager.save()
    except Manager.DoesNotExist:
        return 'manager not exist'


def update_client_statistics(user):
    client = Client.objects.get(user=user)
    user = User.objects.get(id=client.user.id)
    orders_in_progress_client = SentDoc.objects.filter(user=user).exclude(
        status=OrderStatus.objects.get(name=u'Выполнен')).count()
    orders_complete_client = SentDoc.objects.filter(user=user).filter(
        status=OrderStatus.objects.get(name=u'Выполнен')).count()
    orders_paid_client = SentDoc.objects.filter(user=user).filter(payment_date__isnull=False).count()
    # orders_new = SentDoc.objects.filter(status=OrderStatus.objects.get(name='Назначен менеджер')).filter(resp=user).count()
    # orders_complete = SentDoc.objects.filter(status=OrderStatus.objects.get(name='Выполнен')).filter(resp=user).count()
    client.orders_in_progress = orders_in_progress_client
    client.orders_paid = orders_paid_client
    client.orders_complete = orders_complete_client

    client.save()


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def order_details(request, order_id):
    user = User.objects.get(id=request.user.id)
    user_profile = UserProfile.objects.get(user=user)
    # context = get_user_userprofile(request)
    context = get_data_proc(request)
    new_count = 0
    order_det = SentDoc.objects.get(id=order_id)
    translation_files = TranslationFiles.objects.filter(order=order_det)
    comments = OrderComments.objects.filter(order=order_det)
    companies = Company.objects.filter(user=order_det.user)

    msgs = get_messages(request)
    # order_id_msg = None
    for msg in msgs:
        payment_message = msg
        context.update({'payment_message': payment_message})
        break

    try:
        author_role = UserProfile.objects.get(user=order_det.author)
        # author = author_role.role.role_name + ' - ' + order_det.user.first_name + ' ' + order_det.user.last_name
    except UserProfile.DoesNotExist:
        author_role = None
    try:
        user_role = UserProfile.objects.get(user=request.user)
        # author = author_role.role.role_name + ' - ' + order_det.user.first_name + ' ' + order_det.user.last_name
    except UserProfile.DoesNotExist:
        user_role = None
    try:
        files = SentFiles.objects.filter(sent_doc=order_det)

    except SentFiles.DoesNotExist:
        # print('f = none')
        files = None
        # for f in files:
        # print('file = ' + str(f.file_name))

    try:
        client_comments = OrderCommentsClients.objects.filter(order=order_det)
        context.update({
            'client_comments': client_comments
        })
    except OrderCommentsClients.DoesNotExist:
        pass
    try:
        client_comments_answers = OrderCommentsClientsAnswer.objects.filter(order=order_det)
        context.update({
            'client_comments_answers': client_comments_answers
        })
    except OrderCommentsClientsAnswer.DoesNotExist:
        pass

    if user_profile.role.role_name == u'Суперадмин' or user_profile.role.role_name == u'Админ':
        try:
            new_count = SentDoc.objects.filter(status=OrderStatus.objects.get(name=u'Новый')).count()
        except SentDoc.DoesNotExist:
            new_count = 0
    else:
        if user_profile.role.role_name == u'Менеджер':
            order_det.status = OrderStatus.objects.get(name=u'В работе')
            order_det.save()
            update_manager_statistics(user)
            try:
                new_count = SentDoc.objects.filter(status=OrderStatus.objects.get(name=u'Назначен менеджер')).filter(
                    resp=user).count()
            except SentDoc.DoesNotExist:
                sent_docs = None

    context.update({
        'order_details': order_det,
        'files': files,
        'langs': Language.objects.all().order_by('name'),
        'managers': Manager.objects.all(),
        'new_count': new_count,
        'order_status': OrderStatus.objects.all(),
        'author_role': author_role,
        'translators': Translator.objects.all(),
        'paymethods': PayMethod.objects.all(),
        'translation_files': translation_files,
        'comments': comments,
        'user_role': user_role,
        'trans_themes': TranslationTheme.objects.all(),
        'trans_types': TranslationType.objects.all(),
        'companies': companies
    })
    return render(request, 'order_details.html', context)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def download_file(request, file_id):
    path = SentFiles.objects.get(id=file_id)

    with open(path.file.path, 'rb') as f:
        data = f.read()

    response = HttpResponse(data, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % path.file_name
    return response


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def download_translation_file(request, file_id):
    path = TranslationFiles.objects.get(id=file_id)
    with open(path.file.path, 'rb') as f:
        data = f.read()

    response = HttpResponse(data, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % path.file_name

    if UserProfile.objects.get(user=request.user).role.role_name == u'Клиент':
        order = SentDoc.objects.get(id=TranslationFiles.objects.get(id=file_id).order_id)
        if order.paystatus.name != 'Paid':
            return HttpResponse(u'Заявка не оплачена')
        else:
            order.translation_downloaded = True
            order.save()
            return response
    return response


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def set_resp(request):
    if request.method == 'POST':
        resp = request.POST.get('resp', None)
        print('1 - ' + str(resp))
        resp = json.loads(request.body.decode('utf-8'))
        resp_id = resp['resp'].split('.')
        print('2 - ' + str(resp_id[0]) + ' - ' + str(resp['order_id']))
        sent_docs = SentDoc.objects.get(id=resp['order_id'])
        print(resp_id[0])
        if resp_id[0] != '':
            sent_docs.resp = User.objects.get(id=resp_id[0])
            sent_docs.status = OrderStatus.objects.get(name=u'Назначен менеджер')
        else:
            sent_docs.resp = None
            sent_docs.status = OrderStatus.objects.get(name=u'Новый')

        # try:
        #     sent_docs.resp = User.objects.get(id=resp_id[0])
        #     sent_docs.status = OrderStatus.objects.get(name='Назначен менеджер')
        # except User.DoesNotExist:
        #     sent_docs.resp = None
        # sent_docs.status = OrderStatus.objects.get(name='Выполнен')
        sent_docs.save()
        manager = Manager.objects.get(user=User.objects.get(id=resp_id[0]))
        orders_new_manager = SentDoc.objects.filter(resp=User.objects.get(id=resp_id[0])).filter(
            status=OrderStatus.objects.get(name=u'Назначен менеджер')).count()
        manager.orders_new = orders_new_manager
        manager.save()

        new_count = SentDoc.objects.filter(status=OrderStatus.objects.get(name=u'Новый')).count()
        return HttpResponse(new_count)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def set_order_status(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        user_profile = UserProfile.objects.get(user=user)
        if user_profile.role.role_name != u'Клиент':
            json_data = json.loads(request.body.decode('utf-8'))
            order_id = json_data['order_id']
            order_status = json_data['order_status']
            sent_doc = SentDoc.objects.get(id=order_id)
            sent_doc.status = OrderStatus.objects.get(name=order_status)
            sent_doc.save()
            return HttpResponse('ok')
    else:
        return HttpResponse('error')


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def get_translators_list(request):
    translators = Translator.objects.all()

    context = get_data_proc(request)
    context.update({
        'translators': translators
    })
    return render(request, 'translators_list.html', context)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def get_translators_details(request, translator_id):
    context = get_data_proc(request)
    translator = Translator.objects.get(id=translator_id)
    creator = User.objects.get(id=translator.creator.id)
    creator_profile = UserProfile.objects.get(user=creator)
    # print(translator.name)
    langs_select = Translator_Lang.objects.filter(translator=translator)
    list = []
    for i in langs_select:
        list.append(i.lang_id)
    # print(list)
    langs = Language.objects.all().exclude(id__in=list).order_by('name')
    if translator.date_birth:
        birthday_db = translator.date_birth.strftime("%d.%m.%Y")
        context.update({
            'birthday': birthday_db

        })
    context.update({
        'creator_profile': creator_profile,
        'creator': creator,
        'translator': translator,
        'langs': langs,
        'langs_select': langs_select,

    })
    return render(request, 'translator_details.html', context)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def save_translator_photo(request, translator_id):
    if request.method == 'POST':
        files = request.FILES.getlist('photo')
        translator = Translator.objects.get(id=translator_id)
        # translator_id = json_data['translator_id']
        # photo = Translator.photo()
        # print(translator_id)
        for file in files:
            translator.photo = file
            translator.photo_name = file.name
        translator.save()
        return HttpResponse(translator.photo_name)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def create_translator(request):
    if request.method == 'POST':
        data = request.POST
        if data['new_translator'] == 'no':
            translator = Translator.objects.get(id=data['translator_id'])
            user = User.objects.get(id=translator.user.id)
        else:
            translator = Translator()
            user = User()
            password = User.objects.make_random_password()
            user.set_password(password)
            translator.init_password = password

        name = request.POST.get('name_translator')
        email = request.POST.get('email_translator')
        tel = request.POST.get('tel_translator')
        new = request.POST.get('new_translator')
        birthday = request.POST.get('birthday')
        birthday_split = birthday.split('.')
        if birthday:
            birthday_str = birthday_split[2] + '-' + birthday_split[1] + '-' + birthday_split[0]
            translator.date_birth = parse_date(birthday_str)

        if new == 'no':
            translator.changed_by = request.user
        else:
            translator.creator = request.user
        translator.name = name
        user.first_name = name
        translator.email = email
        user.email = email
        user.username = email
        user.save()
        translator.user = user
        translator.tel = tel
        # translator.author = request.user

        translator.save()
        Translator_Lang.objects.filter(translator=translator).delete()

        for item in data:
            if 'lang_' in item:
                language = Language.objects.get(name=request.POST.get(item))

                langs_inst = Translator_Lang()

                langs_inst.translator = translator
                langs_inst.user = request.user
                langs_inst.lang = language
                langs_inst.save()
        if data['new_translator'] == 'yes':
            return HttpResponse(translator.id)
        else:
            return HttpResponse('ok')

    langs = Language.objects.all().order_by('name')
    context = get_data_proc(request)
    context.update({
        'langs': langs,

    })
    return render(request, 'translator_new.html', context)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def delete_translator(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        translator_id = json_data['translator_id']
        Translator.objects.get(id=translator_id).delete()
        # return redirect('ru:dashboard_ru:get_translators_list')
        return HttpResponse('ok')


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def delete_order(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        order_id = json_data['order_id']
        order = SentDoc.objects.get(id=order_id)
        SentFiles.objects.filter(sent_doc=order).delete()
        order.delete()
        return HttpResponse('ok')


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def set_translator_for_order(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        order_id = json_data['order_id']
        order = SentDoc.objects.get(id=order_id)
        translator_json = json_data['translator']
        print(translator_json)
        if translator_json != '':
            translator_id = translator_json.split('_')
            # print(str(translator_id[1]))
            translator = Translator.objects.get(id=translator_id[1])
            order.status = OrderStatus.objects.get(name=u'Назначен переводчик')
            message = 'translator is set'

        else:
            translator = None
            order.status = OrderStatus.objects.get(name=u'Расчет отослан')
            message = 'translator is none'

        order.translator = translator
        order.save()
        # print(translator)
        return HttpResponse(message)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def add_file_to_order(request):
    if request.method == 'POST':
        # print(request.POST.get('order_id'))
        order = SentDoc.objects.get(id=request.POST.get('order_id'))
        order.status = OrderStatus.objects.get(name=u'В работе')
        files = request.FILES.getlist('file')
        f = SentFiles()
        print(order.id)
        print(files)
        for file in files:
            f = SentFiles(file=file, sent_doc=order, file_name=file.name)
            f.save()
            print(f.file_name)
            file_name = f.file_name
            file_id = f.id
        files_qnt = SentFiles.objects.filter(sent_doc=order).count()
        order.files_qnt = files_qnt
        order.save()

        return HttpResponse(json.dumps({'file_name': file_name, 'file_id': file_id}))


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def add_translation_file_to_order(request):
    if request.method == 'POST':
        # print(request.POST.get('order_id'))
        order = SentDoc.objects.get(id=request.POST.get('order_id'))
        if order.paystatus.name == 'Paid':
            order.status = OrderStatus.objects.get(name=u'Выполнен')

        order.translation_files = True
        files = request.FILES.getlist('file')
        f = SentFiles()
        print(order.id)
        print(files)
        for file in files:
            f = TranslationFiles(file=file, order=order, file_name=file.name, uploaded_by=request.user)
            f.save()
            print(f.file_name)
            file_name = f.file_name
            file_id = f.id
        # trans_array = TranslationFiles.objects.filter(order=order)
        # order.files_qnt = files_qnt

        order.save()

        return HttpResponse(json.dumps({'file_name': file_name, 'file_id': file_id}))


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def delete_file_from_order(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        file_id = json_data['file_id']
        print(file_id)
        SentFiles.objects.get(id=file_id).delete()

        return HttpResponse(file_id)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def delete_translation_file_from_order(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        file_id = json_data['file_id']
        order = SentDoc.objects.get(id=TranslationFiles.objects.get(id=file_id).order.id)
        order.translation_downloaded = False
        TranslationFiles.objects.get(id=file_id).delete()

        order_files_qnt = TranslationFiles.objects.filter(order=order).count()
        if order_files_qnt == 0:
            order.translation_files = False

            logger.debug('file qnt = ' + str(order_files_qnt))
        order.save()

        return HttpResponse(file_id)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def update_order(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        order_id = request.POST.get('order_id')
        sent_doc = SentDoc.objects.get(id=order_id)
        user = User.objects.get(id=user_id)
        user_profile = UserProfile.objects.get(user=user)
        user_account = User.objects.get(id=request.user.id)
        user_profile_account = UserProfile.objects.get(user=user_account)

        if user_profile_account.role.role_name != u'Менеджер':

            name = request.POST.get('name_doc_send')
            # print(name)
            email = request.POST.get('email_doc_send')
            tel = request.POST.get('tel_doc_send')
            text_doc_send = request.POST.get('text_doc_send')
            trans_theme = request.POST.get('trans_theme')
            trans_type = request.POST.get('trans_type')
            # print(trans_theme)
            # print(trans_type)
            try:
                sent_doc.translation_theme = TranslationTheme.objects.get(short_name=trans_theme)
            except TranslationTheme.DoesNotExist:
                sent_doc.translation_theme = None
            try:
                sent_doc.translation_type = TranslationType.objects.get(short_name=trans_type)
            except TranslationType.DoesNotExist:
                sent_doc.translation_type = None
            user_profile.tel = tel
            sent_doc.tel = tel
            user.email = email
            sent_doc.email = email
            user.first_name = name
            sent_doc.name = name
            sent_doc.text = text_doc_send
            r = re.compile(r'[{}]'.format(punctuation))
            text_str = r.sub(' ', text_doc_send)
            text_qnt = len(text_str.split())

            sent_doc.text_qnt = text_qnt
            user.save()
            user_profile.save()

        if request.POST.get('trans_from'):
            trans_from = request.POST.get('trans_from')
            trans_from_inst = Language.objects.get(name=trans_from)
        else:
            trans_from = None
            trans_from_inst = None
        if request.POST.get('trans_to'):
            trans_to = request.POST.get('trans_to')
            trans_to_inst = Language.objects.get(name=trans_to)
        else:
            trans_to = None
            trans_to_inst = None
        price = request.POST.get('order_price')
        # calc_sent_date = request.POST.get('calc_sent_date')
        # print(text_doc_send)
        sent_doc.status = OrderStatus.objects.get(name=u'В работе')
        translation_sent_date = request.POST.get('translation_sent_date')
        sent_doc.translation_sent_date = translation_sent_date
        # sent_doc.calc_sent_date = calc_sent_date
        if price:
            sent_doc.price = price
            sent_doc.paystatus = PayStatus.objects.get(name='Price determined')
        else:
            sent_doc.price = None
            sent_doc.paystatus = None
        sent_doc.trans_to = trans_to_inst
        sent_doc.trans_from = trans_from_inst
        sent_doc.save()
        # print(user_id + ' ' + order_id)
        # json_data = json.loads(request.body.decode('utf-8'))
        # file_id = json_data['file_id']
        return HttpResponse()


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def update_order_payment(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        sent_doc = SentDoc.objects.get(id=order_id)
        if sent_doc.status.name != u'Выполнен':
            sent_doc.status = OrderStatus.objects.get(name=u'В работе')
        payment_amount = request.POST.get('paid_amount')
        if payment_amount:
            sent_doc.paystatus = PayStatus.objects.get(name='Paid')
        payment_date = request.POST.get('payment_date')
        payment_method = request.POST.get('payment_method_')
        if not ',' in payment_date:
            parsed_datetime = parse_date_as_datetime(payment_date)
            sent_doc.payment_date = parse_datetime(parsed_datetime)

        sent_doc.payment_amount = payment_amount
        # logger.debug('date = ' + str(parsed_datetime))

        # print(str(payment_date) + str(payment_method) + str(payment_amount))
        sent_doc.paymethod = PayMethod.objects.get(name=payment_method)
        # logger.debug('method = ' + str(payment_method).decode('utf-8'))
        update_client_statistics(sent_doc.user)
        sent_doc.save()
        return HttpResponse('')


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def update_order_translation(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        sent_doc = SentDoc.objects.get(id=order_id)
        sent_doc.status = OrderStatus.objects.get(name=u'Выполнен')
        translation_sent_date = request.POST.get('translation_sent_date')
        sent_doc.translation_sent_date = translation_sent_date
        sent_doc.save()
        update_client_statistics(User.objects.get(id=sent_doc.user.id))
        # orders_complete = SentDoc.objects.filter(status=OrderStatus.objects.get(name='Выполнен')).filter(
        # resp=request.user).count()
        update_manager_statistics(User.objects.get(id=sent_doc.resp_id))
        return HttpResponse()


# @login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
# def create_translator(request):
#     if request.method == 'POST':
#         data = request.POST
#         if data['new_translator'] == 'no':
#             translator = Translator.objects.get(id=data['translator_id'])
#             print(data['translator_id'])
#             user = User.objects.get(id=translator.user.id)
#         else:
#             translator = Translator()
#             user = User()
#             password = User.objects.make_random_password()
#             user.set_password(password)
#             translator.init_password = password
#
#         name = request.POST.get('name_translator')
#         email = request.POST.get('email_translator')
#         tel = request.POST.get('tel_translator')
#         new = request.POST.get('new_translator')
#         birthday = request.POST.get('birthday')
#         if new == 'no':
#             translator.changed_by = request.user
#         else:
#             translator.creator = request.user
#         translator.name = name
#         user.first_name = name
#         translator.email = email
#         user.email = email
#         user.username = email
#         user.save()
#         translator.user = user
#         translator.tel = tel
#         translator.date_birth = birthday
#
#         translator.save()
#         Translator_Lang.objects.filter(translator=translator).delete()
#
#         for item in data:
#             if 'lang_' in item:
#                 language = Language.objects.get(name=request.POST.get(item))
#
#                 langs_inst = Translator_Lang()
#
#                 langs_inst.translator = translator
#                 langs_inst.user = request.user
#                 langs_inst.lang = language
#                 langs_inst.save()
#         if data['new_translator'] == 'yes':
#             return HttpResponse(translator.id)
#         else:
#             return HttpResponse('ok')
#
#     langs = Language.objects.all()
#     context = get_data_proc(request)
#     context.update({
#         'langs': langs,
#
#     })
#     return render(request, 'translator_new.html', context)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def create_manager(request):
    context = get_data_proc(request)

    if request.method == 'POST':
        data = request.POST
        name = request.POST.get('name_manager')
        email = request.POST.get('email_manager')
        tel = request.POST.get('tel_manager')
        new = request.POST.get('new_manager')
        birthday = request.POST.get('birthday')
        payment_method = request.POST.get('payment_method')
        payment_details = request.POST.get('payment_details')

        if data['new_manager'] == 'no':
            manager = Manager.objects.get(id=data['manager_id'])
            user = User.objects.get(id=manager.user.id)
            user_profile = UserProfile.objects.get(user=user)
            try:
                payment_details_inst = PaymentDetails.objects.get(owner=user)
            except PaymentDetails.DoesNotExist:
                if payment_details:
                    payment_details_inst = PaymentDetails()
        else:
            try:
                user = User.objects.get(username=email)
                return HttpResponse('user exists')
            except User.DoesNotExist:
                manager = Manager()
                user = User()
                user_profile = UserProfile()
                password = User.objects.make_random_password()
                user.set_password(password)
                manager.init_password = password
                # payment_details_inst = PaymentDetails()

        user_profile.role = Role.objects.get(role_name=u'Менеджер')
        manager.name = name
        user.first_name = name
        manager.email = email
        user.email = email
        user.username = email
        user.save()
        user_profile.user = user
        if new == 'no':
            manager.changed_by = request.user
            if payment_details:
                payment_details_inst.payment_method = PayMethod.objects.get(name=payment_method)
                payment_details_inst.owner = user
                payment_details_inst.detail = payment_details
                payment_details_inst.author = request.user
                payment_details_inst.save()
                manager.payment_details = payment_details_inst

        else:
            manager.creator = request.user

        manager.user = user
        manager.tel = tel
        manager.date_birth = birthday

        manager.save()
        user_profile.save()
        if data['new_manager'] == 'yes':
            return HttpResponse(manager.id)
        else:
            return HttpResponse('ok')
    # context.update({
    #     'payment_details': payment_details_inst,
    # })

    return render(request, 'manager_new.html', context)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def get_managers_list(request):
    managers = Manager.objects.all()
    context = get_data_proc(request)
    # orders = SentDoc.objects.
    context.update({
        'managers': managers
    })
    return render(request, 'managers_list.html', context)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def get_manager_details(request, manager_id):
    # if Role.objects.get(role_name=UserProfile.objects.get(user=request.user).role.role_name) == 'Суперадмин':
    #     sent_docs = SentDoc.objects.filter(resp=request.user)
    manager = Manager.objects.get(id=manager_id)
    payment_methods = PayMethod.objects.all()
    orders = SentDoc.objects.filter(resp=User.objects.get(id=manager.user.id))
    context = get_data_proc(request)
    author_role = UserProfile.objects.get(user=manager.creator.id).role.role_name
    author = UserProfile.objects.get(user=manager.creator.id)
    context.update({
        'manager': manager,
        'sent_docs': orders,
        'payment_methods': payment_methods,
        'author': author,
        'author_role': author_role

    })
    return render(request, 'manager_details.html', context)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def get_manager_complete_orders(request, manager_id):
    # if Role.objects.get(role_name=UserProfile.objects.get(user=request.user).role.role_name) == 'Суперадмин':
    #     sent_docs = SentDoc.objects.filter(resp=request.user)
    manager = Manager.objects.get(id=manager_id)
    payment_methods = PayMethod.objects.all()
    orders = SentDoc.objects.filter(resp=User.objects.get(id=manager.user.id)).filter(
        status=OrderStatus.objects.get(name=u'Выполнен'))
    # print(translator.name)
    context = get_data_proc(request)
    context.update({
        'manager': manager,
        'sent_docs': orders,
        'payment_methods': payment_methods,
        'orders_label': True

    })
    return render(request, 'manager_details.html', context)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def delete_manager(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        manager_id = json_data['manager_id']
        Manager.objects.get(id=manager_id).delete()
        # return redirect('ru:dashboard_ru:get_translators_list')
        return HttpResponse('ok')


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def save_manager_photo(request, manager_id):
    if request.method == 'POST':
        files = request.FILES.getlist('photo')
        manager = Manager.objects.get(id=manager_id)
        # translator_id = json_data['translator_id']
        # photo = Translator.photo()
        # print(translator_id)
        for file in files:
            manager.photo = file
            manager.photo_name = file.name
        manager.save()
        print(manager.photo.name)
        return HttpResponse(manager.photo_name)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def create_admin(request):
    if request.method == 'POST':
        data = request.POST
        if data['new_admin'] == 'no':
            admin = Admin.objects.get(id=data['admin_id'])
            user = User.objects.get(id=admin.user.id)
            user_profile = UserProfile.objects.get(user=user)
        else:
            admin = Admin()
            user = User()
            user_profile = UserProfile()
            password = User.objects.make_random_password()
            user.set_password(password)
            admin.init_password = password

        name = request.POST.get('name_admin')
        email = request.POST.get('email_admin')
        tel = request.POST.get('tel_admin')
        new = request.POST.get('new_admin')
        birthday = request.POST.get('birthday')
        if new == 'no':
            admin.changed_by = request.user
        else:
            admin.creator = request.user
        user_profile.role = Role.objects.get(role_name='Админ')
        admin.name = name
        user.first_name = name
        admin.email = email
        user.email = email
        user.username = email
        user.save()
        user_profile.user = user

        admin.user = user
        admin.tel = tel
        admin.date_birth = birthday

        admin.save()
        user_profile.save()
        if data['new_admin'] == 'yes':
            return HttpResponse(admin.id)
        else:
            return HttpResponse('ok')

    context = get_data_proc(request)
    context.update({
        # 'langs': langs,

    })
    return render(request, 'admin_new.html', context)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def get_admins_list(request):
    admins = Admin.objects.all()

    context = get_data_proc(request)
    context.update({
        'admins': admins
    })
    return render(request, 'admins_list.html', context)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def get_admin_details(request, admin_id):
    admin = Admin.objects.get(id=admin_id)
    creator_role = Role.objects.get(id=admin.creator.id)
    # print(translator.name)
    context = get_data_proc(request)
    context.update({
        'admin': admin,
        'creator_role': creator_role
    })
    return render(request, 'admin_details.html', context)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def delete_admin(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        admin_id = json_data['admin_id']
        Admin.objects.get(id=admin_id).delete()
        # return redirect('ru:dashboard_ru:get_translators_list')
        return HttpResponse('ok')


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def save_admin_photo(request, admin_id):
    if request.method == 'POST':
        files = request.FILES.getlist('photo')
        admin = Admin.objects.get(id=admin_id)
        # translator_id = json_data['translator_id']
        # photo = Translator.photo()
        # print(translator_id)
        for file in files:
            admin.photo = file
            file_path = file.name
        admin.save()
        return HttpResponse(admin.photo.name)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def create_client(request):
    if request.method == 'POST':
        data = request.POST
        if data['new_client'] == 'no':
            client = Client.objects.get(id=data['client_id'])
            user = User.objects.get(id=client.user.id)
            user_profile = UserProfile.objects.get(user=user)
        else:
            client = Client()
            user = User()
            user_profile = UserProfile()
            password = User.objects.make_random_password()
            user.set_password(password)
            client.init_password = password

        name = request.POST.get('name_client')
        email = request.POST.get('email_client')
        tel = request.POST.get('tel_client')
        new = request.POST.get('new_client')
        birthday = request.POST.get('birthday')
        if new == 'no':
            client.changed_by = request.user
        else:
            client.creator = request.user
        user_profile.role = Role.objects.get(role_name='Клиент')
        client.name = name
        user.first_name = name
        client.email = email
        user.email = email
        user.username = email
        user.save()
        user_profile.user = user

        client.user = user
        client.tel = tel
        client.date_birth = birthday

        client.save()
        user_profile.save()
        if data['new_client'] == 'yes':
            return HttpResponse(client.id)
        else:
            return HttpResponse('ok')

    context = get_data_proc(request)
    context.update({
        # 'langs': langs,

    })
    return render(request, 'client_new.html', context)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def delete_client(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        client_id = json_data['client_id']
        Client.objects.get(id=client_id).delete()
        # return redirect('ru:dashboard_ru:get_translators_list')
        return HttpResponse('ok')


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def get_clients_list(request):
    clients = Client.objects.all()
    context = get_data_proc(request)
    context.update({
        'clients': clients
    })
    return render(request, 'clients_list.html', context)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def get_client_details(request, client_id):
    client = Client.objects.get(id=client_id)
    creator_role = UserProfile.objects.get(user=client.creator).role
    sent_docs = SentDoc.objects.filter(user=client.user)
    context = get_data_proc(request)
    context.update({
        'client': client,
        'creator_role': creator_role,
        'sent_docs': sent_docs
    })
    return render(request, 'client_details.html', context)


# @login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
# def client_admin(request):
#     if request.method == 'POST':
#         json_data = json.loads(request.body.decode('utf-8'))
#         client_id = json_data['client_id']
#         Client.objects.get(id=client_id).delete()
#         # return redirect('ru:dashboard_ru:get_translators_list')
#         return HttpResponse('ok')


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def save_client_photo(request, client_id):
    if request.method == 'POST':
        files = request.FILES.getlist('photo')
        client = Client.objects.get(id=client_id)
        # translator_id = json_data['translator_id']
        # photo = Translator.photo()
        # print(translator_id)
        for file in files:
            client.photo = file
            file_path = file.name
        client.save()
        return HttpResponse(client.photo.name)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def save_order_comment(request):
    if request.method == 'POST':
        if request.POST.get('back_call_id'):
            back_call_id = request.POST.get('back_call_id')
            text = request.POST.get('formated_text')
            # print(comment)
            comment_inst = BackCallComments()
            comment_inst.comment = text
            comment_inst.author = request.user
            comment_inst.back_call = BackCall.objects.get(id=back_call_id)
            comment_inst.author_role = Role.objects.get(id=UserProfile.objects.get(user=request.user).role.id)
            comment_inst.save()
            role = UserProfile.objects.get(user=request.user).role.role_name
        else:
            comment = request.POST.get('comment_text')
            order_id = request.POST.get('order_id')
            order = SentDoc.objects.get(id=order_id)
            comment_inst = OrderComments()
            comment_inst.comment = comment
            comment_inst.author = request.user
            comment_inst.order = order
            comment_inst.author_role = Role.objects.get(id=UserProfile.objects.get(user=request.user).role.id)
            comment_inst.save()
            order.comments = True
            order.save()
            role = UserProfile.objects.get(user=request.user).role.role_name
            # context = {
            #     'date': comment_inst.added.isoformat(),
            #     'comment': comment_inst.comment,
            #     'author': request.user
            # }
        return HttpResponse(json.dumps(
            {'date': comment_inst.added.strftime("%d.%m.%Y, %H:%M"), 'comment': comment_inst.comment,
             'author_firstname': request.user.first_name, 'author_lastname': request.user.last_name, 'role': role}))


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def save_order_comment_client(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        comment_text = request.POST.get('formated_text')
        comment_id = request.POST.get('comment_id')
        context = {}
        if comment_id:
            comment = OrderCommentsClientsAnswer()
            comment.comment = OrderCommentsClients.objects.get(id=comment_id)
            user = User.objects.get(id=request.user.id)
            comment.author = user
            user_profile = UserProfile.objects.get(user=user)
            comment.author_role = user_profile.role
            comment.comment.done = True
            comment.comment.save()
            context.update({
                'user_name': user.first_name,
                'role': user_profile.role.role_name
            })
            answer = 1
        else:
            comment = OrderCommentsClients()
            answer = 0
        order = SentDoc.objects.get(id=order_id)
        comment.text = comment_text
        comment.order = order
        comment.save()
        context.update({
            'added': comment.added.strftime("%d.%m.%Y, %H:%M"),
            'comment_text': comment.text,
            'answer': answer,
            'comment_id': comment_id,
            })
        response = json.dumps(context)
        return HttpResponse(response)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def save_order_comment_client_answer(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        comment_id = request.POST.get('comment_client_id')
        answer_text = request.POST.get('comment_client_answer_text')
        comment = OrderCommentsClients.objects.get(id=comment_id)
        order = SentDoc.objects.get(id=order_id)
        answer = OrderCommentsClientsAnswer()
        answer.text = answer_text
        answer.order = order
        user = User.objects.get(id=request.user.id)
        answer.author = user
        user_profile = UserProfile.objects.get(user=user)
        answer.author_role = user_profile.role
        answer.comment = comment
        answer.save()
        response = json.dumps(
            {'added': comment.added.strftime("%d.%m.%Y, %H:%M"),
             'comment_text': answer.text,
             'author_role': answer.author_role.role_name
             })
        return HttpResponse(response)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def help_dashboard(request):
    context = get_data_proc(request)
    # context.update({
    #     'clients': clients
    # })
    return render(request, 'help.html', context)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def get_back_calls(request):
    back_calls = None
    if UserProfile.objects.get(user=request.user).role.role_name == u'Суперадмин' or UserProfile.objects.get(
            user=request.user).role.role_name == u'Админ':
        back_calls = BackCall.objects.all()
    context = get_data_proc(request)
    context.update({
        'back_calls': back_calls,
    })
    return render(request, 'back_calls.html', context)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def get_new_back_calls(request):
    back_calls = None
    if UserProfile.objects.get(user=request.user).role.role_name == u'Суперадмин' or UserProfile.objects.get(
            user=request.user).role.role_name == u'Админ':
        back_calls = BackCall.objects.filter(new=True)
    context = get_data_proc(request)
    context.update({
        'back_calls': back_calls,
    })
    return render(request, 'back_calls.html', context)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def get_back_call_details(request, back_call_id):
    if UserProfile.objects.get(user=request.user).role.role_name == u'Суперадмин' or UserProfile.objects.get(
            user=request.user).role.role_name == u'Админ':
        back_call = BackCall.objects.get(id=back_call_id)
        back_call.new = False
        back_call.viewed_by = request.user
        back_call.save()
        back_call_comments = BackCallComments.objects.filter(back_call=back_call)
        print(back_call_id)
    context = get_data_proc(request)
    context.update({
        'back_call': back_call,
        'back_call_comments': back_call_comments
    })
    return render(request, 'back_call_details.html', context)


def send_email(request, template, from_, to, context):
    curr_path = os.path.dirname(__file__)
    file_path = os.path.join(os.path.join(curr_path, '..'), 'static/img/logo/logo_vert_35.png')
    with open(file_path, 'rb') as logo:
        logo_img = logo.read()
    logo = InlineImage(filename='logo', content=logo_img)
    context.update({'logo': logo})
    # logger.debug(template + ' ' + from_ + ' ' + context)
    send_templated_mail(template_name=template,
                        from_email=from_,
                        recipient_list=to,
                        context=context,
                        )
    return HttpResponse()


def send_email_test(request):
    template = 'calculation.html'
    from_ = 'info@prolingva.ru'
    to = ['bomvendador@yandex.ru', 'orders@prolingva.ru']
    json_data = json.loads(request.body.decode('utf-8'))
    order_id = json_data['order_id']
    order_price = json_data['order_price']
    order = SentDoc.objects.get(id=order_id)
    manager = User.objects.get(id=order.resp_id)
    context = {'order': order,
               'manager': manager,
               'order_price': order_price
             }
    curr_path = os.path.dirname(__file__)
    file_path = os.path.join(os.path.join(curr_path, '..'), 'static/img/logo/logo_vert_30.png')
    with open(file_path, 'rb') as logo:
        logo_img = logo.read()
    logo = InlineImage(filename='logo', content=logo_img)
    context.update({'logo': logo})
    # logger.debug(template + ' ' + from_ + ' ' + context)
    send_templated_mail(template_name=template,
                        from_email=from_,
                        recipient_list=to,
                        context=context,
                        )
    return HttpResponse()


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def send_calculation_to_client(request):
    if request.method == 'POST':
        logger.debug('start = ')

        json_data = json.loads(request.body.decode('utf-8'))
        order_id = json_data['order_id']
        order_price = json_data['order_price']
        order = SentDoc.objects.get(id=order_id)
        order.calc_sent_date = datetime.datetime.now()
        order.save()
        manager = User.objects.get(id=order.resp_id)
        email_context = {'order': order,
                         'manager': manager,
                         'order_price': order_price
                         }
        # TODO изменить адрес отправки
        # send_email(request, 'calculation.html', 'info@prolingva.ru', [order.user.email], email_context)
        send_email(request, 'calculation.html', 'info@prolingva.ru', ['orders@prolingva.ru', 'bomvendador@yandex.ru'], email_context)
        logger.debug('id = ' + str(order_id))
        logger.debug('price = ' + order.calc_sent_date.strftime("%d.%m.%Y, %H:%M"))
        return HttpResponse(order.calc_sent_date.strftime("%d.%m.%Y, %H:%M"))


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def send_trans_files_to_client(request):
    if request.method == 'POST':
        logger.debug('start = ')

        json_data = json.loads(request.body.decode('utf-8'))
        order_id = json_data['order_id']
        order = SentDoc.objects.get(id=order_id)
        order.translation_sent_date = datetime.datetime.now()
        order.save()
        manager = User.objects.get(id=order.resp_id)
        email_context = {'order': order,
                         'manager': manager,
                         }
        # TODO изменить адрес отправки
        # send_email(request, 'calculation.html', 'info@prolingva.ru', [order.user.email], email_context)
        send_email(request, 'translation_is_ready.html', 'info@prolingva.ru', ['orders@prolingva.ru', 'bomvendador@yandex.ru'], email_context)
        # logger.debug('id = ' + str(order_id))
        # logger.debug('price = ' + order.calc_sent_date.strftime("%d.%m.%Y, %H:%M"))
        return HttpResponse(order.translation_sent_date.strftime("%d.%m.%Y, %H:%M"))


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def testimonial(request, testimonial_id):
    context = get_data_proc(request)
    testimonial_ = Testimonials.objects.get(id=testimonial_id)
    context.update({
        'testimonial': testimonial_
    })
    return render(request, 'testimonial_details.html', context)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def save_testimonial(request):
    if request.method == 'POST':
        name = request.POST.get('name_testimonial', None)
        company = request.POST.get('company_testimonial', None)
        text = request.POST.get('text_testimonial', None)
        approved = request.POST.get('approved', None)
        logger.debug('appr = ' + str(approved))
        new_testimonial = request.POST.get('new_testimonial', None)
        testimonial_id = request.POST.get('testimonial_id', None)
        if new_testimonial == 'yes':
            testimonial_inst = Testimonials()
        else:
            testimonial_inst = Testimonials.objects.get(id=testimonial_id)
        if approved == '1':
            testimonial_inst.is_approved = True
        else:
            testimonial_inst.is_approved = False
        try:
            userprofile = UserProfile.objects.get(user=request.user)
            if userprofile.role.role_name != u'Суперадмин' or userprofile.role.role_name != u'Админ':
                testimonial_inst.new = False
            else:
                testimonial_inst.new = True
        except UserProfile.DoesNotExist:
            testimonial_inst.new = True
        testimonial_inst.name = name
        testimonial_inst.company = company
        testimonial_inst.text = text
        testimonial_inst.save()
        # if request.method == 'POST':
        return HttpResponse('ok')


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def add_testimonial(request):
    context = get_data_proc(request)
    context.update({
        'new': 1
    })
    return render(request, 'testimonial_details.html', context)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def companies_list(request):
    context = get_data_proc(request)
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.role.role_name == u'Клиент':
        companies = Company.objects.filter(user=request.user)
    else:
        companies = Company.objects.all()
    context.update({
        'companies': companies,
    })
    return render(request, 'companies_list.html', context)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def company(request, company_id):
    context = get_data_proc(request)
    company_ = Company.objects.get(id=company_id)
    properties = Property.objects.all()
    context.update({
        'company': company_,
        'properties': properties,
    })
    return render(request, 'company_details.html', context)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def add_company(request):
    context = get_data_proc(request)
    properties = Property.objects.all()
    clients = Client.objects.all()

    context.update({
        'new': 1,
        'properties': properties,
        'clients': clients

    })
    return render(request, 'company_details.html', context)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def save_company(request):
    if request.method == 'POST':
        name = request.POST.get('name_company', None)
        property_id = request.POST.get('property', None)
        inn = request.POST.get('inn_company', None)
        kpp = request.POST.get('kpp_company', None)
        ogrn = request.POST.get('ogrn_company', None)
        address = request.POST.get('address_company', None)
        new = request.POST.get('new', None)
        client_id = request.POST.get('client_id', None)
        company_id = request.POST.get('company_id', None)
        property_inst = Property.objects.get(id=property_id)
        if new == 'yes':
            company_inst = Company()
        else:
            company_inst = Company.objects.get(id=company_id)
        if client_id:
            company_inst.user = User.objects.get(id=Client.objects.get(id=client_id).user.id)
        else:
            company_inst.user = request.user
        company_inst.name = name
        company_inst.property = property_inst
        company_inst.inn = inn
        company_inst.kpp = kpp
        company_inst.ogrn = ogrn
        company_inst.address = address
        company_inst.save()
        # if request.method == 'POST':
        return HttpResponse('ok')


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def set_company_for_payment(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        order_id = json_data['order_id']
        company_id = json_data['company_id']
        order_inst = SentDoc.objects.get(id=order_id)
        company_inst = Company.objects.get(id=company_id)
        order_inst.company = company_inst
        order_inst.save()
        orders_qnt = SentDoc.objects.filter(company=company_inst).count()
        company_inst.orders_qnt = orders_qnt
        company_inst.save()
        invoice = Invoice()
        invoice.order = order_inst
        invoice.save()
        email_context_ = {
            'order': order_inst,
            'company': company_inst
        }
        send_email(request, 'invoice_request.html', 'info@prolingva.ru', ['invoices@prolingva.ru'], email_context_)
        name = company_inst.property.short_name + ' "' + company_inst.name + '"'
        company_id = company_inst.id
        response = json.dumps({
            'name': name,
            'company_id': company_id
        })
        return HttpResponse(response)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def del_company_from_payment(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        order_id = json_data['order_id']
        company_id = json_data['company_id']
        logger.debug('company id=' + str(company_id))
        company_inst = Company.objects.get(id=company_id)
        order_inst = SentDoc.objects.get(id=order_id)
        order_inst.company = None
        order_inst.save()
        orders_qnt = SentDoc.objects.filter(company=company_inst).count()
        company_inst.orders_qnt = orders_qnt
        company_inst.save()

        Invoice.objects.filter(order=order_inst).delete()
        email_context = {
            'order': order_inst
        }
        send_email(request, 'invoice_request.html', 'info@prolingva.ru', ['invoices@prolingva.ru'], email_context)
        return HttpResponse('ok')
