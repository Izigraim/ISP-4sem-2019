# Generated by Django 2.2 on 2019-05-28 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_auto_20190528_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='popularity',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9),
        ),
    ]
