from django.urls import path

from . import views

app_name = 'card'

urlpatterns = [
    path('view/<int:order>/<int:deck_id>/', views.card_view, name='view'),
    path('change/<int:order>/<int:deck_id>/', views.change_card_view, name='change'),
    path('turn/<int:order>/<int:deck_id>/', views.turn_card_view, name='turn'),
    path('remove/<int:order>/<int:deck_id>/', views.card_remove_view, name='remove'),
    path('add/<int:deck_id>/', views.add_card, name='add'),
    path('edit/<int:order>/<int:deck_id>/', views.edit_card, name='edit'),
    path('remove_meaning/<int:word_id>/', views.remove_meaning, name='remove_meaning'),
    path('add_meaning/<int:word_id>/', views.add_meanning, name='add_meaning'),
]
