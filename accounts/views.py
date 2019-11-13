from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


class SignUpView(CreateView):
    """View for signups"""

    success_url = reverse_lazy('login')

    def get(self, request):
        """Get the signup page"""
        form_class = UserCreationForm
        return render(request, 'registration/signup.html', {'form': form_class})
