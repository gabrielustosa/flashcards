# Generated by Django 4.0.5 on 2022-07-07 20:42

import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone
import flashcards.apps.user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='E-mail')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Staff')),
                ('language', models.CharField(choices=[('af', 'Afrikaans'), ('ar', 'Arabic'), ('bn', 'Bangla'), ('bg', 'Bulgarian'), ('ca', 'Catalan'), ('hr', 'Croatian'), ('cs', 'Czech'), ('da', 'Danish'), ('nl', 'Dutch'), ('en', 'English'), ('fi', 'Finnish'), ('fr', 'French'), ('de', 'German'), ('el', 'Greek'), ('he', 'Hebrew'), ('hi', 'Hindi'), ('hu', 'Hungarian'), ('is', 'Icelandic'), ('id', 'Indonesian'), ('it', 'Italian'), ('ja', 'Japanese'), ('ko', 'Korean'), ('lv', 'Latvian'), ('lt', 'Lithuanian'), ('ms', 'Malay'), ('nb', 'Norwegian'), ('fa', 'Persian'), ('pl', 'Polish'), ('pt-br', 'Portuguese Brazilian'), ('pt-pt', 'Portuguese'), ('ro', 'Romanian'), ('ru', 'Russian'), ('sr-Latn', 'Serbian'), ('sk', 'Slovak'), ('sl', 'Slovenian'), ('es', 'Spanish'), ('sw', 'Swahili'), ('sv', 'Swedish'), ('th', 'Thai'), ('tr', 'Turkish'), ('uk', 'Ukrainian'), ('ur', 'Urdu'), ('vi', 'Vietnamese'), ('cy', 'Welsh')], max_length=7, verbose_name='Language')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', flashcards.apps.user.models.UserManager()),
            ],
        ),
    ]
