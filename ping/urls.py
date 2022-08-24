from django.urls import path
from .views import pingView

urlpatterns = [
    path('', pingView, name='ping'),
]
