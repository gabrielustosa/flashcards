# Generated by Django 4.0.5 on 2022-07-05 19:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('card', '0003_alter_card_options_remove_card_order'),
        ('deck', '0003_cardrelation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deck',
            name='cards',
        ),
        migrations.AddField(
            model_name='deck',
            name='cards',
            field=models.ManyToManyField(blank=True, through='deck.CardRelation', to='card.card'),
        ),
    ]
