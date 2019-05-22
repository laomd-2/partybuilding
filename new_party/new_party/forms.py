from django.forms import CheckboxInput, BooleanField
from django.forms import ModelForm
from datetime import datetime
from datetime import date
from django.utils.safestring import mark_safe


class ToggleInput(CheckboxInput):
    def render(self, name, value, attrs=None, renderer=None):
        res = super().render(name, value, attrs, renderer)
        res += mark_safe('''<script>$("[name='%s']").bootstrapSwitch();</script>''' % name)
        return res


class ToggleField(BooleanField):
    widget = ToggleInput


class DateCheckModelForm(ModelForm):
    pass
    # def clean(self):
    #     cd = super().clean()
    #     model = type(self.instance)
    #     for f in model._meta.fields:
    #         if 'Date' in f.get_internal_type():
    #             d = cd.get(f.name)
    #             if d:
    #                 if isinstance(d, date):
    #                     d = datetime.combine(d, datetime.min.time())
    #                 if d > datetime.now():
    #                     self.add_error(f.name, '您穿越了？')
    #     return cd
