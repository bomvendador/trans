from django.conf.urls import url
from django.contrib import admin
from . import views
from trans import payments
from ru import views as ru_views

app_name = 'dashboard_ru'

urlpatterns = [
    url(r'^(?P<user_id>\d+)/$', views.base_board, name='base_board'),
    url(r'^login/$', views.login_board, name='login_board'),
    url(r'^logout/$', views.logout_board, name='logout_board'),
    url(r'^help/$', views.help_dashboard, name='help_dashboard'),
    url(r'^sign_up/$', views.sign_up_board, name='sign_up_board'),

    url(r'^order_details/(?P<order_id>\d+)/$', views.order_details, name='order_details'),
    url(r'^sent_docs/$', views.get_sent_docs, name='get_sent_docs'),
    url(r'^back_calls/$', views.get_back_calls, name='get_back_calls'),
    url(r'^back_call_details/(?P<back_call_id>\d+)/$', views.get_back_call_details, name='get_back_call_details'),
    url(r'^save_order_comment/$', views.save_order_comment, name='save_order_comment'),
    url(r'^new_orders/$', views.get_new_sent_docs, name='get_new_orders'),
    url(r'^in_progress_orders/$', views.get_in_progress_sent_docs, name='get_in_progress_sent_docs'),
    url(r'^complete_orders/$', views.get_complete_sent_docs, name='get_complete_sent_docs'),
    url(r'^add_file_to_order/$', views.add_file_to_order, name='add_file_to_order'),
    url(r'^add_translation_file_to_order/$', views.add_translation_file_to_order, name='add_translation_file_to_order'),
    url(r'^update_order_translation/$', views.update_order_translation, name='update_order_translation'),
    url(r'^delete_file_from_order/$', views.delete_file_from_order, name='delete_file_from_order'),
    url(r'^delete_translation_file_from_order/$', views.delete_translation_file_from_order,
        name='delete_translation_file_from_order'),
    url(r'^delete_order/$', views.delete_order, name='delete_order'),
    url(r'^update_order/$', views.update_order, name='update_order'),
    url(r'^update_order_payment/$', views.update_order_payment, name='update_order_payment'),
    url(r'^add_new_order/$', views.add_new_order, name='add_new_order'),
    url(r'^set_resp/$', views.set_resp, name='set_resp'),
    url(r'^set_order_status/$', views.set_order_status, name='set_order_status'),
    url(r'^download_file/(?P<file_id>\d+)/$', views.download_file, name='download_file'),
    url(r'^change_just_paid/$', payments.change_just_paid, name='change_just_paid'),
    url(r'^change_payment_failre/$', payments.change_payment_failure, name='change_payment_failre'),
    url(r'^download_translation_file/(?P<file_id>\d+)/$', views.download_translation_file,
        name='download_translation_file'),
    url(r'^send_calc_to_client/$', views.send_calculation_to_client, name='send_calculation_to_client'),
    url(r'^send_trans_files_to_client/$', views.send_trans_files_to_client, name='send_trans_files_to_client'),


    url(r'^send_email/$', views.send_email, name='send_email'),
    url(r'^send_email_test/$', views.send_email_test, name='send_email_test'),

    url(r'^translator_details/(?P<translator_id>\d+)/$', views.get_translators_details, name='get_translators_details'),
    url(r'^translator_delete/$', views.delete_translator, name='delete_translator'),
    url(r'^translator_list/$', views.get_translators_list, name='get_translators_list'),
    url(r'^save_translator_photo/(?P<translator_id>\d+)/$', views.save_translator_photo, name='save_translator_photo'),
    url(r'^set_translator_for_order/$', views.set_translator_for_order, name='set_translator_for_order'),
    url(r'^save_translator_list/$', views.create_translator, name='save_translator'),
    url(r'^save_translator_new/$', views.create_translator, name='save_translator_new'),

    url(r'^manager_details/(?P<manager_id>\d+)/$', views.get_manager_details, name='get_manager_details'),
    url(r'^manager_complete_orders/(?P<manager_id>\d+)/$', views.get_manager_complete_orders, name='get_manager_complete_orders'),
    url(r'^manager_delete/$', views.delete_manager, name='delete_manager'),
    url(r'^managers_list/$', views.get_managers_list, name='get_managers_list'),
    url(r'^save_manager_new/$', views.create_manager, name='save_manager_new'),
    url(r'^save_manager_photo/(?P<manager_id>\d+)/$', views.save_manager_photo, name='save_manager_photo'),

    url(r'^admin_details/(?P<admin_id>\d+)/$', views.get_admin_details, name='get_admin_details'),
    url(r'^admin_delete/$', views.delete_admin, name='delete_admin'),
    url(r'^admins_list/$', views.get_admins_list, name='get_admins_list'),
    url(r'^save_admin_new/$', views.create_admin, name='save_admin_new'),
    url(r'^save_admin_photo/(?P<admin_id>\d+)/$', views.save_admin_photo, name='save_admin_photo'),

    url(r'^client_details/(?P<client_id>\d+)/$', views.get_client_details, name='get_client_details'),
    url(r'^client_delete/$', views.delete_client, name='delete_client'),
    url(r'^clients_list/$', views.get_clients_list, name='get_clients_list'),
    url(r'^save_client_new/$', views.create_client, name='save_client_new'),
    url(r'^save_client_photo/(?P<client_id>\d+)/$', views.save_client_photo, name='save_client_photo'),

    # url(r'^login/$', views.loginUser, name='loginUser'),
    # url(r'^logout/$', views.logout_user, name='logoutUser'),
    # url(r'^ckusr/$', views.check_user, name='check_user'),
    # url(r'^reg/$', views.reg_user, name='reg_user'),

    url(r'^testimonials_list/$', ru_views.get_testimonials_list, name='testimonials_list'),
    url(r'^add_testimonials/$', views.add_testimonial, name='add_testimonial'),
    url(r'^save_testimonial/$', views.save_testimonial, name='save_testimonial'),
    url(r'^testimonial/(?P<testimonial_id>\d+)/$', views.testimonial, name='testimonial'),

    url(r'^save_company/$', views.save_company, name='save_company'),
    url(r'^companies_list/$', views.companies_list, name='companies_list'),
    url(r'^add_company/$', views.add_company, name='add_company'),
    url(r'^company/(?P<company_id>\d+)/$', views.company, name='company'),

]