from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views
from .v1.views import RecipesViewSet


app_name = 'foodgram_api'


urlpatterns = [
    path('v1/', include('foodgram_api.v1.urls')),
    path('api-token-auth/', views.obtain_auth_token)
]
