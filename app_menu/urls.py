from django.urls import path
from app_menu.views import IndexView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>/', IndexView.as_view(), name='detail_menu'),
]
