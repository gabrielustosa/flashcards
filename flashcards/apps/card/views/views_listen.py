from random import shuffle

from django.http import JsonResponse
from django.shortcuts import render

from flashcards.apps.card.models import Word
from flashcards.apps.deck.models import CardRelation, Deck


def listen_view(request, deck_id):
    last_relation = CardRelation.objects.filter(deck__id=deck_id).order_by('order').last()

    listen_order = []
    for i in range(1, last_relation.order):
        listen_order.append(i)
    shuffle(listen_order)

    deck = Deck.objects.filter(id=deck_id).first()

    return render(request, 'includes/card/listen/view.html', context={'listen_order': listen_order, 'deck': deck})


def listen_word_view(request, deck_id, order):
    card_relation = CardRelation.objects.filter(deck__id=deck_id, order=order).first()

    return render(request, 'includes/card/listen/listen_word.html', context={'word': card_relation.card.word})


def listen_verify_view(request, word_id):
    answer = request.GET.get('answer').lower()

    word_object = Word.objects.filter(id=word_id).first()

    correct = word_object.word.lower() == answer

    return JsonResponse({'correct': correct, 'word': word_object.word})
