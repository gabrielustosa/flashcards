from django.db import models
from django.db.models import Max
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from flashcards.apps.card.models import Card
from flashcards.apps.core.fields import OrderField
from flashcards.apps.core.models import UrlBase, TimeStampedBase, CreatorBase


class Deck(UrlBase, TimeStampedBase, CreatorBase):
    name = models.CharField(_('Name'), max_length=100)
    description = models.TextField(_('Description'))
    cards = models.ManyToManyField(
        Card,
        through='CardRelation',
        blank=True,
    )

    class Meta:
        ordering = ['id']

    def has_cards(self):
        print(self.cards.count())
        return 0 if self.cards.count() <= 1 else 1

    def get_last_order(self):
        return self.cards.aggregate(last_order=Max('cardrelation__order')).get('last_order')

    def get_absolute_url(self):
        return reverse('deck:view', kwargs={'deck_id': self.id})

    def __str__(self):
        return self.name


class CardRelation(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    order = OrderField(for_fields=['deck'])
