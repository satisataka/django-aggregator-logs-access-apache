from django_filters import rest_framework as filters
from rest_framework import generics

from log_access_apache.models import LogAccessApacheModel
from .serializers import LogAccessApacheSerializer
from .filters import LogAccessApacheFilter


class LogAccessApacheList(generics.ListAPIView):
    queryset = LogAccessApacheModel.objects.all()
    serializer_class = LogAccessApacheSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class=LogAccessApacheFilter


class LogAccessApacheDetail(generics.RetrieveAPIView):
    queryset = LogAccessApacheModel.objects.all()
    serializer_class = LogAccessApacheSerializer

