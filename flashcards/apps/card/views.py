from django.db.models import F, ExpressionWrapper, PositiveIntegerField
from django.shortcuts import render
from django.views.generic import TemplateView

from flashcards.apps.card.models import Card, WordMeaning
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


def turn_card_view(request, order, deck_id):
    deck = Deck.objects.filter(id=deck_id).first()

    card = CardRelation.objects.filter(deck=deck, order=order).first().card

    side = request.GET.get('side')

    if side == 'front':
        return render(request, 'includes/card/flashcard/front.html', context={'card': card.item.word, 'deck': deck})

    meanings = WordMeaning.objects.filter(word=card.item.word).all()
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
        context.update({'card': new_card.item.word})

    CardRelation.objects.filter(deck=deck, order__gt=order).update(
        order=ExpressionWrapper(F('order') - 1, output_field=PositiveIntegerField))

    return render(request, 'includes/card/flashcard/front.html', context=context)
