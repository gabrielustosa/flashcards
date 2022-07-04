from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from flashcards.apps.card.models.word import Word
from flashcards.apps.core.fields import OrderField
from flashcards.apps.core.models import UrlBase, TimeStampedBase, CreatorBase
from flashcards.apps.deck.models import Deck


class Card(models.Model):
    deck = models.ForeignKey(
        Deck,
        related_name='cards',
        on_delete=models.CASCADE
    )
    order = OrderField(for_fields=['deck'])

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={'model__in': (
            'cardword',
            'cardphrasalverb',
            'cardexpressions')}
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ('order',)


class CardWord(UrlBase, TimeStampedBase, CreatorBase):
    language = models.CharField(_('Language'), max_length=5)
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE
    )


class CardPhrasalVerb(UrlBase, TimeStampedBase, CreatorBase):
    pass


class CardExpression(UrlBase, TimeStampedBase, CreatorBase):
    pass
