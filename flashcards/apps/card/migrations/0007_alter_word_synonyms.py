# Generated by Django 4.0.5 on 2022-07-10 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0006_remove_wordusermeaning_meaning_wordusermeaning_word'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='synonyms',
            field=models.TextField(null=True, verbose_name='Synonyms'),
        ),
    ]
