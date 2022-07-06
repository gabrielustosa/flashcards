from django.contrib import admin

from flashcards.apps.card.models import Card, WordMeaning, WordDefinition, Word

admin.site.register(Card)

admin.site.register(WordMeaning)
admin.site.register(Word)
admin.site.register(WordDefinition)
