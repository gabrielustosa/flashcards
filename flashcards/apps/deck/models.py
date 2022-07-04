from django.db import models
from django.utils.translation import gettext_lazy as _

from flashcards.apps.core.models import UrlBase, TimeStampedBase, CreatorBase

DECK_TYPES = (
    ('word', _('Word')),
    ('normal', _('Normal')),
    ('phrasal', _('Phrasal Verbs')),
    ('expressions', _('Popular Expressions')),
)


class Deck(UrlBase, TimeStampedBase, CreatorBase):
    name = models.CharField(_('Name'), max_length=100)
    deck_type = models.CharField(_('Deck type'), max_length=11, choices=DECK_TYPES)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name
