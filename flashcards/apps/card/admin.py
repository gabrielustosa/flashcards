from django.contrib import admin

from flashcards.apps.card.models import Card, WordMeaning, WordDefinition, Word, WordUserMeaning

admin.site.register(Card)

admin.site.register(WordMeaning)
admin.site.register(Word)
admin.site.register(WordDefinition)
admin.site.register(WordUserMeaning)
