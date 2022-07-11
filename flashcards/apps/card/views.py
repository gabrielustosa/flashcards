from django.db.models import F, ExpressionWrapper, PositiveIntegerField
from django.shortcuts import render

from flashcards.apps.card.forms import CardForm
from flashcards.apps.card.models import WordMeaning, Word, WordDefinition, Card, WordUserMeaning
from flashcards.apps.deck.models import CardRelation, Deck

from utils.audio import get_word_phonetic

from utils.translation import get_word_definitions, get_word_meanigs, get_text_translated


def card_view(request, order, deck_id):
    deck = Deck.objects.filter(id=deck_id).first()

    card = None
    current_card_order = 0

    card_relation = CardRelation.objects.filter(deck=deck, order=order).first()

    if card_relation:
        card = card_relation.card.word
        current_card_order = card_relation.order

    return render(request, 'includes/card/flashcard.html', context={
        'deck': deck,
        'card': card,
        'current_card_order': current_card_order,
    })


def change_card_view(request, order, deck_id):
    deck = Deck.objects.filter(id=deck_id).first()

    card_relation = CardRelation.objects.filter(deck=deck, order=order).first()

    card = None
    if card_relation:
        card = card_relation.card

    context = {
        'card': card.word,
        'deck': deck
    }

    return render(request, 'includes/card/flashcard/front.html', context=context)


def turn_card_view(request, order, deck_id):
    deck = Deck.objects.filter(id=deck_id).first()

    card = CardRelation.objects.filter(deck=deck, order=order).first().card

    side = request.GET.get('side')

    if side == 'front':
        return render(request, 'includes/card/flashcard/front.html', context={
            'card': card.word,
            'deck': deck,
        })

    word_meanings = WordUserMeaning.objects.filter(word=card.word, user=deck.creator).first()

    return render(request, 'includes/card/flashcard/back.html', context={
        'card': card,
        'word_meanings': word_meanings
    })


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

    return card_view(request, new_order, deck_id)


def add_card(request, deck_id):
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
            word_definitions_objects = []

            for result in result_definitions.get('meaning'):
                pos_tag = result.get('partOfSpeech')
                for definition_result in result.get('definitions'):
                    definition = definition_result.get('definition')
                    example = None
                    if definition_result.get('example'):
                        example = definition_result.get('example')
                    word_definitions_objects.append(WordDefinition(
                        word=word_object,
                        pos_tag=pos_tag,
                        definition=definition,
                        example=example
                    ))
            WordDefinition.objects.bulk_create(word_definitions_objects)

        word_meaning = WordMeaning.objects.create(word=word_object, for_language=user_langauge, meanings=meanings)
        WordUserMeaning.objects.create(word=word_object, user=request.user, meanings=word_meaning.meanings)

    card = Card.objects.create(word=word_object)

    deck.cards.add(card)

    order = CardRelation.objects.filter(deck=deck, card=card).first().order

    return card_view(request, order, deck_id)


def edit_card(request, order, deck_id):
    deck = Deck.objects.filter(id=deck_id).first()

    card = CardRelation.objects.filter(deck=deck, order=order).first().card

    word_meanings = WordUserMeaning.objects.filter(word=card.word, user=deck.creator).first()

    edit_form = CardForm()

    return render(request, 'includes/card/flashcard/edit.html',
                  context={
                      'word': card.word,
                      'word_meanings': word_meanings,
                      'edit_form': edit_form
                  })


def remove_meaning(request, word_id):
    word_meanings = WordUserMeaning.objects.filter(word__id=word_id, user=request.user).first()

    value = int(request.GET.get('value'))
    meanings = word_meanings.get_meanings()

    meanings.pop(value)
    meanings = '|'.join(meanings)

    word_meanings.meanings = meanings
    word_meanings.save()

    return render(request, 'includes/card/flashcard/meaning_list.html',
                  context={
                      'word': word_meanings.word,
                      'word_meanings': word_meanings,
                  })


def add_meanning(request, word_id):
    word_meanings = WordUserMeaning.objects.filter(word__id=word_id, user=request.user).first()

    word = request.POST.get('word')

    meanings = word_meanings.get_meanings()

    if word != "" and word not in meanings:
        meanings.append(word)
        meanings = '|'.join(meanings)

        word_meanings.meanings = meanings
        word_meanings.save()

    return render(request, 'includes/card/flashcard/meaning_list.html',
                  context={
                      'word': word_meanings.word,
                      'word_meanings': word_meanings,
                  })
