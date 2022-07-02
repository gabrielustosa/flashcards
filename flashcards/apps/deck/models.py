from django.db import models
from django.utils.translation import gettext_lazy as _

from flashcards.apps.core.models import UrlBase, TimeStampedBase, CreatorBase


class Deck(UrlBase, TimeStampedBase, CreatorBase):
    name = models.CharField(_('Name'), max_length=100)
    description = models.TextField(_('Description'))

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name
