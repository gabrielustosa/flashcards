from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from flashcards.apps.card.models import Card
from flashcards.apps.core.fields import OrderField
from flashcards.apps.core.models import UrlBase, TimeStampedBase, CreatorBase


class Deck(UrlBase, TimeStampedBase, CreatorBase):
    name = models.CharField(_('Name'), max_length=100)
    language = models.CharField(_('Language'), max_length=5, choices=settings.WORD_LANGUAGES)
    cards = models.ManyToManyField(
        Card,
        through='CardRelation',
        blank=True,
    )

    class Meta:
        ordering = ['id']

    def get_first_card(self):
        try:
            return CardRelation.objects.filter(deck=self).order_by('order').first().card
        except Exception:
            pass

    def get_last_order(self):
        try:
            return CardRelation.objects.filter(deck=self).order_by('order').last().order
        except Exception:
            pass

    def get_absolute_url(self):
        return reverse('deck:view', kwargs={'deck_id': self.id})

    def __str__(self):
        return self.name


class CardRelation(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    order = OrderField(for_fields=['deck'])
