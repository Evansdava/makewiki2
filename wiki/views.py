from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from wiki.models import Page, PageForm


class PageListView(ListView):
    """Renders a list of all Pages."""

    model = Page

    def get(self, request):
        """GET a list of Pages."""
        pages = self.get_queryset().all().order_by('-created')
        username = None
        auth = request.user.is_authenticated
        if auth:
            username = request.user.username
        return render(request, 'list.html', {
                      'pages': pages,
                      'username': username,
                      'auth': auth,
                      })


class PageDetailView(DetailView):
    """Renders a specific page based on it's slug."""

    model = Page

    def get(self, request, slug):
        """Returns a specific wiki page by slug."""
        page = self.get_queryset().get(slug__iexact=slug)
        username = None
        auth = request.user.is_authenticated
        if auth:
            username = request.user.username
        return render(request, 'page.html', {
                      'page': page,
                      'username': username,
                      'auth': auth,
                      })


class NewPageView(CreateView):
    """Returns a form for a new article"""

    template_name = 'new_article.html'
    form_class = PageForm
    success_url = reverse_lazy('wiki-list-page')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.save()
        return super().form_valid(form)
