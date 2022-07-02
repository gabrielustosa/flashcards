from django.db import models
from django.utils.translation import gettext_lazy as _

from flashcards.apps.card.models.word import Word
from flashcards.apps.core.fields import OrderField
from flashcards.apps.core.models import UrlBase, TimeStampedBase, CreatorBase
from flashcards.apps.deck.models import Deck


class Card(UrlBase, TimeStampedBase, CreatorBase):
    language = models.CharField(_('Language'), max_length=5)
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE
    )
    deck = models.ForeignKey(
        Deck,
        related_name='cards',
        on_delete=models.CASCADE
    )
    order = OrderField(for_fields=['deck'])
