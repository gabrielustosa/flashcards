from django.db.models import F, Value, CharField
from django.db.models.functions import Concat
from django.views.generic import TemplateView

from flashcards.apps.deck.models import Deck


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['decks'] = Deck.objects.annotate(
            url=Concat(Value('deck/visualizar/'), F('deck_type'), Value('/'), F('id'),
                       output_field=CharField())).all()
        if self.request.user.is_authenticated:
            context['my_decks'] = Deck.objects.filter(creator=self.request.user).annotate(
                url=Concat(Value('deck/visualizar/'), F('deck_type'), Value('/'), F('id'),
                           output_field=CharField()))

        return context
