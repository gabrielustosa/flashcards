from django.urls import path

from .views import views_card_crud, views_meaning, views_card, views_information

app_name = 'card'

urlpatterns = [
    path('view/<int:order>/<int:deck_id>/', views_card.card_view, name='view'),
    path('change/<int:order>/<int:deck_id>/', views_card.change_card_view, name='change'),
    path('turn/<int:order>/<int:deck_id>/', views_card.turn_card_view, name='turn'),

    path('remove/<int:order>/<int:deck_id>/', views_card_crud.card_remove_view, name='remove'),
    path('add/<int:deck_id>/', views_card_crud.add_card_view, name='add'),
    path('edit/<int:order>/<int:deck_id>/', views_card_crud.edit_card_view, name='edit'),

    path('remove_meaning/<int:word_id>/', views_meaning.remove_meaning_view, name='remove_meaning'),
    path('add_meaning/<int:word_id>/', views_meaning.add_meanning_view, name='add_meaning'),

    path('information/<int:deck_id>/', views_information.information_view, name='information'),
    path('search_word/<int:deck_id>/', views_information.search_word_view, name='search_word'),
    path('word_information/<int:creator_id>/<int:word_id>/', views_information.information_word_view, name='word_information'),

]
