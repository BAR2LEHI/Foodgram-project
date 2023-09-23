from django.views.generic import TemplateView

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('foodgram_api.urls')),
    path('redoc/', TemplateView.as_view(
        template_name='redoc.html'
    ), name='redoc')
]
