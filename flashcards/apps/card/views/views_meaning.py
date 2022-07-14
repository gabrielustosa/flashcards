from django.shortcuts import render

from flashcards.apps.card.models import WordUserMeaning
from flashcards.apps.core.decorators import deck_creator_required


@deck_creator_required()
def remove_meaning_view(request, word_id, deck_id):
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
                      'deck_id': deck_id,
                  })


@deck_creator_required()
def add_meanning_view(request, word_id, deck_id):
    word_meanings = WordUserMeaning.objects.filter(word__id=word_id, user=request.user).first()

    word = request.POST.get('word')

    meanings = word_meanings.get_meanings()

    if word != "" and word.capitalize() not in meanings:
        meanings.append(word)
        meanings = '|'.join(meanings)

        word_meanings.meanings = meanings
        word_meanings.save()

    return render(request, 'includes/card/flashcard/meaning_list.html',
                  context={
                      'word': word_meanings.word,
                      'word_meanings': word_meanings,
                      'deck_id': deck_id,
                  })
