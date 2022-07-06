from django.urls import path

from . import views

app_name = 'card'

urlpatterns = [
    path('view/<int:order>/<int:deck_id>/', views.FlashCardView.as_view(), name='view'),
    path('turn/<int:order>/<int:deck_id>/', views.turn_card_view, name='turn'),
    path('remove/<int:order>/<int:deck_id>/', views.card_remove_view, name='remove'),
    path('add/<int:deck_id>/', views.add_card, name='add')
]
