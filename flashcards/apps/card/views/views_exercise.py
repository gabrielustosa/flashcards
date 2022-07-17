from random import choice, shuffle

from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import render

from flashcards.apps.card.models import Word, WordUserMeaning, WordUserDefinition
from flashcards.apps.deck.models import Deck
from utils.util import shuffle_from_dict, escape


def exercise_view(request, deck_id):
    # digitar significado TY
    # multipla escolha com signifcado MS
    # multipla escolha com exemplo ME
    deck = Deck.objects.filter(id=deck_id).prefetch_related('cards').annotate(total_cards=Count('cards')).first()

    exercises_type = ['TY', 'MS', 'ME']
    result = []

    multi_choice_enabled = deck.total_cards >= 4

    if not multi_choice_enabled:
        exercises_type = ['TY']

    for card in deck.cards.all():
        word = card.word

        exercise_choice = choice(exercises_type)
        result.append(f"{exercise_choice}-{word.id}")

    shuffle(result)

    return render(request, 'includes/card/exercise/view.html', context={'exercises_list': result, 'deck': deck})


def render_type_exercise(request, word_id):
    word_object = Word.objects.filter(id=word_id).first()

    return render(request, 'includes/card/exercise/type.html', context={'word': word_object})


def verify_typing(request, word_id, deck_id):
    deck = Deck.objects.filter(id=deck_id).first()

    meanings = WordUserMeaning.objects.filter(word__id=word_id, user=deck.creator).first().meanings

    meanings = [meaning.lower() for meaning in meanings.split('|')]

    answer = request.GET.get('answer').strip().lower()

    correct = answer in meanings

    if correct:
        meanings.remove(answer)

    return JsonResponse({'correct': correct, 'meanings': meanings})


def render_multiple_meaning_exercise(request, word_id, deck_id):
    deck = Deck.objects.filter(id=deck_id).first()
    word_object = Word.objects.filter(id=word_id).first()

    word_meaning = WordUserMeaning.objects.filter(word__id=word_id, user=deck.creator).first()

    meanings = word_meaning.get_meanings_list()

    choices = dict()

    choices[word_object.id] = word_object.word

    [choices.update({word.id: word.word}) for word in deck.cards.filter(~Q(word=word_object)).order_by('?')[:3]]

    choices = shuffle_from_dict(choices)

    return render(request, 'includes/card/exercise/multiple_meaning.html', context={
        'meanings': meanings,
        'choices': choices,
        'right_answer': f'{word_object.word}|{word_object.id}',
    })


def render_multiple_example(request, word_id, deck_id):
    deck = Deck.objects.prefetch_related('cards__word').filter(id=deck_id).first()
    word_object = Word.objects.filter(id=word_id).first()

    word_user_definitions = WordUserDefinition.objects.filter(user=deck.creator, word=word_object)

    examples = list(filter(None, [definition.example for definition in word_user_definitions]))

    if not examples:
        return render_type_exercise(request, word_id)

    random_example = choice(examples)
    word = word_object.word

    random_example = escape(word, random_example)

    choices = dict()

    choices[word_object.id] = word_object.word

    [choices.update({word.id: word.word}) for word in deck.cards.filter(~Q(word=word_object)).order_by('?')[:3]]

    choices = shuffle_from_dict(choices)

    return render(request, 'includes/card/exercise/multiple_example.html', context={
        'example': random_example,
        'choices': choices,
        'right_answer': f'{word_object.word}|{word_object.id}',
    })
