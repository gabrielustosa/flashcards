import tempfile

from django.core.files import File
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from gtts import gTTS

from flashcards.apps.core.models import UrlBase


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
    meaning = models.TextField(_('Meanings'))
