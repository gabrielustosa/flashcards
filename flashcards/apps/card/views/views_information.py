from django.forms import modelform_factory
from django.shortcuts import render

from flashcards.apps.card.models import Word, WordUserMeaning, WordUserDefinition
from flashcards.apps.core.decorators import deck_creator_required
from flashcards.apps.deck.models import Deck


def information_view(request, deck_id):
    deck = Deck.objects.filter(id=deck_id).prefetch_related('cards__word', 'creator').first()

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

    user_definitions = WordUserDefinition.objects.filter(user__id=creator_id, word=word).all()

    meaning = WordUserMeaning.objects.filter(word=word, user__id=creator_id).first()

    return render(request, 'includes/card/information/word_information.html', context={
        'word': word,
        'word_definitions': user_definitions,
        'word_meanings': meaning,
        'creator_id': creator_id,
    })


@deck_creator_required()
def render_add_definition_view(request, word_id, creator_id):
    form = modelform_factory(WordUserDefinition, fields=['pos_tag', 'definition', 'example'])
    word = Word.objects.filter(id=word_id).first()

    return render(request, 'includes/card/information/definition/add_definition.html', context={
        'word': word,
        'form': form,
        'creator_id': creator_id,
    })


@deck_creator_required()
def add_definition_view(request, word_id, creator_id):
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

    return information_word_view(request, creator_id, word.id)


@deck_creator_required()
def render_edit_information_view(request, word_id, creator_id):
    word = Word.objects.filter(id=word_id).first()

    user_definitions = WordUserDefinition.objects.filter(user__id=creator_id, word=word).all()

    return render(request, 'includes/card/information/edit_information.html', context={
        'word': word,
        'word_definitions': user_definitions,
        'creator_id': creator_id,
    })


@deck_creator_required()
def remove_definition_view(request, word_id, creator_id, definition_id):
    WordUserDefinition.objects.filter(id=definition_id).delete()
    return render_edit_information_view(request, word_id, creator_id)


@deck_creator_required()
def render_edit_definition_view(request, word_id, creator_id, definition_id):
    word = Word.objects.filter(id=word_id).first()
    word_definition = WordUserDefinition.objects.filter(id=definition_id).first()

    form = modelform_factory(WordUserDefinition, fields=['pos_tag', 'definition', 'example'])(instance=word_definition)

    return render(request, 'includes/card/information/definition/edit_definition.html', context={
        'word': word,
        'word_definition_id': word_definition.id,
        'creator_id': creator_id,
        'form': form,
    })


@deck_creator_required()
def edit_definition_view(request, word_id, creator_id, definition_id):
    word_definition = WordUserDefinition.objects.filter(id=definition_id).first()

    pos_tag = request.POST.get('pos_tag')
    definition = request.POST.get('definition')
    example = request.POST.get('example')

    word_definition.pos_tag = pos_tag
    word_definition.definition = definition
    word_definition.example = example

    word_definition.save()

    return render_edit_information_view(request, word_id, creator_id)
