from django.contrib import admin
from .models import *


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'video_url')
    search_fields = ('title',)
    list_filter = ('title',)


@admin.register(Script)
class ScriptAdmin(admin.ModelAdmin):
    list_display = ('id', 'script_title', 'product_title', 'product_category', 'rating')
    search_fields = ('script_title', 'product_title', 'product_category')
    list_filter = ('product_category', 'scripts_ton')
