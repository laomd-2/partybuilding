
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

from common.rules import is_school_admin
from xadmin.plugins.utils import get_context_dict
from xadmin.sites import site
from xadmin.views import BaseAdminPlugin, ListAdminView, DetailAdminView, UpdateAdminView
from xadmin.views.dashboard import ModelBaseWidget, widget_manager
from xadmin.util import lookup_field, label_for_field, json


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


class ChartWidget(ModelBaseWidget):
    widget_type = 'chart'
    chart_attr_name = ''
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

        if hasattr(model_admin, self.chart_attr_name):
            if chart and chart in model_admin.detail_charts:
                self.charts = {chart: model_admin.detail_charts[chart]}
                self.one_chart = True
                if self.title is None:
                    self.title = model_admin.detail_charts[chart].get('title')
            else:
                self.charts = model_admin.detail_charts
                if self.title is None:
                    self.title = ugettext(
                        "%s Charts") % self.model._meta.verbose_name_plural

    def get_chart_url(self, name, v):
        pass

    def filte_choices_model(self, model, modeladmin):
        return bool(getattr(modeladmin, self.chart_attr_name, None)) and \
               super(ChartWidget, self).filte_choices_model(model, modeladmin)

    def context(self, context):
        context.update({
            'charts': [{"name": name, "title": v['title'], 'url': self.get_chart_url(name, v)} for name, v in self.charts.items()],
        })

    # Media
    def media(self):
        return self.vendor('flot.js', 'xadmin.plugin.anycharts.js')


@widget_manager.register
class DetailChartWidget(ChartWidget):
    chart_attr_name = 'detail_charts'

    def get_chart_url(self, name, v):
        which = ''
        try:
            which = str(int(self.request.path.split('/')[-3]))
        except ValueError:
            pass
        return self.model_admin_url('detailchart', name) + "?" + self.opts.model_name + '=%s' % which


@widget_manager.register
class ListChartWidget(ChartWidget):
    chart_attr_name = 'list_charts'

    def get_chart_url(self, name, v):
        return self.model_admin_url('listchart', name) + "?"


class ChartsPlugin(BaseAdminPlugin):
    def get_chart_url(self, name, v):
        pass
    
    # Media
    def get_media(self, media):
        return media + self.vendor('flot.js', 'xadmin.plugin.anycharts.js')


class DetailChartsPlugin(ChartsPlugin):
    detail_charts = {}
    
    def init_request(self, *args, **kwargs):
        return is_school_admin(self.request.user) and bool(self.detail_charts)

    def get_chart_url(self, name, v):
        which = ''
        try:
            which = str(int(self.request.path.split('/')[-3]))
        except ValueError:
            pass
        return self.admin_view.model_admin_url('detailchart', name) + "?" + self.opts.model_name + '=%s' % which

    def block_after_fieldsets(self, context, nodes):
        context.update({
            'charts': [{"name": name, "title": v['title'], 'url': self.get_chart_url(name, v)}
                       for name, v in self.detail_charts.items()],
        })
        nodes.append(loader.render_to_string('xadmin/blocks/model_list.results_top.charts.html',
                                             context=get_context_dict(context)))


class ListChartsPlugin(ChartsPlugin):
    list_charts = {}

    def init_request(self, *args, **kwargs):
        return bool(self.list_charts)

    def get_chart_url(self, name, v):
        return self.admin_view.model_admin_url('listchart', name) + "?"

    def block_after_results(self, context, nodes):
        context.update({
            'charts': [{"name": name, "title": v['title'], 'url': self.get_chart_url(name, v)}
                       for name, v in self.list_charts.items()],
        })
        nodes.append(loader.render_to_string('xadmin/blocks/model_list.results_top.charts.html',
                                             context=get_context_dict(context)))


class ChartsView(ListAdminView):
    detail_charts = {}

    def get_ordering(self):
        if 'order' in self.chart:
            return self.chart['order']
        else:
            return super(ChartsView, self).get_ordering()

    def get(self, request, name):
        charts = self.detail_charts
        if name not in charts:
            return HttpResponseNotFound()
        self.chart = charts[name]
        content = {'option': self.chart['option']}
        result = json.dumps(content, cls=JSONEncoder, ensure_ascii=False)
        return HttpResponse(result)


class ListChartsView(ListAdminView):
    list_charts = {}

    def get_ordering(self):
        if 'order' in self.chart:
            return self.chart['order']
        else:
            return super(ListChartsView, self).get_ordering()

    def get(self, request, name):
        charts = self.list_charts
        if name not in charts:
            return HttpResponseNotFound()
        self.chart = charts[name]
        content = {'option': self.chart['option']}
        result = json.dumps(content, cls=JSONEncoder, ensure_ascii=False)
        return HttpResponse(result)


site.register_plugin(ListChartsPlugin, ListAdminView)
site.register_plugin(DetailChartsPlugin, DetailAdminView)
site.register_plugin(DetailChartsPlugin, UpdateAdminView)
site.register_modelview(r'^detailchart/(.+)/$', ChartsView, name='%s_%s_detailchart')
site.register_modelview(r'^listchart/(.+)/$', ListChartsView, name='%s_%s_listchart')
