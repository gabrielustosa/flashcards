# Generated by Django 4.0.5 on 2022-07-05 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='card',
            options={},
        ),
        migrations.RemoveField(
            model_name='card',
            name='order',
        ),
    ]