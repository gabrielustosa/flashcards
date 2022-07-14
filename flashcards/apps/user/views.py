from django.contrib.auth import authenticate, login
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from flashcards.apps.user.forms import UserCreateForm


class UserRegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        raise PermissionDenied()

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(
            username=cd['username'],
            password=cd['password1']
        )
        login(request=self.request, user=user)
        return result


def add_right_answer(request):
    user = request.user
    user.right_answers += 1
    user.save()
    return JsonResponse({'status': 'ok'})
