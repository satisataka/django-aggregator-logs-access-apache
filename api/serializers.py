from log_access_apache.models import LogAccessApacheModel
from rest_framework import serializers


class LogAccessApacheSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LogAccessApacheModel
        fields = '__all__'
        extra_kwargs = {
            'url': {'view_name': 'api-log-detail'},
        }
