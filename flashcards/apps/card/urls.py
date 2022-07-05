from django.urls import path

from . import views

app_name = 'card'

urlpatterns = [
    path('view/<str:cnt_type>/<int:order>/<int:deck_id>/', views.FlashCardView.as_view(), name='view'),
    path('turn/<int:card_id>/', views.turn_card_view, name='turn'),
    path('remove/<int:order>/<int:deck_id>/', views.card_remove_view, name='remove')
]
