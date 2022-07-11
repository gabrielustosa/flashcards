from django.urls import path

from . import views

app_name = 'deck'

urlpatterns = [
    path('visualizar/<int:deck_id>/', views.deck_view, name='view'),
    path('criar/', views.DeckCreateView.as_view(), name='create'),
]
