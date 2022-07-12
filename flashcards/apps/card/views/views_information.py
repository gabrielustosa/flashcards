from django.shortcuts import render

from flashcards.apps.card.models import Word, WordUserMeaning
from flashcards.apps.deck.models import Deck


def information_view(request, deck_id):
    deck = Deck.objects.filter(id=deck_id).first()

    cards = deck.cards.all()

    return render(request, 'includes/card/information/view.html', context={
        'deck': deck,
        'cards': cards
    })


def search_word_view(request, deck_id):
    deck = Deck.objects.filter(id=deck_id).first()

    cards = deck.cards.all()

    search_term = request.POST.get('search')

    if search_term != "":
        cards = deck.cards.filter(word__word__icontains=search_term).all()

    return render(request, 'includes/card/information/word_list.html', context={
        'cards': cards,
        'deck': deck,
    })


def information_word_view(request, creator_id, word_id):
    word = Word.objects.filter(id=word_id).first()

    definitions = word.definitions.all()

    meaning = WordUserMeaning.objects.filter(word=word, user__id=creator_id).first()

    return render(request, 'includes/card/information/word_information.html', context={
        'word': word,
        'word_definitions': definitions,
        'word_meanings': meaning,
    })
