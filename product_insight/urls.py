"""
URL configuration for product_insight project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from . import views

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # Default language switcher
    path('set-language/', views.set_language_ajax, name='set_language_ajax'),  # AJAX language switcher
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path(_('about/'), TemplateView.as_view(template_name='about.html'), name='about'),
    path(_('contact/'), TemplateView.as_view(template_name='contact.html'), name='contact'),
    path(_('privacy/'), TemplateView.as_view(template_name='privacy.html'), name='privacy'),
    path(_('terms/'), TemplateView.as_view(template_name='terms.html'), name='terms'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    prefix_default_language=False
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
