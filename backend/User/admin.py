from django.contrib import admin

from .models import FoodGramUser


@admin.register(FoodGramUser)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
    )
    search_fields = (
        'username',
        'email',
    )
    empty_value_display = '-пусто-'
