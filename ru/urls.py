from django.conf.urls import url, include
from django.contrib import admin
from . import views

app_name = 'ru'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^login/$', views.loginUser, name='loginUser'),
    url(r'^logout/$', views.logout_user, name='logoutUser'),
    url(r'^ckusr/$', views.check_user, name='check_user'),
    url(r'^reg/$', views.reg_user, name='reg_user'),
    url(r'^get_langs/$', views.get_langs, name='get_langs'),
    url(r'^send_docs/$', views.save_files_trans, name='save_files_trans'),
    url(r'^learn_more_trans/$', views.learn_more_trans, name='learn_more_trans'),
    url(r'^learn_more_types/$', views.learn_more_types, name='learn_more_types'),
    url(r'^confidentiality/$', views.confidentiality, name='confidentiality'),
    # url(r'^dashbrd/$', views.Base_view_.as_view(), name='base_board'),
    # url(r'^dashbrd/$', views.base_view_, name='base_board'),
    url(r'^dashbrd/', include('dashboard_ru.urls', namespace='dashboard_ru')),

]