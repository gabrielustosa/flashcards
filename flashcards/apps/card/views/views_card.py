from django.shortcuts import render

from flashcards.apps.card.models import WordUserMeaning
from flashcards.apps.deck.models import CardRelation, Deck


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
