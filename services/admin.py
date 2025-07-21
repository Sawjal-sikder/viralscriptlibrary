from django.contrib import admin
from .models import *


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'video_url')
    search_fields = ('title',)
    list_filter = ('title',)


@admin.register(Script)
class ScriptAdmin(admin.ModelAdmin):
    list_display = "__all__"
    search_fields = ('script_title', 'product_title', 'product_category')
    list_filter = ('product_category', 'scripts_ton')


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = "__all__"
    search_fields = ('title',)
    list_filter = ('have_access_scripts_per_month', 'full_scripts_library_access',
                   'downloadable_template', 'ai_screept_generator')
    
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'package', 'start_date', 'end_date')
    # list_filter = ('start_date', 'end_date')

