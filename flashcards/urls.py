from django.contrib import admin
from django.urls import path, include

from flashcards.apps.core.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),

    path("__reload__/", include("django_browser_reload.urls")),

    path('', HomeView.as_view(), name='home')
]
