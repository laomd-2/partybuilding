from common.forms import DateCheckModelForm
from .util import check_fields
import re

eighteen = re.compile(r'^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$')


class InfoForm(DateCheckModelForm):
    def is_valid(self):
        if super(InfoForm, self).is_valid():
            self.save(commit=False)
            errors = []
            res = check_fields(self.instance, errors)
            for e in errors:
                self.add_error(None, e)
            return res
        return False

    def clean(self):
        cd = super().clean()
        id_card = cd.get('id_card_number')
        if id_card and (not eighteen.match(id_card) or
                        id_card[6:14] != str(cd.get('birth_date', '')).replace('-', '') or
                        ((int(id_card[-2]) & 1) == (int(cd.get('gender') != '男') & 1))):
            self.add_error('id_card_number', '身份证号码不规范。')
        return cd
