# Generated by Django 3.0.3 on 2020-05-12 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travello', '0003_auto_20200430_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='destination',
            name='typeofplace',
            field=models.CharField(default='beach', max_length=200),
            preserve_default=False,
        ),
    ]