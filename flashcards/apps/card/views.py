from django.db.models import F, ExpressionWrapper, PositiveIntegerField
from django.shortcuts import render, redirect
from django.urls import reverse

from flashcards.apps.card.forms import CardForm
from flashcards.apps.card.models import WordMeaning, Word, WordDefinition, Card, WordUserMeaning
from flashcards.apps.deck.models import CardRelation, Deck

from utils.audio import get_word_phonetic

from utils.translation import get_word_definitions, get_word_meanigs, get_text_translated


def card_view(request, order, deck_id):
    deck = Deck.objects.filter(id=deck_id).first()

    card_relation = CardRelation.objects.filter(deck=deck, order=order).first()

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
        return render(request, 'includes/card/flashcard/front.html', context={'card': card.word, 'deck': deck})

    word_meanings = WordUserMeaning.objects.filter(word=card.word, user=deck.creator).first()

    return render(request, 'includes/card/flashcard/back.html', context={'card': card, 'word_meanings': word_meanings})


def card_remove_view(request, order, deck_id):
    deck = Deck.objects.filter(id=deck_id).first()

    card = CardRelation.objects.filter(deck=deck, order=order).first().card

    deck.cards.remove(card)

    card.delete()

    new_card = None

    if order > 1:
        previous_order = order - 1
        new_card = CardRelation.objects.filter(deck=deck, order=previous_order).first().card

    if not new_card and CardRelation.objects.filter(deck=deck).exists():
        next_order = order + 1
        new_card = CardRelation.objects.filter(deck=deck, order=next_order).first().card

    context = {
        'deck': deck,
    }

    if new_card:
        context.update({'card': new_card.word})

    CardRelation.objects.filter(deck=deck, order__gt=order).update(
        order=ExpressionWrapper(F('order') - 1, output_field=PositiveIntegerField))

    WordUserMeaning.objects.filter(user=deck.creator, word=card.word).delete()

    return render(request, 'includes/card/flashcard/front.html', context=context)


def add_card(request, deck_id):
    deck = Deck.objects.filter(id=deck_id).first()

    word = request.POST.get('word').strip().capitalize()

    user_langauge = request.user.language

    word_query = Word.objects.filter(word=word)

    if WordUserMeaning.objects.filter(word__word=word, user=request.user).exists():
        return redirect(reverse('deck:view', kwargs={'deck_id': deck_id}))

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
            synonyms = '|'.join(result_definitions.get('synonyms'))

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

        meaning = WordMeaning.objects.create(word=word_object, for_language=user_langauge, meanings=meanings)
        WordUserMeaning.objects.create(word=word_object, user=request.user, meanings=meaning.meanings)

    card = Card.objects.create(word=word_object)

    deck.cards.add(card)

    return redirect(reverse('deck:view', kwargs={'deck_id': deck_id}))


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
