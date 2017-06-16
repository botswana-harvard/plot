from django.apps import apps as django_apps

from edc_model_wrapper.wrappers import ModelWithLogWrapper

from .plot_log_entry_model_wrapper import PlotLogEntryModelWrapper


class PlotWithLogEntryModelWrapper(ModelWithLogWrapper):

    model = 'plot.plot'
    log_entry_model_wrapper_cls = PlotLogEntryModelWrapper
    next_url_name = django_apps.get_app_config('plot').listboard_url_name
    next_url_attrs = ['plot_identifier']

    @property
    def plot(self):
        return self.object