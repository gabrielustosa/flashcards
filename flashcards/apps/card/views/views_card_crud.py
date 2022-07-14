from django.db.models import F, ExpressionWrapper, PositiveIntegerField
from django.shortcuts import render

from flashcards.apps.card.forms import CardForm
from flashcards.apps.card.models import WordMeaning, Word, WordDefinition, Card, WordUserMeaning, WordUserDefinition
from flashcards.apps.card.views.views_card import card_view
from flashcards.apps.core.decorators import deck_creator_required
from flashcards.apps.deck.models import CardRelation, Deck

from utils.audio import get_word_phonetic

from utils.translation import get_word_definitions, get_word_meanigs, get_text_translated


@deck_creator_required()
def card_remove_view(request, order, deck_id):
    deck = Deck.objects.filter(id=deck_id).first()

    card_relation_query = CardRelation.objects.filter(deck=deck)

    card = card_relation_query.filter(order=order).first().card

    deck.cards.remove(card)

    card.delete()

    new_order = 0

    if order > 1:
        new_order = order - 1
    else:
        if deck.cards.count() > 0:
            new_order = 1

    card_relation_query.filter(order__gt=order).update(
        order=ExpressionWrapper(F('order') - 1, output_field=PositiveIntegerField)
    )

    WordUserMeaning.objects.filter(user=deck.creator, word=card.word).delete()
    WordUserDefinition.objects.filter(user=deck.creator, word=card.word).delete()

    return card_view(request, new_order, deck_id)


@deck_creator_required()
def add_card_view(request, deck_id):
    deck = Deck.objects.filter(id=deck_id).first()

    word = request.POST.get('word').strip().capitalize()

    user_langauge = request.user.language

    word_query = Word.objects.filter(word=word)

    if deck.cards.filter(word__word=word).exists():
        return card_view(request, 1, deck_id)

    if word_query.exists():
        word_object = word_query.first()

        meaning_query = WordMeaning.objects.filter(word=word_object, for_language=user_langauge)

        if meaning_query.exists():
            meaning = meaning_query.first()
            WordUserMeaning.objects.create(word=word_object, user=request.user, meanings=meaning.meanings)
        else:
            meanings = get_word_meanigs(word, user_langauge)

            if not meanings:
                meanings = get_text_translated(word, user_langauge)

            meaning = WordMeaning.objects.create(word=word_object, for_language=user_langauge, meanings=meanings)
            WordUserMeaning.objects.create(word=word_object, user=request.user, meanings=meaning.meanings)

    else:
        result_definitions = get_word_definitions(word)

        meanings = get_word_meanigs(word, user_langauge)

        if not meanings:
            meanings = get_text_translated(word, user_langauge)

        synonyms = None
        audio_phonetic = None
        if result_definitions:
            audio_phonetic = result_definitions.get('audio')
            synonyms = result_definitions.get('synonyms')

        if not audio_phonetic:
            audio_phonetic = get_word_phonetic(word)

        word_object = Word.objects.create(
            word=word,
            synonyms=synonyms,
            audio_phonetic=audio_phonetic
        )

        if result_definitions:
            for result in result_definitions.get('meaning'):
                pos_tag = result.get('partOfSpeech')
                for definition_result in result.get('definitions'):
                    definition = definition_result.get('definition')
                    example = definition_result.get('example')
                    if example:
                        if word.lower() not in example.lower():
                            example = None
                    WordDefinition.objects.create(
                        word=word_object,
                        pos_tag=pos_tag.capitalize(),
                        definition=definition,
                        example=example
                    )

        word_meaning = WordMeaning.objects.create(word=word_object, for_language=user_langauge, meanings=meanings)
        WordUserMeaning.objects.create(word=word_object, user=request.user, meanings=word_meaning.meanings)

    word_definitions = WordDefinition.objects.filter(word=word_object)

    for word_definition in word_definitions.all():
        WordUserDefinition.objects.create(
            word=word_object,
            user=request.user,
            pos_tag=word_definition.pos_tag,
            definition=word_definition.definition,
            example=word_definition.example,
        )

    card = Card.objects.create(word=word_object)

    deck.cards.add(card)

    order = CardRelation.objects.filter(deck=deck, card=card).first().order

    return card_view(request, order, deck_id)


@deck_creator_required()
def edit_card_view(request, order, deck_id):
    deck = Deck.objects.filter(id=deck_id).prefetch_related('creator').first()

    card = CardRelation.objects.filter(deck=deck, order=order).first().card

    word_meanings = WordUserMeaning.objects.filter(word=card.word, user=deck.creator).first()

    edit_form = CardForm()

    return render(request, 'includes/card/flashcard/edit.html',
                  context={
                      'word': card.word,
                      'word_meanings': word_meanings,
                      'edit_form': edit_form,
                      'deck_id': deck.id,
                  })
