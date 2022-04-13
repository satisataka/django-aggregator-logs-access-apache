from django.urls import path

from .views import LogAccessApacheListView, LogDetailView

urlpatterns = [
    path('', LogAccessApacheListView.as_view(), name='logs_list'),
    path('<int:pk>/', LogDetailView.as_view(), name='log_detail'),
]
