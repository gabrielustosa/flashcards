# Generated by Django 4.0.5 on 2022-07-09 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0004_alter_card_language_alter_wordmeaning_for_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordusermeaning',
            name='meanings',
            field=models.TextField(default='a', verbose_name='Meanings'),
            preserve_default=False,
        ),
    ]