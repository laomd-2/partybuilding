import datetime
from datetime import date

from django.db.models import F
from tablib.core import Dataset

from common.base import wrap
from import_export import resources


class MyResource(resources.ModelResource):
    def before_import(self, dataset: Dataset, using_transactions, dry_run, **kwargs):
        fields = self._meta.model.export_field_map()
        dataset.headers = [fields[verbose_name] for verbose_name in dataset.headers]
        super().before_import(dataset, using_transactions, dry_run, **kwargs)

    def before_import_row(self, row, **kwargs):
        replaces = './'
        base_date = date(1900, 1, 1)
        for key, value in row.items():
            if isinstance(value, float) and 49 * 365 < value < (2050 - 1900) * 365:
                value = str(base_date + datetime.timedelta(days=int(value - 2)))
            elif isinstance(value, str):
                if value == '是':
                    value = True
                elif value == '否':
                    value = False
                else:
                    for rep in replaces:
                        value = value.replace(rep, '-')
            row[key] = value
        super(MyResource, self).before_import_row(row, **kwargs)
                            
    def get_export_headers(self):
        headers = super(MyResource, self).get_export_headers()
        model = self._meta.model
        headers_ = []
        for f in headers:
            meta = model._meta
            fields = f.split('__')
            for f1 in fields[:-1]:
                meta = meta.get_field(f1).remote_field.model._meta
            headers_.append(meta.get_field(fields[-1]).verbose_name)
        return headers_

    def export_resource(self, obj):
        res = []
        for field in self.get_export_fields():
            value = getattr(obj, field.column_name)
            res.append(wrap(value))
        return res
