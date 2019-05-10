from django.forms.models import ModelForm
from datetime import datetime
from datetime import date


class DateCheckModelForm(ModelForm):
    def clean(self):
        cd = super().clean()
        model = type(self.instance)
        for f in model._meta.fields:
            if 'Date' in f.get_internal_type():
                d = cd.get(f.name)
                if d:
                    if isinstance(d, date):
                        d = datetime.combine(d, datetime.min.time())
                    if d > datetime.now():
                        self.add_error(f.name, '您穿越了？')
        return cd
