from django.db.models import F, ExpressionWrapper, PositiveIntegerField
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from flashcards.apps.card.models import WordMeaning, Word, WordDefinition, Card
from flashcards.apps.deck.models import CardRelation, Deck
from utils.translation import get_lexical_definitions, get_word_meanigs


class FlashCardView(TemplateView):
    template_name = 'includes/card/flashcard/front.html'

    def get_context_data(self, **kwargs):
        context = super(FlashCardView, self).get_context_data(**kwargs)

        deck = Deck.objects.filter(id=self.kwargs.get('deck_id')).first()

        card_relation = CardRelation.objects.filter(deck=deck, order=self.kwargs.get('order')).first()

        card = card_relation.card

        context['card'] = card.word

        context['deck'] = deck

        return context


def turn_card_view(request, order, deck_id):
    deck = Deck.objects.filter(id=deck_id).first()

    card = CardRelation.objects.filter(deck=deck, order=order).first().card

    side = request.GET.get('side')

    if side == 'front':
        return render(request, 'includes/card/flashcard/front.html', context={'card': card.word, 'deck': deck})

    meanings = WordMeaning.objects.filter(word=card.word).all()
    return render(request, 'includes/card/flashcard/back.html', context={'card': card, 'meanings': meanings})


def card_remove_view(request, order, deck_id):
    deck = Deck.objects.filter(id=deck_id).first()

    card = CardRelation.objects.filter(deck=deck, order=order).first().card

    deck.cards.remove(card)

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

    return render(request, 'includes/card/flashcard/front.html', context=context)


def add_card(request, deck_id):
    deck = Deck.objects.filter(id=deck_id).first()

    word = request.POST.get('word').capitalize()

    user_langauge = request.user.language

    word_query = Word.objects.filter(word=word, for_language=user_langauge)

    if word_query.exists():
        word_object = word_query.first()

        card = Card.objects.create(word=word_object)

        deck.cards.add(card)
    else:
        result_definitions = get_lexical_definitions(word, user_langauge)

        if not result_definitions:
            return redirect(reverse('deck:view', kwargs={'deck_id': deck_id}))

        result_meanings, synonyms = get_word_meanigs(word, user_langauge)

        word_object = Word.objects.create(word=word, for_language=user_langauge, synonyms=synonyms)

        for result in result_definitions:
            for headword, definitions in result.items():
                for definition in definitions:
                    headword_split = headword.split('-')
                    headword_pos = headword_split[0]
                    headword_text = headword_split[1]

                    WordDefinition.objects.create(
                        word=word_object,
                        headword_pos=headword_pos,
                        headword_text=headword_text,
                        for_language=user_langauge,
                        definition=definition
                    )

        for meaning in result_meanings:
            WordMeaning.objects.create(
                word=word_object,
                for_language=user_langauge,
                meaning=meaning
            )

        card = Card.objects.create(word=word_object)

        deck.cards.add(card)

    return redirect(reverse('deck:view', kwargs={'deck_id': deck_id}))
