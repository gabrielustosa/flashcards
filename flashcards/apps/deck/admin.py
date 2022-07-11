from django.contrib import admin

from flashcards.apps.deck.models import Deck, CardRelation

admin.site.register(Deck)
admin.site.register(CardRelation)
