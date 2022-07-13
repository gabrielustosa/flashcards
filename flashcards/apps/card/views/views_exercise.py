from random import choice, shuffle

from django.http import JsonResponse
from django.shortcuts import render

from flashcards.apps.card.models import Word, WordUserMeaning, WordUserDefinition
from flashcards.apps.deck.models import Deck
from utils.util import sample_from_dict, shuffle_from_dict


def exercise_view(request, deck_id):
    # digitar significado TY
    # multipla escolha com signifcado MS
    # multipla escolha com exemplo ME
    deck = Deck.objects.filter(id=deck_id).first()

    exercises = ['TY', 'MS', 'ME']
    result = []

    multi_choice_enabled = deck.cards.count() >= 4

    for card in deck.cards.all():
        word = card.word

        run = True
        while run:
            exercise_choice = choice(exercises)
            if exercise_choice == 'TY' or exercise_choice == 'ME' and multi_choice_enabled:
                run = False
            if exercise_choice == 'MS' and multi_choice_enabled:
                word_definitions = list(word.definitions.all()) + list(
                    WordUserDefinition.objects.filter(user__id=deck.creator.id, word=word)
                )
                for definition in word_definitions:
                    if definition.example:
                        if word.word.lower() in definition.example.lower():
                            run = False
            if not run:
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

    deck_words = {card.id: card.word.word for card in deck.cards.all()}

    choices = sample_from_dict(deck_words, 3)

    while word_object.word in choices.values():
        choices = sample_from_dict(deck_words, 3)

    choices[word_object.id] = word_object.word

    choices = shuffle_from_dict(choices)

    return render(request, 'includes/card/exercise/multiple_meaning.html', context={
        'meanings': meanings,
        'choices': choices,
        'right_answer': f'{word_object.word}|{word_object.id}',
    })


def render_multiple_example(request, word_id, deck_id):
    deck = Deck.objects.filter(id=deck_id).first()
    word_object = Word.objects.filter(id=word_id).first()

    word_user_definitions = list(WordUserDefinition.objects.filter(user__id=deck.creator.id, word=word_object))

    examples = list(filter(None, [definition.example for definition in word_object.definitions.all()])) + [
        definition.example for definition in word_user_definitions]

    random_example = choice(examples).lower()

    word = word_object.word.lower()

    while word not in random_example:
        random_example = choice(examples).lower()

    if ' ' in word:  # phrasal verbs examples
        word_parts = word.split(' ')
        example_obfuscated = ''
        for example_word in random_example.replace('.', '').split(' '):
            if example_word in word_parts:
                example_word = ''.join(['_' for n in range(len(example_word))])
            example_obfuscated += example_word
            example_obfuscated += ' '
        random_example = example_obfuscated
    else:
        random_example = random_example.replace(word, ''.join(['_' for n in range(len(word))]))

    random_example = random_example.capitalize()

    deck_words = {card.id: card.word.word for card in deck.cards.all()}

    choices = sample_from_dict(deck_words, 3)

    while word_object.word in choices.values():
        choices = sample_from_dict(deck_words, 3)

    choices[word_object.id] = word_object.word

    choices = shuffle_from_dict(choices)
    return render(request, 'includes/card/exercise/multiple_example.html', context={
        'example': random_example,
        'choices': choices,
        'right_answer': f'{word_object.word}|{word_object.id}',
    })
