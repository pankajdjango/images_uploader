from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from home import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.home),
    path("delete",views.delete),
    path("logout",views.logout),
    path("upload_images",views.upload_images),
    # path("login",views.register_or_login),
    path("login",views.register_user),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
