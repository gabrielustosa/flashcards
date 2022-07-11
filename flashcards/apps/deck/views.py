from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from flashcards.apps.card.forms import CardForm
from flashcards.apps.deck.models import Deck


def deck_view(request, deck_id):
    deck = Deck.objects.filter(id=deck_id).first()

    context = {
        'deck': deck,
        'add_form': CardForm()
    }

    return render(request, 'deck/view.html', context=context)


class DeckCreateView(CreateView):
    template_name = 'deck/create.html'
    model = Deck
    fields = ['name', 'description']
    success_url = reverse_lazy('home')
