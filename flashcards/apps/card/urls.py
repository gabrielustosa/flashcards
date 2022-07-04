from django.urls import path

from . import views

app_name = 'card'

urlpatterns = [
    path('view/<str:cnt_type>/<int:card_id>/', views.FlashCardView.as_view(), name='view'),
]
