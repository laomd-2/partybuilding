from new_party.forms import DateCheckModelForm
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
        if id_card is None:
            id_card = self.instance.id_card_number
            if id_card:
                if 'birth_date' in cd:
                    if id_card[6:14] != str(cd.get('birth_date')).replace('-', ''):
                        self.add_error('birth_date', '出生日期与身份证号码不对应。')
                if 'gender' in cd:
                    if (int(id_card[-2]) & 1) == (int(cd.get('gender') != '男') & 1):
                        self.add_error('gender', '性别与身份证号码不对应。')
        else:
            if not eighteen.match(id_card):
                self.add_error('id_card_number', '身份证号码不规范。')
            if id_card[6:14] != str(cd.get('birth_date', self.instance.birth_date)).replace('-', ''):
                self.add_error('id_card_number', '出生日期不对应。')
            if (int(id_card[-2]) & 1) == (int(cd.get('gender', self.instance.gender) != '男') & 1):
                self.add_error('id_card_number', '性别不对应。')
        return cd
