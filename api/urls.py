from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import LogAccessApacheList, LogAccessApacheDetail


urlpatterns = [
    path('logs-list/', LogAccessApacheList.as_view(), name='api-logs-list'),
    path('log/<int:pk>/', LogAccessApacheDetail.as_view(), name="api-log-detail"),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
