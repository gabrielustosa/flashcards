from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as views_login

from flashcards.apps.user.views import UserRegisterView
from flashcards.apps.core.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),

    path("__reload__/", include("django_browser_reload.urls")),

    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', views_login.LoginView.as_view(), name='login'),
    path('logout/', views_login.LogoutView.as_view(), name='logout'),

    path('deck/', include('flashcards.apps.deck.urls')),
    path('card/', include('flashcards.apps.card.urls')),

    path('', HomeView.as_view(), name='home')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
