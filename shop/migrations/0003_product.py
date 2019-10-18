# Generated by Django 2.1.7 on 2019-04-01 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_brand'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('slug', models.SlugField()),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('available', models.BooleanField(default=True)),
                ('brand', models.ForeignKey(on_delete='', to='shop.Brand')),
                ('category', models.ForeignKey(on_delete='', to='shop.Category')),
            ],
        ),
    ]
