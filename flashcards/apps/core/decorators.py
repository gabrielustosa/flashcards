from functools import wraps

from django.core.exceptions import PermissionDenied

from flashcards.apps.deck.models import Deck
from flashcards.apps.user.models import User


def deck_creator_required():
    def decorator(func):
        @wraps(func)
        def _wrapped_view(request, *args, **kwargs):
            deck_id = kwargs.get('deck_id')
            if deck_id:
                deck = Deck.objects.filter(id=deck_id).first()
                if deck.creator != request.user:
                    raise PermissionDenied()

            creator_id = kwargs.get('creator_id')
            if creator_id:
                creator = User.objects.filter(id=creator_id).first()
                if request.user != creator:
                    raise PermissionDenied()

            return func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
