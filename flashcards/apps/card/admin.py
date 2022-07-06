from django.contrib import admin

from flashcards.apps.card.models import Card, WordMeaning

admin.site.register(Card)

admin.site.register(WordMeaning)
