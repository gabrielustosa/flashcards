from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from flashcards.apps.card.models import Card, WordTranslated
from flashcards.apps.deck.models import CardRelation, Deck


class FlashCardView(TemplateView):
    template_name = 'includes/card/flashcard/front.html'

    def get_context_data(self, **kwargs):
        context = super(FlashCardView, self).get_context_data(**kwargs)

        deck = Deck.objects.filter(id=self.kwargs.get('deck_id')).first()

        card_relation = CardRelation.objects.filter(deck=deck, order=self.kwargs.get('order')).first()

        card = card_relation.card

        cnt_type = self.kwargs.get('cnt_type')
        if cnt_type == 'word':
            context['card'] = card.item.word

        context['deck'] = deck

        return context


def turn_card_view(request, card_id):
    card = Card.objects.filter(id=card_id).first()

    side = request.GET.get('side')

    if side == 'front':
        return render(request, 'includes/card/flashcard/front.html', context={'card': card.item.word})

    meanings = WordTranslated.objects.filter(word=card.item.word).all()
    return render(request, 'includes/card/flashcard/back.html', context={'card': card, 'meanings': meanings})


def card_remove_view(request, order, deck_id):
    deck = Deck.objects.filter(id=deck_id).first()

    card = CardRelation.objects.filter(deck=deck, order=order).first().card

    deck.cards.remove(card)

    previous_card = None

    if order > 1:
        previous_order = order - 1
        previous_card = CardRelation.objects.filter(deck=deck, order=previous_order).first().card

    context = {}

    if previous_card:
        context.update({'card': previous_card.item.word})

    return render(request, 'includes/card/flashcard/front.html', context=context)
