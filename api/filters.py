
from django import forms
from django.core import validators
from django_filters import widgets, rest_framework as filters

from log_access_apache.models import LogAccessApacheModel

class LogAccessApacheFilter(filters.FilterSet):
    host = filters.CharFilter(
        label='Host (IP)',
        widget=forms.TextInput(attrs={'placeholder': '255.255.255.255',}),
        validators=[validators.validate_ipv46_address]
        )
    date = filters.DateTimeFromToRangeFilter(
        label="Date range",
        widget=widgets.RangeWidget(attrs={'type': 'date',}),
        help_text='Enter Date (01.01.2022)',
    )
    time =filters.TimeRangeFilter(
        field_name='date__time',
        label="Time range",
        widget=widgets.RangeWidget(attrs={'type': 'time', "step": "1"}),
        help_text='Enter Time (12:01:20)',
    )

    class Meta:
        model = LogAccessApacheModel
        fields = ['host', 'date', 'time']
