# Generated by Django 2.2 on 2019-05-19 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_delete_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=20, null=True)),
                ('comment', models.TextField(max_length=1000, null=True)),
            ],
        ),
    ]
