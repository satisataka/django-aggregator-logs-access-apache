from wsgiref.validate import validator
from .models import LogAccessApacheModel
from django import forms
import django_filters
from django_filters import widgets

from django.core import validators

class LogAccessApacheFilter(django_filters.FilterSet):
    host = django_filters.CharFilter(
        label='Host (IP)',
        widget=forms.TextInput(attrs={'placeholder': '255.255.255.255',}),
        validators=[validators.validate_ipv46_address]
        )
    date = django_filters.DateFromToRangeFilter(
        label="Date range",
        widget=widgets.RangeWidget(attrs={'type': 'date',}),
        help_text='Enter Date (01.01.2022)',
    )
    time =django_filters.TimeRangeFilter(
        field_name='date__time',
        label="Time range",
        widget=widgets.RangeWidget(attrs={'type': 'time', "step": "1"}),
        help_text='Enter Time (12:01:20)',
    )
    class Meta:
        model = LogAccessApacheModel
        fields = ['host', 'date', 'time']
