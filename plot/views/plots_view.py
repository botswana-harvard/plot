from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls.base import reverse
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from django.views.generic import TemplateView

from edc_base.view_mixins import EdcBaseViewMixin
from edc_search.forms import SearchForm
from edc_search.view_mixins import SearchViewMixin

from ..constants import RESIDENTIAL_HABITABLE
from ..models import Plot

from .result_wrapper import ResultWrapper


app_config = django_apps.get_app_config('plot')


class SearchPlotForm(SearchForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_action = reverse('plot:list_url')


class PlotResultWrapper(ResultWrapper):
    pass


class PlotsView(EdcBaseViewMixin, TemplateView, SearchViewMixin, FormView):

    form_class = SearchPlotForm
    template_name = app_config.list_template_name
    paginate_by = 10
    list_url = 'plot:list_url'
    search_model = Plot
    url_lookup_parameters = ['id', 'plot_identifier']
    queryset_ordering = '-created'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def search_options_for_date(self, search_term, **kwargs):
        q, options = super().search_options_for_date(search_term, **kwargs)
        q = q | Q(report_datetime__date=search_term.date())
        return q, options

    def search_options(self, search_term, **kwargs):
        q, options = super().search_options(search_term, **kwargs)
        if search_term.lower() == 'ess':
            options = {'ess': True}
            q = Q()
        else:
            q = q | Q(plot_identifier__icontains=search_term)
        return q, options

    def queryset_wrapper(self, qs):
        """Override to wrap each plot instance in the paginated queryset."""
        results = []
        for obj in qs:
            results.append(PlotResultWrapper(obj))
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            navbar_selected='plot',
            RESIDENTIAL_HABITABLE=RESIDENTIAL_HABITABLE)
        return context
