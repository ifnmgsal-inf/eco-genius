from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from lifetable.forms import UserCreateForm
from lifetable.models import User


class TeacherCreateView(CreateView):
    template_name = 'lifetable/teacher/create.html'
    model = User
    form_class = UserCreateForm
    success_url = reverse_lazy('list_teachers')


class TeacherListView(ListView):
    model = User
    template_name = 'lifetable/teacher/index.html'
    paginate_by = 20

    def get_queryset(self):
        return super(TeacherListView, self).get_queryset().filter(
            is_student=False,
        ).exclude(
            is_superuser=True
        ).order_by('pk')
