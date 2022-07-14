from functools import wraps

from django.core.exceptions import PermissionDenied

from flashcards.apps.deck.models import Deck


def deck_creator_required():
    def decorator(func):
        @wraps(func)
        def _wrapped_view(request, *args, **kwargs):
            deck = Deck.objects.filter(id=kwargs.get('deck_id')).first()
            if deck.creator != request.user:
                raise PermissionDenied()
            return func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
