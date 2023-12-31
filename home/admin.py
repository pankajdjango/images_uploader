from django.contrib import admin
from django.utils.html import format_html
from .models import Image,UserAccount,Docs

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["id","name","duplicate","generated", "active", "source", "display_image" ]
    list_filter = ['generated', 'active',"duplicate"]

    def display_image(self, obj):
        return format_html(f'<img src="{obj.photo.url}" width="100" height="100"  style="border-radius: 50%;"/>')

    display_image.short_description = 'Image'

@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ["user_id","email","first_name","last_name","password","mobile_no","is_active","is_staff","generated","date_joined"]
    list_filter = ['user_id', 'is_active',"first_name","mobile_no","email"]

@admin.register(Docs)
class DocsAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "upload_file", "generated", "active", "duplicate", "user_id"]
    list_filter = ['generated', 'active',"user_id"]

    def display_docs(self, obj):
        return format_html(f'<a href="{obj.upload_file.url}" width="100" height="100"  style="border-radius: 50%;">{obj.name} <a/>')

    display_docs.short_description = 'Docs'

