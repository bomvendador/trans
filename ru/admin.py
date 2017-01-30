from django.contrib import admin
from ru.models import Translator

# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Translator)