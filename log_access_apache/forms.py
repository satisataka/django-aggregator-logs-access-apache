from .models import LogAccessApacheModel
from django import forms

#CharField, ModelForm, Form, GenericIPAddressField, DateTimeField, DateInput, Ip

class LogAccessApacheFilterForm(forms.Form):
    host = forms.GenericIPAddressField(
        required=False,
        label='Host (IP)',
        help_text='Enter IP (127.0.0.1)',
    )
    date_start = forms.DateTimeField(
        widget=forms.DateInput(),
        required=False,
        label='Date start',
        help_text='Enter Date (01-01-2022)',
    )
    time_start = forms.TimeField(
        widget=forms.TimeInput(),
        required=False,
        label='Time start',
        help_text='Enter Time (13:47:10)',
        initial='00:00:00',
    )
    date_end = forms.DateTimeField(
        widget=forms.DateInput(),
        required=False,
        label='Date end',
        help_text='Enter Date (01-01-2022)',
    )
    time_end = forms.TimeField(
        widget=forms.TimeInput(),
        required=False,
        label='Time end',
        help_text='Enter Time (13:47:10)',
        initial='23:59:59',
    )


