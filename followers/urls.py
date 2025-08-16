from django.urls import path
from . import views

urlpatterns = [
    path('', views.FollowerList.as_view(), name='follow-list'),
    path('<int:pk>/', views.FollowerDetail.as_view(), name='follow-detail'),
]