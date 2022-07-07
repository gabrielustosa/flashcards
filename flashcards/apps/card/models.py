import tempfile

from django.conf import settings
from django.core.files import File
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from flashcards.apps.core.models import UrlBase, TimeStampedBase, CreatorBase

from gtts import gTTS


class Word(UrlBase):
    word = models.CharField(_('Word'), max_length=100)
    audio_phonetic = models.FileField(_('Audio'), upload_to='phonetics/', null=True)
    for_language = models.CharField(_('Language'), max_length=7)
    synonyms = models.TextField(_('Synonyms'))

    def save(self, *args, **kwargs):
        if not self.audio_phonetic:
            audio = gTTS(text=self.word, lang='en', slow=True)

            with tempfile.TemporaryFile(mode='wb+') as file:
                audio.write_to_fp(file)
                file_name = f'{slugify(self.word)}.mp3'
                self.audio_phonetic.save(file_name, File(file=file))

            super().save(*args, **kwargs)

    def get_synonyms(self):
        return [synonym for synonym in self.synonyms.split('|')]

    def __str__(self):
        return self.word


class WordDefinition(models.Model):
    word = models.ForeignKey(
        Word,
        related_name='definitions',
        on_delete=models.CASCADE
    )
    headword_pos = models.CharField(_('Headword Pos'), max_length=100)
    headword_text = models.CharField(_('Headword Text'), max_length=100)
    for_language = models.CharField(_('Language'), max_length=5)
    definition = models.TextField(_('Definition'))


class WordMeaning(models.Model):
    word = models.ForeignKey(
        Word,
        related_name='meanings',
        on_delete=models.CASCADE
    )
    for_language = models.CharField(_('Language'), max_length=5)
    meaning = models.TextField(_('Meaning'))


class Card(UrlBase, TimeStampedBase, CreatorBase):
    language = models.CharField(_('Language'), max_length=5)
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE
    )
