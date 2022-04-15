from django.urls import path

from .views import LogDetailView, LogAccessApacheFilterView

urlpatterns = [

    path('', LogAccessApacheFilterView.as_view(), name='logs_list'),
    path('<int:pk>/', LogDetailView.as_view(), name='log_detail'),

]
