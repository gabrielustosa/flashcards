# Generated by Django 4.0.5 on 2022-07-17 02:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100, verbose_name='Word')),
                ('audio_phonetic', models.URLField(verbose_name='Audio')),
                ('synonyms', models.TextField(null=True, verbose_name='Synonyms')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WordUserMeaning',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meanings', models.TextField(verbose_name='Meanings')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='card.word')),
            ],
        ),
        migrations.CreateModel(
            name='WordUserDefinition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pos_tag', models.CharField(choices=[('Adjective', 'Adjective'), ('Adverb', 'Adverb'), ('Conjunction', 'Conjunction'), ('Determiner', 'Determiner'), ('Modal', 'Modal'), ('Noun', 'Noun'), ('Preposition', 'Preposition'), ('Pronoun', 'Pronoun'), ('Verb', 'Verb'), ('Other', 'Other')], max_length=15, verbose_name='Pos Tag')),
                ('definition', models.TextField(verbose_name='Definition')),
                ('example', models.TextField(null=True, verbose_name='Example')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='card.word')),
            ],
        ),
        migrations.CreateModel(
            name='WordMeaning',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('for_language', models.CharField(max_length=7, verbose_name='Language')),
                ('meanings', models.TextField(verbose_name='Meanings')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meanings', to='card.word')),
            ],
        ),
        migrations.CreateModel(
            name='WordDefinition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pos_tag', models.CharField(max_length=100, verbose_name='Pos Tag')),
                ('definition', models.TextField(verbose_name='Definition')),
                ('example', models.TextField(null=True, verbose_name='Example')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='definitions', to='card.word')),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date and Time')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modification Date and Time')),
                ('creator', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='card.word')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
