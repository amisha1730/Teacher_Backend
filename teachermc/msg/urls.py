from django.urls import path,include
from .views import GetMsg


urlpatterns = [
    path('get', GetMsg.as_view()),
]

