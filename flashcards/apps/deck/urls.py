from django.urls import path

from . import views

app_name = 'deck'

urlpatterns = [
    path('visualizar/<str:cnt_type>/<int:deck_id>/', views.DeckView.as_view(), name='view'),
]
