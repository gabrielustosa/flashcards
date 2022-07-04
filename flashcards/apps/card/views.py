from django.views.generic import TemplateView

from flashcards.apps.card.models import Card


class FlashCardView(TemplateView):
    template_name = 'includes/deck/flashcard.html'

    def get_context_data(self, **kwargs):
        context = super(FlashCardView, self).get_context_data(**kwargs)

        card = Card.objects.filter(id=self.kwargs.get('card_id')).first()

        cnt_type = self.kwargs.get('cnt_type')
        if cnt_type == 'word':
            context['card'] = card.item.word

        context['deck'] = card.deck

        return context


def turn_card_view(request, card_id):
    card = Card.objects.filter(id=card_id).first()


