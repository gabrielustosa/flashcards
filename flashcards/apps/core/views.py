from django.views.generic import TemplateView

from flashcards.apps.deck.models import Deck


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['decks'] = Deck.objects.all()

        return context
