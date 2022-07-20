from random import choice, shuffle, randint

from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render

from flashcards.apps.card.models import WordUserMeaning, WordUserDefinition
from flashcards.apps.deck.models import Deck, CardRelation
from utils.util import shuffle_from_dict, escape, get_random_cards


def exercise_view(request, deck_id):
    # digitar significado TY
    # multipla escolha com signifcado MS
    # multipla escolha com exemplo ME
    deck = Deck.objects.filter(id=deck_id).annotate(total_cards=Count('cards')).first()
    last_relation = CardRelation.objects.filter(deck=deck).order_by('order').last()

    exercises_type = ['TY', 'MS', 'ME']
    result = []

    multi_choice_enabled = deck.total_cards >= 4

    if not multi_choice_enabled:
        exercises_type = ['TY']

    for order in range(1, last_relation.order + 1):
        exercise_choice = choice(exercises_type)
        result.append(f"{exercise_choice}-{order}")

    shuffle(result)

    return render(request, 'includes/card/exercise/view.html', context={'exercises_list': result, 'deck': deck})


def render_type_exercise(request, deck_id, order):
    card = CardRelation.objects.filter(deck__id=deck_id, order=order).first().card

    return render(request, 'includes/card/exercise/type.html', context={'word': card.word})


def verify_typing(request, word_id, deck_id):
    deck = Deck.objects.filter(id=deck_id).first()

    meanings = WordUserMeaning.objects.filter(word__id=word_id, user=deck.creator).first().meanings

    meanings = [meaning.lower() for meaning in meanings.split('|')]

    answer = request.GET.get('answer').strip().lower()

    correct = answer in meanings

    if correct:
        meanings.remove(answer)

    return JsonResponse({'correct': correct, 'meanings': meanings})


def render_multiple_meaning_exercise(request, deck_id, order):
    deck = Deck.objects.filter(id=deck_id).first()
    word_object = CardRelation.objects.filter(deck__id=deck_id, order=order).first().card.word

    word_meaning = WordUserMeaning.objects.filter(word=word_object, user=deck.creator).first()

    meanings = word_meaning.get_meanings_list()

    choices = {word_object.id: word_object.word}

    [choices.update({card.word.id: card.word.word}) for card in get_random_cards(deck.cards, not_equal=word_object.id, quantity=3)]

    choices = shuffle_from_dict(choices)

    return render(request, 'includes/card/exercise/multiple_meaning.html', context={
        'meanings': meanings,
        'choices': choices,
        'right_answer': f'{word_object.word}|{word_object.id}',
    })


def render_multiple_example(request, deck_id, order):
    deck = Deck.objects.prefetch_related('cards__word').filter(id=deck_id).first()
    word_object = CardRelation.objects.filter(deck__id=deck_id, order=order).first().card.word

    word_user_definitions = WordUserDefinition.objects.filter(user=deck.creator, word=word_object)

    examples = list(filter(None, [definition.example for definition in word_user_definitions]))

    if not examples:
        random_choice = randint(0, 1)
        if random_choice == 1:
            return render_multiple_meaning_exercise(request, deck_id, order)
        return render_type_exercise(request, deck_id, order)

    random_example = choice(examples)
    word = word_object.word

    random_example = escape(word, random_example)

    choices = {word_object.id: word_object.word}

    [choices.update({card.word.id: card.word.word}) for card in get_random_cards(deck.cards, not_equal=word_object.id, quantity=3)]

    choices = shuffle_from_dict(choices)

    return render(request, 'includes/card/exercise/multiple_example.html', context={
        'example': random_example,
        'choices': choices,
        'right_answer': f'{word_object.word}|{word_object.id}',
    })
