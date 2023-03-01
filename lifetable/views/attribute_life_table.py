from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from lifetable.forms import AttributeLifeTableForm
from lifetable.models import AttributeLifeTable


class AttributeLifeTableCreateView(CreateView):
    template_name = 'lifetable/attribute_life_table/create.html'
    model = AttributeLifeTable
    form_class = AttributeLifeTableForm
    success_url = reverse_lazy('list_attributes')


class AttributeLifeTableUpdateView(UpdateView):
    template_name = 'lifetable/attribute_life_table/update.html'
    model = AttributeLifeTable
    form_class = AttributeLifeTableForm
    success_url = reverse_lazy('list_attributes')


class AttributeLifeTableListView(ListView):
    model = AttributeLifeTable
    template_name = 'lifetable/attribute_life_table/index.html'
    paginate_by = 20

    def get_queryset(self):
        return super(AttributeLifeTableListView, self).get_queryset().order_by('pk')


class AttributeLifeTableDeleteView(DeleteView):
    model = AttributeLifeTable
    template_name = 'lifetable/attribute_life_table/delete.html'
    success_url = reverse_lazy('list_attributes')
