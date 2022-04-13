from ntpath import join
from re import template
from django.shortcuts import render
from .models import LogAccessApacheModel
from django.views.generic.list import ListView
from django.core.validators import validate_ipv46_address
from django.core.exceptions import ValidationError
from django.views.generic.edit import FormMixin
from django.views.generic.detail import DetailView
from .forms import LogAccessApacheFilterForm
from django.db.models import Q
from datetime import datetime


class FilterMixin(object):
    def get_queryset_filters(self):
        filters = {}
        if self.form.is_valid():
            filters = {}
            for item in self.allowed_filters:
                if item in self.request.GET:
                    if self.form.cleaned_data[item]:
                        if item == 'date_end':
                            date_end = self.form.cleaned_data[item]
                            self.form.cleaned_data[item] =  datetime.combine(date_end.date(), datetime.max.time())
                        filters[self.allowed_filters[item]] = self.form.cleaned_data[item]
        return filters

    def get_queryset(self):
        return super().get_queryset().filter(**self.get_queryset_filters())


class LogAccessApacheListView(FilterMixin, ListView, FormMixin):
    model = LogAccessApacheModel
    paginate_by = 100
    template_name = "logs/logs_list.html"
    form_class = LogAccessApacheFilterForm
    allowed_filters = {
        'host': 'host',
        'date_start': 'date__gte',
        'date_end': 'date__lte',
        'time_start': 'date__time__gte',
        'time_end': 'date__time__lte',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        if self.paginate_by:
            page_get = '&'.join([k+'='+v for k, v in self.request.GET.items() if k!='page' and v])
            context['page_get'] = page_get
        return context

    def get(self, request, *args, **kwargs):
        self.form = self.form_class(request.GET)
        return super().get(request, *args, **kwargs)

class LogDetailView(DetailView):
    model = LogAccessApacheModel
    template_name = "logs/log_detail.html"
