from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, TemplateView
from OnlyShop.main_app.models import Item


class IndexView(ListView):
    model = Item
    template_name = 'index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user'] = User.objects.first()
        return context
