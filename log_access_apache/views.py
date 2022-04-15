from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView

from .models import LogAccessApacheModel
from .filters import LogAccessApacheFilter


class LogAccessApacheFilterView(LoginRequiredMixin, FilterView):
    template_name = "logs/logs_list.html"
    model = LogAccessApacheModel
    paginate_by = 10
    filterset_class = LogAccessApacheFilter


class LogDetailView(DetailView):
    model = LogAccessApacheModel
    template_name = "logs/log_detail.html"
