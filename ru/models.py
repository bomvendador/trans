from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import positions
import os


class Testimonials(models.Model):
    text = models.CharField(max_length=3000)
    name = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    is_approved = models.BooleanField(default=False)
    new = models.BooleanField(default=True)


class Language (models.Model):
    name = models.CharField(max_length=50)


class Role(models.Model):
    role_name = models.CharField(max_length=20)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    tel = models.CharField(max_length=15)
    role = models.ForeignKey(Role, blank=False, null=False)


class OrderStatus(models.Model):
    name = models.CharField(max_length=15)
    position = positions.PositionField(collection='name')

    class Meta:
        ordering = ['position']


class PayStatus(models.Model):
    name = models.CharField(max_length=15)


class PayMethod(models.Model):
    name = models.CharField(max_length=15)


class OrderSource(models.Model):
    name = models.CharField(max_length=15)


class TranslationType(models.Model):
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=50, null=True, blank=True)


class TranslationTheme(models.Model):
    name = models.CharField(max_length=20)
    short_name = models.CharField(max_length=50, null=True, blank=True)


class Phone(models.Model):
    number = models.CharField(max_length=25)


class Email (models.Model):
    email = models.EmailField(null=True, blank=True)


class PaymentDetails(models.Model):
    payment_method = models.ForeignKey(PayMethod)
    owner = models.ForeignKey(User, related_name='payment_details_owner')
    detail = models.CharField(max_length=30)
    added = models.DateTimeField(auto_now_add=True, auto_now=False)
    changed = models.DateTimeField(auto_now_add=False, auto_now=True)
    author = models.ForeignKey(User, related_name='payment_details_author')


class Translator(models.Model):
    creator = models.ForeignKey(User, blank=True, null=True, related_name='translator_creator', on_delete=models.CASCADE)
    changed_by = models.ForeignKey(User, blank=True, null=True, related_name='translator_changed_by', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    tel = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    date_birth = models.DateField(null=True, blank=True)
    registered = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    changed = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    photo = models.ImageField(upload_to=settings.BASE_DIR + '/media/photo', null=True, blank=True)
    photo_name = models.CharField(max_length=100, null = True, blank = True)
    password = models.CharField(max_length=50, null=True, blank=True)
    user = models.OneToOneField(User, blank=True, null=True)
    init_password = models.CharField(max_length=50, blank=True, null=True)


class Manager(models.Model):
    creator = models.ForeignKey(User, blank=True, null=True, related_name='manager_creator', on_delete=models.CASCADE)
    changed_by = models.ForeignKey(User, blank=True, null=True, related_name='manager_changed_by', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    tel = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    date_birth = models.CharField(max_length=15, null=True, blank=True)
    registered = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    changed = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
    photo = models.ImageField(upload_to=settings.BASE_DIR + '/media/photo', default=None)
    photo_name = models.CharField(max_length=100, blank=True, null=True)
    user = models.OneToOneField(User, blank=True, null=True)
    init_password = models.CharField(max_length=50, blank=True, null=True)
    payment_details = models.ForeignKey(PaymentDetails, null=True, blank=True)
    orders_new = models.IntegerField(null=True, blank=True, default=0)
    orders_in_progress = models.IntegerField(null=True, blank=True, default=0)
    orders_complete = models.IntegerField(null=True, blank=True, default=0)

    def filename(self):
        return os.path.basename(self.photo.name)


class Admin(models.Model):
    creator = models.ForeignKey(User, blank=True, null=True, related_name='admin_creator', on_delete=models.CASCADE)
    changed_by = models.ForeignKey(User, blank=True, null=True, related_name='admin_changed_by', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    tel = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    date_birth = models.CharField(max_length=15, null=True, blank=True)
    registered = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    changed = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
    photo = models.ImageField(upload_to=settings.BASE_DIR + '/media/photo', null=True, blank=True)
    user = models.OneToOneField(User, blank=True, null=True)
    init_password = models.CharField(max_length=50, blank=True, null=True)


class Client(models.Model):
    creator = models.ForeignKey(User, blank=True, null=True, related_name='client_creator', on_delete=models.CASCADE)
    changed_by = models.ForeignKey(User, blank=True, null=True, related_name='client_changed_by', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    tel = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    date_birth = models.CharField(max_length=15, null=True, blank=True)
    registered = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    changed = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
    photo = models.ImageField(upload_to=settings.BASE_DIR + '/media/photo', null=True, blank=True)
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    init_password = models.CharField(max_length=50, blank=True, null=True)
    orders_in_progress = models.IntegerField(null=True, blank=True, default=0)
    orders_complete = models.IntegerField(null=True, blank=True, default=0)
    orders_paid = models.IntegerField(null=True, blank=True, default=0)
    visited_times = models.IntegerField(default=0)


class SentDoc (models.Model):
    user = models.ForeignKey(User, blank=True, null=True, related_name='user')
    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    tel = models.CharField(max_length=15, null=True, blank=True)
    text = models.CharField(max_length=10000, null=True, blank=True)
    text_qnt = models.IntegerField(blank=True, null=True)
    trans_from = models.ForeignKey(Language, blank=True, null=True, related_name='trans_from')
    trans_to = models.ForeignKey(Language, blank=True, null=True)
    status = models.ForeignKey(OrderStatus, blank=False, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    resp = models.ForeignKey(User, blank=False, null=True, related_name='resp')
    translator = models.ForeignKey(Translator, blank=True, null=True, related_name='translator')
    files_qnt = models.IntegerField(blank=True, null=True)
    order_src = models.ForeignKey(OrderSource, blank=False, null=False, default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    payment_amount = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    paystatus = models.ForeignKey(PayStatus, blank=True, null=True)
    paymethod = models.ForeignKey(PayMethod, blank=True, null=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    changed = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    calc_sent_date = models.DateTimeField(null=True, blank=True)
    translation_sent_date = models.DateTimeField(null=True, blank=True)
    translation_files = models.BooleanField(default=False)
    translation_downloaded = models.BooleanField(default=False)
    author = models.ForeignKey(User, related_name='author', blank=True, null=True)
    comments = models.NullBooleanField(default=False, blank=True, null=True)
    paid_to_manager = models.NullBooleanField(default=False)
    paid_to_manager_date = models.CharField(max_length=15, blank=True, null=True)
    paid_to_translator = models.NullBooleanField(default=False)
    paid_to_translator_date = models.CharField(max_length=15, blank=True, null=True)
    contact_form_message = models.CharField(max_length=150, blank=True, null=True)
    translation_type = models.ForeignKey(TranslationType, blank=True, null=True)
    translation_theme = models.ForeignKey(TranslationTheme, blank=True, null=True)
    just_paid = models.BooleanField(default=False)
    payment_failure = models.BooleanField(default=False)


class BackCall(models.Model):
    tel = models.CharField(max_length=25)
    name = models.CharField(max_length=100)
    added = models.DateTimeField(auto_now_add=True, auto_now=False)
    order = models.ForeignKey(SentDoc, null=True, blank=True)
    new = models.BooleanField(default=True)
    viewed_by = models.ForeignKey(User, null=True, blank=True)


class BackCallComments(models.Model):
    back_call = models.ForeignKey(BackCall)
    comment = models.CharField(max_length=200)
    added = models.DateTimeField(auto_now=False, auto_now_add=True)
    author = models.ForeignKey(User)
    author_role = models.ForeignKey(Role, null=True, blank=True)


class OrderComments(models.Model):
    order = models.ForeignKey(SentDoc)
    comment = models.CharField(max_length=200)
    added = models.DateTimeField(auto_now=False, auto_now_add=True)
    author = models.ForeignKey(User)
    author_role = models.ForeignKey(Role, null=True, blank=True)


class OrderCommentsClients(models.Model):
    order = models.ForeignKey(SentDoc)
    comment = models.CharField(max_length=200)
    answer = models.CharField(max_length=200, null=True, blank=True)
    added = models.DateTimeField(auto_now=False, auto_now_add=True)
    changed = models.DateTimeField(auto_now=True, auto_now_add=False)
    answer_author = models.ForeignKey(User, null=True, blank=True)
    answer_author_role = models.ForeignKey(Role, null=True, blank=True)


class TranslationFiles(models.Model):
    file = models.FileField(upload_to=settings.BASE_DIR + '/media/translation_files', blank=True, null=True)
    file_name = models.CharField(max_length=100, null=True, blank=True)
    order = models.ForeignKey(SentDoc, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True, auto_now=False)
    changed = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    uploaded_by = models.ForeignKey(User, null=True, blank=True)


class SentFiles (models.Model):
    file = models.FileField(upload_to=settings.BASE_DIR + '/media/sent_docs')
    file_name = models.CharField(max_length=150, null=True)
    sent_doc = models.ForeignKey(SentDoc)


class Translator_Lang(models.Model):
    translator = models.ForeignKey(Translator, blank=True, null=True)
    lang = models.ForeignKey(Language, blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)
    changed = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)

