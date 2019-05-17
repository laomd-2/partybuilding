from django import forms
from common.forms import DateCheckModelForm


class ActivityForm(DateCheckModelForm):
    def __init__(self, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)
        self.fields['should_phase'].widget = forms.widgets.CheckboxSelectMultiple()
