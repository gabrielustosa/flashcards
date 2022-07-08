from django.db import models
from django.utils.translation import gettext_lazy as _

from flashcards.apps.core.models import UrlBase, TimeStampedBase, CreatorBase
from flashcards.apps.user.models import User


class Word(UrlBase):
    word = models.CharField(_('Word'), max_length=100)
    audio_phonetic = models.URLField(_('Audio'), null=True)
    synonyms = models.TextField(_('Synonyms'))

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
    pos_tag = models.CharField(_('Pos Tag'), max_length=100)
    definition = models.TextField(_('Definition'))
    example = models.TextField(_('Example'), null=True)


class WordMeaning(models.Model):
    word = models.ForeignKey(
        Word,
        related_name='meanings',
        on_delete=models.CASCADE
    )
    for_language = models.CharField(_('Language'), max_length=7)
    meanings = models.TextField(_('Meanings'))


class Card(UrlBase, TimeStampedBase, CreatorBase):
    language = models.CharField(_('Language'), max_length=7)
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE
    )


class WordUserMeaning(models.Model):
    meaning = models.ForeignKey(
        WordMeaning,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def get_meanings(self):
        return [meaning for meaning in self.meaning.meanings.split('|')]
