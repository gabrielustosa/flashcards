from django.forms import modelform_factory
from django.shortcuts import render

from flashcards.apps.card.models import Word, WordUserMeaning, WordUserDefinition
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
    user_definitions = WordUserDefinition.objects.filter(user__id=creator_id, word=word).all()

    meaning = WordUserMeaning.objects.filter(word=word, user__id=creator_id).first()

    return render(request, 'includes/card/information/word_information.html', context={
        'word': word,
        'word_definitions': list(definitions) + list(user_definitions),
        'word_meanings': meaning,
    })


def render_add_information_view(request, word_id):
    form = modelform_factory(WordUserDefinition, fields=['pos_tag', 'definition', 'example'])
    word = Word.objects.filter(id=word_id).first()

    return render(request, 'includes/card/information/add_information.html', context={
        'word': word,
        'form': form
    })


def add_information_view(request, word_id):
    word = Word.objects.filter(id=word_id).first()

    pos_tag = request.POST.get('pos_tag')
    definition = request.POST.get('definition')
    example = request.POST.get('example')

    WordUserDefinition.objects.create(
        pos_tag=pos_tag,
        definition=definition,
        example=example,
        word=word,
        user=request.user
    )

    return information_word_view(request, request.user.id, word.id)
