from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from lifetable.forms import LifeTableForm
from lifetable.models import LifeTable


class LifeTableCreateView(CreateView):
    template_name = 'lifetable/life_table/create.html'
    model = LifeTable
    form_class = LifeTableForm
    success_url = reverse_lazy('list_life_table')


class LifeTableUpdateView(UpdateView):
    template_name = 'lifetable/life_table/update.html'
    model = LifeTable
    form_class = LifeTableForm
    success_url = reverse_lazy('list_life_table')


class LifeTableListView(ListView):
    model = LifeTable
    template_name = 'lifetable/life_table/index.html'
    paginate_by = 20

    def get_queryset(self):
        return super(LifeTableListView, self).get_queryset().order_by('pk')


class LifeTableDeleteView(DeleteView):
    model = LifeTable
    template_name = 'lifetable/life_table/delete.html'
    success_url = reverse_lazy('list_life_table')
