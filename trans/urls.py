"""trans URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from ru import views
from trans import payments, views as trans_views


# urlpatterns = i18n_patterns('',
#     url(r'^admin/', admin.site.urls),
#     url(r'^ru/', include('ru.urls')),
# )
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^payment_success', payments.payment_success, name='payment_success'),
    url(r'^payment_failure', payments.payment_failure, name='payment_failure'),
    url(r'^ru/', include('ru.urls', namespace='ru')),
    # url(r'^paymaster/', include('paymaster.urls', namespace='paymaster')),
    url(r'^ws', trans_views.user_list, name='user_list'),

]

