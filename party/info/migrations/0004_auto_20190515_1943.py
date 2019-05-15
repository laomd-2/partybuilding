# Generated by Django 2.2.1 on 2019-05-15 19:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('info', '0003_auto_20190515_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='branch',
            field=models.ForeignKey(on_delete=models.SET(106), to='info.Branch', verbose_name='党支部名称'),
        ),
        migrations.AlterField(
            model_name='oldmember',
            name='branch',
            field=models.ForeignKey(on_delete=models.SET(106), to='info.Branch', verbose_name='党支部名称'),
        ),
    ]
