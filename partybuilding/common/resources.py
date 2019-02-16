import datetime
from datetime import date
from tablib.core import Dataset
from import_export import resources


class MyResource(resources.ModelResource):
    def before_import(self, dataset: Dataset, using_transactions, dry_run, **kwargs):
        fields = self._meta.model.export_field_map()
        replaces = '年月/'
        base_date = date(1900, 1, 1)
        for i in range(len(dataset)):
            row = list(dataset[i])
            for j in range(len(row)):
                if isinstance(row[j], float) and 49*365 < row[j] < (2050-1900)*365:
                    row[j] = str(base_date + datetime.timedelta(days=int(row[j] - 2)))
                elif isinstance(row[j], str):
                    if row[j] == '空':
                        row[j] = ''
                    else:
                        for rep in replaces:
                            row[j] = row[j].replace(rep, '-')
                        row[j] = row[j].replace('日', '')
            dataset[i] = tuple(row)
        dataset.headers = [fields[verbose_name] for verbose_name in dataset.headers]
        super().before_import(dataset, using_transactions, dry_run, **kwargs)