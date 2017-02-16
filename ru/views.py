#-*- encoding:utf-8-*-
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.models import User
from .models import Language, SentDoc, SentFiles, UserProfile, Role, OrderStatus, OrderSource, Client, TranslationTheme, TranslationType, BackCall, Testimonials
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
import hashlib
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import re
from string import punctuation
from dashboard_ru.views import update_client_statistics
from dashboard_ru import views as dash_views

from django.contrib.auth.decorators import login_required

import logging
logger = logging.getLogger('django-debug')


class IndexView (generic.TemplateView):
    template_name = 'index.html'
    context_object_name = 'user'

    def get_queryset(self):
        return User.objects.all()

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        username = context['login']
        password = context['password']
        # print('login' + str(login) + ' pass = ' + password)

        user = authenticate(username=username, password=password)
        if user is not None:
            print(user.username)

            if user.is_active:
                login(request, user)
                return redirect('ru:index')
        else:
            # messages.error(self.request, 'fdfdfd')

            message_ = u'Логин или пароль указаны не верно'
            return HttpResponse(message_)
                # return render(self.request, 'index.html', {'user': user})
        return render(self.request, 'index.html', {'user': User.objects.all()})
        # return super(generic.TemplateView, self).render_to_response(context)

    def get_context_data(self, **kwargs):
        # context = super(IndexView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            try:
                user_profile = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                user_profile = None
        else:
            user_profile = None
        context = {'login': self.request.POST.get('login'),
                   'password': self.request.POST.get('password'),
                   'langs': Language.objects.all().order_by('name'),
                   'user_profile': user_profile,
                   'testimonials': Testimonials.objects.all()
                   }
        # print(self.request.POST.get('login'))
        return context


class BaseView (generic.TemplateView):
    template_name = 'base.html'
    context_object_name = 'user'

    def get_queryset(self):
        return {'user': User.objects.all(), 'lang': Language.objects.all().order_by('name')}


def baseView (request):
    context = {'user': User.objects.all(),
               'langs': Language.objects.all().order_by('name')
               }
    return render(request, 'base.html', context)


def loginUser(request):
    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['password']
        print(login + '  ' + password)
        user = authenticate(username=login, password=password)
        if user is not None:
            print(user.username)

            if user.is_active:
                login(request, user)
                return redirect('ru:index')

        return render(request, 'index.html')


def logout_user(request):
    if request.user is not None:
        logout(request)
        return redirect('ru:index')


def check_user(request):
    if request.method == 'POST':

        email = request.POST['email']
        password = request.POST['password']
        print('before')
        # user_ = User.objects.get(email=email)

        user = authenticate(username=email, password=password)
        # print('username = ' + str(user_.username) + ' ddd = ' + str(user))

        if user is not None:
            print('user')

            if user.is_active:
                login(request, user)
                error_ = 0
                return HttpResponse(error_)
        else:
            # messages.error(self.request, 'fdfdfd')

            error_ = 1
            return HttpResponse(error_)


def reg_user(request):
    print(request)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        try:
            user_exist = User.objects.get(username=email)
        except User.DoesNotExist:
            user_exist = None
        if user_exist is None:
            user_profile = UserProfile()
            user = User()
            user.username = email
            user.set_password(password)
            user.first_name = name
            user.email = email
            user.save()
            if request.POST.get('role', False) == u'Клиент':
                client = Client()
                client.user = user
                client.creator = user
                client.name = name
                client.email = email
                client.visited_times = 1
                client.save()
                user_profile.role = Role.objects.get(role_name=request.POST['role'])
                email_context = {'user': user, 'login': email, 'password': password}
                dash_views.send_email(request, 'welcome.html', 'info@prolingva.ru', [email], email_context)
            # else:
            #     user_profile.role = Role.objects.get(id=3)
            # user = User.objects.create(username=email, email=email, password=password, first_name=name)

            user_profile.user = user
            user_profile.tel = request.POST.get('tel', False)

            user_profile.save()
            # hashed_password = hashlib.md5(password)
            user_auth = authenticate(username=email, password=password)
            login(request, user_auth)
            message = user.id
        else:
            message = 'user_exists'
        return HttpResponse(message)


# class Base_view_ (generic.TemplateView):
#     template_name = 'base_board.html'


def base_view_(request):
    print('fff')
    return render(request, 'base_board.html')


def get_langs(request):
    langs = Language.objects.all().order_by('name')
    return HttpResponse(langs)


def user_client_add(name, email, tel):
    user = User()
    user.first_name = name
    user.email = email
    user.username = email
    password = User.objects.make_random_password()
    print(password)
    user.set_password(password)
    user.save()

    client = Client()
    client.name = name
    client.email = email
    client.tel = tel
    client.init_password = password
    client.user = user
    client.creator = user
    client.save()

    user_profile = UserProfile()
    user_profile.tel = tel
    user_profile.user = user
    user_profile.role = Role.objects.get(role_name=u'Клиент')
    user_profile.save()
    return {'user': user, 'client': client, 'user_profile': user_profile}


def save_files_trans(request):
    if request.method == 'POST':
        email_source = u'Сайт - заявка'
        data = request.POST
        user_exists = False
        doc_sent = SentDoc()
        if data.get('contact_form_footer'):
            name = request.POST['name_contact_form_footer']
            email = request.POST['email_contact_form_footer']
            try:
                # id = request.POST['tel_doc_send']
                client = Client.objects.get(email=email)
                user = User.objects.get(id=client.user.id)
                message = 'user_exists'

            except Client.DoesNotExist:
                user = user_client_add(name, email, '')['user']

                message = 'ok'
            doc_sent.author = user
            doc_sent.email = email
            doc_sent.user = user
            doc_sent.name = name
            doc_sent.contact_form_message = data['message_contact_form_footer']
            doc_sent.status = OrderStatus.objects.get(name=u'Новый')
            doc_sent.order_src = OrderSource.objects.get(name=u'Сайт - футер')
            doc_sent.text = ''
            doc_sent.save()
            update_client_statistics(user)
            email_context = {'client': name, 'email': email, 'type': u'Сайт - футер', 'message': data[
                'message_contact_form_footer']}
            dash_views.send_email(request, 'orders.html', 'info@prolingva.ru', ['orders@prolingva.ru'], email_context)

            return HttpResponse(message)

        if request.POST.get('back_call'):
            print('call')
            name = request.POST['name_back_call_form']
            tel = request.POST['tel_back_call_form']
            back_call = BackCall()
            back_call.tel = tel
            back_call.name = name
            back_call.save()
            email_context = {'client': name, 'type': u'Обратный звонок', 'tel': tel}
            dash_views.send_email(request, 'orders.html', 'info@prolingva.ru', ['orders@prolingva.ru'], email_context)

            return HttpResponse('ok')

        if request.POST.get('learn_more'):
            short_name_theme = ''
            short_name_type = ''
            if data['learn_more'] == 'trans_official_docs':
                short_name_theme = 'official'
            if data['learn_more'] == 'trans_medic':
                short_name_theme = 'medic'
            if data['learn_more'] == 'trans_custom':
                short_name_theme = 'custom'
            if data['learn_more'] == 'trans_tech':
                short_name_theme = 'technical'
            if data['learn_more'] == 'trans_www':
                short_name_theme = 'www'
            if data['learn_more'] == 'trans_economic':
                short_name_theme = 'economic'
            if data['learn_more'] == 'type_written':
                short_name_type = 'written'
            if data['learn_more'] == 'type_spoken':
                short_name_type = 'spoken'
            if data['learn_more'] == 'type_video':
                short_name_type = 'video'

            name = request.POST['name_contact_form']
            email = request.POST['email_contact_form']
            tel = request.POST['tel_contact_form']
            text = request.POST['text_contact_form']
            try:
                # id = request.POST['tel_doc_send']
                client = Client.objects.get(email=email)
                user = User.objects.get(id=client.user.id)
                message = 'user_exists'

            except Client.DoesNotExist:
                user = user_client_add(name, email, tel)['user']
                message = 'ok'
            doc_sent.author = user
            doc_sent.email = email
            doc_sent.user = user
            doc_sent.name = name
            doc_sent.tel = tel
            doc_sent.contact_form_message = data['text_contact_form']
            doc_sent.status = OrderStatus.objects.get(name=u'Новый')
            doc_sent.order_src = OrderSource.objects.get(name=u'Сайт')

            if short_name_type:
                doc_sent.translation_type = TranslationType.objects.get(short_name=short_name_type)
                email_context = {'client': name, 'type': u'Заказ услуги', 'email': email, 'tel': tel, 'order_type': short_name_type, 'message': data['text_contact_form']}
            if short_name_theme:
                email_context = {'client': name, 'type': u'Заказ услуги', 'email': email, 'tel': tel, 'order_theme': short_name_theme,
                                 'message': data['text_contact_form']}
                doc_sent.translation_theme = TranslationTheme.objects.get(short_name=short_name_theme)
            doc_sent.text = ''
            doc_sent.save()

            dash_views.send_email(request, 'orders.html', 'info@prolingva.ru', ['orders@prolingva.ru'], email_context)
            return HttpResponse(message)
        else:
            if not request.user.is_anonymous():
                user_profile = UserProfile.objects.get(user=request.user)
                doc_sent.author = request.user

                if user_profile.role.role_name != u'Клиент':

                    name = request.POST['name_doc_send']
                    email = request.POST['email_doc_send']
                    tel = request.POST['tel_doc_send']
                    # if request.POST['client_id_doc_send']:
                    #     client_by_id = Client.objects.get(id=request.POST['client_id_doc_send'])
                    #     user_exists = True
                    #     user = User.objects.get(id=client.user.id)
                    # else:
                    #
                    #     user = User()
                    #     user.first_name = name
                    #     user.email = email
                    #     user.username = email
                    #     password = User.objects.make_random_password()
                    #     print(password)
                    #     user.set_password(password)
                    #     user.save()
                    #
                    #     client = Client()
                    #     client.name = name
                    #     client.email = email
                    #     client.tel = tel
                    #     client.init_password = password
                    #     client.user = user
                    #     client.creator = request.user
                    #     client.save()
                    #
                    #     user_profile = UserProfile()
                    #     user_profile.tel = tel
                    #     user_profile.user = user
                    #     user_profile.role = Role.objects.get(role_name='Client')
                    #     user_profile.save()

                    try:
                        # id = request.POST['tel_doc_send']
                        client = Client.objects.get(email=email)
                        user_exists = True
                        user = User.objects.get(id=client.user.id)

                    except Client.DoesNotExist:
                        user = User()
                        user.first_name = name
                        user.email = email
                        user.username = email
                        password = User.objects.make_random_password()
                        print(password)
                        user.set_password(password)
                        user.save()

                        client = Client()
                        client.name = name
                        client.email = email
                        client.tel = tel
                        client.init_password = password
                        client.user = user
                        client.creator = request.user
                        client.save()

                        user_profile = UserProfile()
                        user_profile.tel = tel
                        user_profile.user = user
                        user_profile.role = Role.objects.get(role_name=u'Клиент')
                        user_profile.save()

                else:
                    user_exists = True

                    client = Client.objects.get(user=request.user)
                    name = client.name
                    email = client.email
                    tel = client.tel
                    user = User.objects.get(id=request.user.id)
            else:
                name = request.POST['name_doc_send']
                email = request.POST['email_doc_send']
                tel = request.POST['tel_doc_send']
                try:
                    # id = request.POST['tel_doc_send']
                    client = Client.objects.get(email=email)
                    user_exists = True
                    user = User.objects.get(id=client.user.id)

                except Client.DoesNotExist:
                    user = User()
                    user.first_name = name
                    user.email = email
                    user.username = email
                    password = User.objects.make_random_password()
                    print(password)
                    user.set_password(password)
                    user.save()

                    client = Client()
                    client.name = name
                    client.email = email
                    client.tel = tel
                    client.init_password = password
                    client.user = user
                    client.creator = user
                    client.save()

                    user_profile = UserProfile()
                    user_profile.tel = tel
                    user_profile.user = user
                    user_profile.role = Role.objects.get(role_name=u'Клиент')
                    user_profile.save()
                doc_sent.author = user
            text = request.POST['text_doc_send']
            if request.POST['trans_from']:
                try:
                    trans_from = Language.objects.get(name=request.POST['trans_from'])
                except Language.DoesNotExist:
                    trans_from = None
                doc_sent.trans_from = trans_from

            if request.POST['trans_to']:
                try:
                    trans_to = Language.objects.get(name=request.POST['trans_to'])
                except Language.DoesNotExist:
                    trans_to = None
                doc_sent.trans_to = trans_to

            doc_sent.email = email
            doc_sent.user = user
            doc_sent.name = name
            doc_sent.tel = tel
            doc_sent.text = text
            doc_sent.status = OrderStatus.objects.get(name=u'Новый')
            # doc_sent.author = request.user

            # file = SentFiles()

            r = re.compile(r'[{}]'.format(punctuation))
            text_str = r.sub(' ', text)
            text_qnt = len(text_str.split())
            doc_sent.text_qnt = text_qnt
            files_qnt = 0

            for f in request.FILES.getlist('filesToUpload'):
                files_qnt += 1
            if files_qnt > 0:
                doc_sent.files_qnt = files_qnt
            if request.user.is_authenticated():
                try:
                    user_profile = UserProfile.objects.get(user=request.user.id)
                    if user_profile.role.role_name != u'Клиент':
                        doc_sent.order_src = OrderSource.objects.get(name=u'Персонал')
                        email_source = u'Персонал'
                    else:
                        print('client')
                        if request.POST.get('order_source') == 'dashboard':
                            print('clientwww')
                            doc_sent.order_src = OrderSource.objects.get(name=u'Панель управления - Клиент')
                            email_source = u'Панель управления - Клиент'
                except UserProfile.DoesNotExist:
                    doc_sent.order_src = OrderSource.objects.get(name=u'Сайт')
                    email_source = u'Сайт - заявка'

            doc_sent.save()

            for f in request.FILES.getlist('filesToUpload'):
                s = SentFiles(file=f, sent_doc=doc_sent, file_name=f.name)
                s.save()
            if user_exists:
                message = 'user_exists'
            else:
                message = 'ok'

            email_context = {'client': name, 'email': email, 'type': email_source, 'ID': doc_sent.id, 'tel': tel}
            dash_views.send_email(request, 'orders.html', 'info@prolingva.ru', ['orders@prolingva.ru'], email_context)

            return HttpResponse(message)
    return HttpResponse()


def learn_more_trans(request):
    context = {
        'learn_more': 'trans',
        'langs': Language.objects.all().order_by('name'),

    }
    return render(request, 'learn_more_trans.html', context)


def learn_more_types(request):
    context = {
        'learn_more': 'types',
        'langs': Language.objects.all().order_by('name'),

    }
    return render(request, 'learn_more_trans.html', context)


def confidentiality(request):
    context = {'confidentiality': 'yes'}
    return render(request, 'confidentiality.html', context)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def get_testimonials_list(request):
    context = dash_views.get_data_proc(request)
    testimonials = Testimonials.objects.all()
    context.update(
        {
            'testimonials': testimonials

        })
    return render(request, 'testimonials_list.html', context)


@login_required(redirect_field_name=None, login_url='/ru/dashbrd/login')
def get_new_testimonials_list(request):
    context = dash_views.get_data_proc(request)
    testimonials = Testimonials.objects.filter(new=True)
    context.update(
        {
            'testimonials': testimonials

        })
    return render(request, 'testimonials_list.html', context)

