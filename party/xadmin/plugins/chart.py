
import calendar
import datetime
import decimal

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader
from django.utils.http import urlencode
from django.utils.encoding import force_text, smart_text
from django.utils.translation import ugettext_lazy as _, ugettext

from xadmin.plugins.utils import get_context_dict
from xadmin.sites import site
from xadmin.views import BaseAdminPlugin, ListAdminView
from xadmin.views.dashboard import ModelBaseWidget, widget_manager
from xadmin.util import lookup_field, label_for_field, json


@widget_manager.register
class ChartWidget(ModelBaseWidget):
    widget_type = 'chart'
    description = _('Show models simple chart.')
    template = 'xadmin/widgets/chart.html'
    widget_icon = 'fa fa-bar-chart-o'

    def convert(self, data):
        self.list_params = data.pop('params', {})
        self.chart = data.pop('chart', None)

    def setup(self):
        super(ChartWidget, self).setup()

        self.charts = {}
        self.one_chart = False
        model_admin = self.admin_site._registry[self.model]
        chart = self.chart

        if hasattr(model_admin, 'data_charts'):
            if chart and chart in model_admin.data_charts:
                self.charts = {chart: model_admin.data_charts[chart]}
                self.one_chart = True
                if self.title is None:
                    self.title = model_admin.data_charts[chart].get('title')
            else:
                self.charts = model_admin.data_charts
                if self.title is None:
                    self.title = ugettext(
                        "%s Charts") % self.model._meta.verbose_name_plural

    def filte_choices_model(self, model, modeladmin):
        return bool(getattr(modeladmin, 'data_charts', None)) and \
            super(ChartWidget, self).filte_choices_model(model, modeladmin)

    def get_chart_url(self, name, v):
        return self.model_admin_url('chart', name) + "?" + urlencode(self.list_params)

    def context(self, context):
        context.update({
            'charts': [{"name": name, "title": v['title'], 'url': self.get_chart_url(name, v)} for name, v in self.charts.items()],
        })

    # Media
    def media(self):
        return self.vendor('flot.js', 'xadmin.plugin.anycharts.js')


class JSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime.date, datetime.datetime)):
            return calendar.timegm(o.timetuple()) * 1000
        elif isinstance(o, decimal.Decimal):
            return str(o)
        else:
            try:
                return super(JSONEncoder, self).default(o)
            except Exception:
                return smart_text(o)


class ChartsPlugin(BaseAdminPlugin):

    data_charts = {}

    def init_request(self, *args, **kwargs):
        return bool(self.data_charts)

    def get_chart_url(self, name, v):
        return self.admin_view.model_admin_url('chart', name) + self.admin_view.get_query_string()

    # Media
    def get_media(self, media):
        return media + self.vendor('flot.js', 'xadmin.plugin.anycharts.js')

    # Block Views
    def block_results_bottom(self, context, nodes):
        context.update({
            'charts': [{"name": name, "title": v['title'], 'url': self.get_chart_url(name, v)} for name, v in self.data_charts.items()],
        })
        nodes.append(loader.render_to_string('xadmin/blocks/model_list.results_top.charts.html',
                                             context=get_context_dict(context)))


class ChartsView(ListAdminView):

    data_charts = {}

    def get_ordering(self):
        if 'order' in self.chart:
            return self.chart['order']
        else:
            return super(ChartsView, self).get_ordering()

    def get(self, request, name):
        if name not in self.data_charts:
            return HttpResponseNotFound()
        self.chart = self.data_charts[name]
        content = {'option': self.chart['option']}
        result = json.dumps(content, cls=JSONEncoder, ensure_ascii=False)
        return HttpResponse(result)


site.register_plugin(ChartsPlugin, ListAdminView)
site.register_modelview(r'^chart/(.+)/$', ChartsView, name='%s_%s_chart')
