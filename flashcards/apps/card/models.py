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
    language = models.CharField(_('Language'), max_length=5)
    audio_phonetic = models.FileField(_('Audio'), upload_to='phonetics/', null=True)

    def save(self, *args, **kwargs):
        if not self.audio_phonetic:
            audio = gTTS(text=self.word, lang=self.language, slow=True)

            with tempfile.TemporaryFile(mode='wb+') as file:
                audio.write_to_fp(file)
                file_name = f'{slugify(self.word)}-{self.language}.mp3'
                self.audio_phonetic.save(file_name, File(file=file))

            super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.word} - {self.language}'


class WordDefinition(models.Model):
    word = models.ForeignKey(
        Word,
        related_name='definitions',
        on_delete=models.CASCADE
    )
    headword = models.CharField(_('Headword'), max_length=100)
    for_language = models.CharField(_('Language'), choices=settings.WORD_LANGUAGES, max_length=5)
    definition = models.TextField(_('Definition'))


class WordMeaning(models.Model):
    word = models.ForeignKey(
        Word,
        related_name='meanings',
        on_delete=models.CASCADE
    )
    for_language = models.CharField(_('Language'), choices=settings.WORD_LANGUAGES, max_length=5)
    meaning = models.TextField(_('Meaning'))


class Card(UrlBase, TimeStampedBase, CreatorBase):
    language = models.CharField(_('Language'), max_length=5)
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE
    )
