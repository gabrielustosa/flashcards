from django.db import models
from django.utils.translation import gettext_lazy as _

from flashcards.apps.core.models import UrlBase, TimeStampedBase, CreatorBase
from flashcards.apps.user.models import User


class Word(UrlBase):
    word = models.CharField(_('Word'), max_length=100)
    audio_phonetic = models.URLField(_('Audio'))
    synonyms = models.TextField(_('Synonyms'), null=True)

    def get_synonyms(self):
        return [synonym.capitalize() for synonym in self.synonyms.split('|')]

    def get_synonyms_list(self):
        return ', '.join(self.get_synonyms())

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
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE
    )


class WordUserMeaning(models.Model):
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    meanings = models.TextField(_('Meanings'))

    def get_meanings(self):
        return [meaning.capitalize() for meaning in self.meanings.split('|')]

    def get_meanings_list(self):
        return ', '.join(self.get_meanings())


class WordUserDefinition(models.Model):
    POS_TAG_CHOICES = (
        ('Adjective', 'Adjective'),
        ('Adverb', 'Adverb'),
        ('Conjunction', 'Conjunction'),
        ('Determiner', 'Determiner'),
        ('Modal', 'Modal'),
        ('Noun', 'Noun'),
        ('Preposition', 'Preposition'),
        ('Pronoun', 'Pronoun'),
        ('Verb', 'Verb'),
        ('Other', 'Other'),
    )
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    pos_tag = models.CharField(_('Pos Tag'), max_length=15, choices=POS_TAG_CHOICES)
    definition = models.TextField(_('Definition'))
    example = models.TextField(_('Example'), null=True)
