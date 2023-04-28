from django.urls import path
from django.views.generic import TemplateView
from django.urls import include
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', TemplateView.as_view(template_name="index.html"), name='index'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('auth.urls')),
]
