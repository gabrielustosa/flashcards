from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from flashcards.apps.card.forms import CardForm
from flashcards.apps.deck.models import Deck


class DeckView(TemplateView):
    template_name = 'deck/view.html'

    def get_context_data(self, **kwargs):
        context = super(DeckView, self).get_context_data(**kwargs)

        deck_id = self.kwargs.get('deck_id')

        deck = Deck.objects.filter(id=deck_id).first()

        context['deck'] = deck

        card = None
        if deck.get_first_card():
            card = deck.get_first_card().word
        context['card'] = card

        context['add_form'] = CardForm()

        context['current_card_number'] = 1 if card else 0

        return context


class DeckCreateView(CreateView):
    template_name = 'deck/create.html'
    model = Deck
    fields = ['name', 'description']
    success_url = reverse_lazy('home')
