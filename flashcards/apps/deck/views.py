from django.views.generic import TemplateView

from flashcards.apps.deck.models import Deck


class DeckView(TemplateView):
    template_name = 'deck/view.html'

    def get_context_data(self, **kwargs):
        context = super(DeckView, self).get_context_data(**kwargs)

        deck_id = self.kwargs.get('deck_id')

        deck = Deck.objects.filter(id=deck_id).first()

        context['deck'] = deck

        cnt_type = self.kwargs.get('cnt_type')
        if cnt_type == 'word':
            context['card'] = deck.get_first_card().item.word

        return context
