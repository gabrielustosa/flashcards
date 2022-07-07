# Generated by Django 4.0.5 on 2022-07-07 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date and Time')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modification Date and Time')),
                ('language', models.CharField(max_length=5, verbose_name='Language')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100, verbose_name='Word')),
                ('audio_phonetic', models.FileField(null=True, upload_to='phonetics/', verbose_name='Audio')),
                ('for_language', models.CharField(max_length=7, verbose_name='Language')),
                ('synonyms', models.TextField(verbose_name='Synonyms')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WordMeaning',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('for_language', models.CharField(max_length=5, verbose_name='Language')),
                ('meaning', models.TextField(verbose_name='Meaning')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meanings', to='card.word')),
            ],
        ),
        migrations.CreateModel(
            name='WordDefinition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headword_pos', models.CharField(max_length=100, verbose_name='Headword Pos')),
                ('headword_text', models.CharField(max_length=100, verbose_name='Headword Text')),
                ('for_language', models.CharField(max_length=5, verbose_name='Language')),
                ('definition', models.TextField(verbose_name='Definition')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='definitions', to='card.word')),
            ],
        ),
    ]
