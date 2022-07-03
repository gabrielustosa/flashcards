import tempfile

from django.core.files import File
from django.db import models
from django.utils.translation import gettext_lazy as _

from gtts import gTTS

from flashcards.apps.core.models import UrlBase

WORD_LANGUAGES = [
    ('ar', 'Arabic'),
    ('zh', 'Simplified Chinese'),
    ('zh-tw', 'Traditional Chinese'),
    ('cs', 'Czech'),
    ('da', 'Danish'),
    ('nl', 'Dutc'),
    ('en', 'English'),
    ('fr', 'French'),
    ('de', 'German'),
    ('el', 'Greek'),
    ('iw', 'Hebrew'),
    ('hi', 'Hindi'),
    ('it', 'Italian'),
    ('ja', 'Japanese'),
    ('ko', 'Korean'),
    ('la', 'Latin'),
    ('no', 'Norwegian'),
    ('pl', 'Polish'),
    ('pt', 'Portuguese'),
    ('pt-br', 'Portuguese Brazilian'),
    ('ru', 'Russian'),
    ('es', 'Spanish'),
    ('sv', 'Swedish'),
    ('th', 'Thai'),
    ('tr', 'Turkish')
]

DIFERENT_OPTIONS = {
    'tw': 'zh-tw',
    'dk': 'da',
    'he': 'iw',
    'br': 'pt-br'
}


class Word(UrlBase):
    word = models.CharField(_('Word'), max_length=100)
    language = models.CharField(_('Language'), max_length=5)
    audio_phonetic = models.FileField(_('Audio'), upload_to='phonetics/', null=True)

    def save(self, *args, **kwargs):
        if not self.audio_phonetic:
            audio = gTTS(text=self.word, lang=self.language, slow=True)

            with tempfile.TemporaryFile(mode='w') as file:
                audio.write_to_fp(file)
                file_name = f'{self.word}.mp3'
                self.audio_phonetic.save(file_name, File(file=file))

            super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.word} - {self.language}'


class Meaning(models.Model):
    word = models.ForeignKey(
        Word,
        related_name='meanings',
        on_delete=models.CASCADE
    )
    headword = models.CharField(_('Headword'), max_length=100)
    definitions = models.TextField(_('Definitions'))

    def get_definitions(self):
        return [definition for definition in self.definitions.split('|')]


class WordTranslated(models.Model):
    word = models.ForeignKey(
        Word,
        related_name='translations',
        on_delete=models.CASCADE
    )
    for_language = models.CharField(_('Language'), max_length=5)
    meanings = models.TextField(_('Meanings'))

    def get_meanings(self):
        return [meaning for meaning in self.meanings.split('|')]
