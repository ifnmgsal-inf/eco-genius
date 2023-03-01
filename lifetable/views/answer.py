import numpy as np
from django.db.models import ExpressionWrapper, F, Count, Q, DecimalField, Max
from django.db.models.functions import Round
from django.http import Http404, HttpResponseRedirect, QueryDict
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView

from lifetable.forms import AnswerForm
from lifetable.models import Answer, LifeTable, ColumnLifeTable, Cell, User


class AnswerCreateView(CreateView):
    template_name = 'lifetable/answer/create.html'
    model = Answer
    form_class = AnswerForm
    success_url = reverse_lazy('list_answer')
    object = None
    cells_pk = []
    quantity_lines = 0
    columns_life_table = None
    cells = None
    table = None

    def get_success_url(self):
        return self.success_url

    def get_form_kwargs(self, cell_pk=None, student_pk=None):
        kwargs = {
            "initial": self.get_initial(),
            "prefix": self.get_prefix(),
            'cell_pk': cell_pk,
            'student_pk': student_pk,
        }
        query_dict = kwargs.get('data')
        if not query_dict:
            query_dict = QueryDict('', mutable=True)
            data = {
                'cell': cell_pk,
                'student': student_pk,
            }
            query_dict.update(data)
            kwargs.update({"data": query_dict})
        if self.request.method in ("POST", "PUT"):
            data = {
                'csrfmiddlewaretoken': self.request.POST.get('csrfmiddlewaretoken'),
                'value': self.request.POST.get(str(cell_pk)),
                'cell': cell_pk,
                'student': student_pk,
            }
            query_dict = QueryDict('', mutable=True)
            query_dict.update(data)
            kwargs.update(
                {
                    "data": query_dict,
                    "files": self.request.FILES,
                }
            )
        if hasattr(self, "object") and self.object and self.object.cell.pk == cell_pk:
            kwargs.update({"instance": self.object})
        return kwargs

    def get_form(self, form_class=None):
        """
        Returns an array of Answers forms with the cells chosen to answer
        """

        forms = []
        user_pk = self.request.user.pk
        for cell_pk in self.cells_pk:
            form = AnswerForm(**self.get_form_kwargs(cell_pk=cell_pk, student_pk=user_pk))
            forms.append(form)

        return forms

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""

        # Get the table if it exists
        table_pk = kwargs.get('table_pk')
        try:
            self.table = LifeTable.objects.get(pk=table_pk)
        except Exception:
            raise Http404

        # Get all cells from the life table
        self.cells = Cell.objects.filter(table=self.table.pk).order_by('pk').all()

        # Get all columns from the life table
        columns_id = self.cells.values_list('column', flat=True).distinct()
        self.columns_life_table = ColumnLifeTable.objects.filter(pk__in=columns_id).order_by('pk')

        # Remove first column (referring to the time range)
        columns_answer = self.columns_life_table.exclude(pk=self.columns_life_table.first().pk).all()
        # Get the number of rows from the life table
        self.quantity_lines = columns_answer.first().cell_set.count()
        # Number of cells to answer (30%)
        number_responses_per_column = int(self.quantity_lines / 3) if int(self.quantity_lines / 3) > 1 else 1

        context = super(AnswerCreateView, self).get_context_data(**kwargs)
        if "forms" not in context:
            # Choose cells to answer in each column
            self.cells_pk.clear()
            for column in columns_answer:
                lines = np.random.randint(0, self.quantity_lines, (1, number_responses_per_column))[0]
                self.cells_pk += self.cells.filter(column=column.pk, line__in=lines).values_list('pk', flat=True)

            context["forms"] = self.get_form()
            context.pop('form')
        else:
            forms = context.get('forms')
            self.cells_pk.clear()

            for form in forms:
                self.cells_pk.append(form.data.get('cell'))

        # Puts in context the name of all columns of the life table
        context['columns'] = self.columns_life_table.values_list('attribute__name', flat=True).order_by('pk')

        lines_life_table = []
        for line in range(self.quantity_lines):
            # Gets all cells from row "line" of the life table
            cells_line = self.cells.filter(line=line).order_by('column__pk')
            cells_line_dict = []
            for cell in cells_line:
                if cell.pk in self.cells_pk:
                    form_cell = None
                    for form in context.get('forms'):
                        if form.data.get('cell') == cell.pk:
                            form_cell = form
                            break
                    cell_ln_dict = {'pk': cell.pk, 'form': form_cell}
                else:
                    cell_ln_dict = {'pk': cell.pk, 'value': cell.value}
                cells_line_dict.append(cell_ln_dict)
            # Put the line in the lines array
            lines_life_table.append(cells_line_dict)

        # Puts the row array in context
        context['lines'] = lines_life_table
        return context

    def get(self, request, *args, **kwargs):
        self.object = None
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context=context)

    def post(self, request, *args, **kwargs):
        self.object = None
        forms = self.get_form()
        for index, form in enumerate(forms):
            if not form.is_valid():
                cell = Cell.objects.get(pk=form.data.get('cell'))
                table = LifeTable.objects.get(pk=cell.table.pk)
                table_pk = table.pk
                return self.render_to_response(self.get_context_data(table_pk=table_pk, forms=forms))

        for form in forms:
            form.save()

        return HttpResponseRedirect(self.get_success_url())


class AnswerListView(ListView):
    model = LifeTable
    template_name = 'lifetable/answer/index.html'
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user

        if user.is_student:
            answers = Answer.objects.filter(student=user)
        else:
            answers = Answer.objects.all()

        cells_pk = answers.values_list('cell', flat=True)

        tables_pk = Cell.objects.filter(pk__in=cells_pk).values_list('table', flat=True).distinct()

        corrects = ExpressionWrapper(
            Round(Count('pk', filter=Q(cell__answer__value=F('cell__value'))) * 100. / Count('cell__answer__value')),
            output_field=DecimalField()
        )

        tables_answers = super(AnswerListView, self).get_queryset().order_by('pk').filter(
            pk__in=tables_pk, cell__answer__in=answers,
        ).annotate(
            corrects=corrects,
        )

        if not user.is_student:
            tables_answers = tables_answers.annotate(
                quantity=Count('cell__answer__student', distinct=True),
            )
        else:
            tables_answers = tables_answers.annotate(
                date_response=Max('cell__answer__updated_at'),
            )

        return tables_answers

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AnswerListView, self).get_context_data(object_list=object_list, **kwargs)
        user = self.request.user
        if user.is_student:
            context['tables'] = LifeTable.objects.exclude(pk__in=self.get_queryset())
        return context


class AnswerView(View):
    template_name = 'lifetable/answer/view.html'

    def get(self, request, *args, **kwargs):
        # Get the table if it exists
        table_pk = kwargs.pop('table_pk', None)
        try:
            table = LifeTable.objects.get(pk=table_pk)
        except Exception:
            raise Http404

        # Get all cells from the life table
        cells = Cell.objects.filter(table=table.pk).order_by('pk').all()

        user = request.user
        answers = Answer.objects.filter(student=user, cell__in=cells)
        if not answers.exists():
            raise Http404

        answer_cells_pk = answers.values_list('cell', flat=True)

        # Get all columns from the life table
        columns_id = cells.values_list('column', flat=True).distinct()
        columns_life_table = ColumnLifeTable.objects.filter(pk__in=columns_id).order_by('pk')

        # Puts in context the name of all columns of the life table
        columns_name = columns_life_table.values_list('attribute__name', flat=True).order_by('pk')
        # Get the number of rows from the life table
        quantity_lines = columns_life_table.first().cell_set.count()

        lines_life_table = []
        for line in range(quantity_lines):
            # Gets all cells from row "line" of the life table
            cells_line = cells.filter(line=line).order_by('column__pk').all()
            cells_line_dict = []
            for cell in cells_line:
                if cell.pk in answer_cells_pk:
                    anser = answers.get(cell=cell.pk)
                    cell_ln_dict = {'pk': cell.pk, 'value': cell.value, 'answer': anser.value}
                else:
                    cell_ln_dict = {'pk': cell.pk, 'value': cell.value}
                cells_line_dict.append(cell_ln_dict)
            # Put the line in the lines array
            lines_life_table.append(cells_line_dict)

        context = {
            'table_pk': table_pk,
            'columns': columns_name,
            'lines': lines_life_table,
        }

        return render(request=request, template_name=self.template_name, context=context)


class AnswerStudentListView(ListView):
    model = User
    template_name = 'lifetable/answer/answers_students.html'
    paginate_by = 20
    table_pk = None

    def get_queryset(self):
        table_pk = self.kwargs.get('table_pk')
        cells_pk = Cell.objects.filter(table=table_pk).values_list('pk', flat=True)
        students_pk = Answer.objects.filter(cell__in=cells_pk).values_list('student', flat=True)

        corrects = ExpressionWrapper(
            Count('pk', filter=Q(answer__value=F('answer__cell__value'))) * 100 / Count('answer'),
            output_field=DecimalField()
        )

        return super(AnswerStudentListView, self).get_queryset().order_by('pk').filter(
            pk__in=students_pk,
        ).annotate(
            corrects=corrects,
            date_response=Max('answer__updated_at'),
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AnswerStudentListView, self).get_context_data(object_list=object_list, **kwargs)
        context['table_pk'] = self.table_pk
        return context

    def get(self, request, *args, **kwargs):
        self.table_pk = kwargs.get('table_pk')
        return super(AnswerStudentListView, self).get(request, *args, **kwargs)


class AnswerStudentView(View):
    template_name = 'lifetable/answer/view.html'

    def get(self, request, *args, **kwargs):
        # Get the table if it exists
        table_pk = kwargs.pop('table_pk', None)
        student_pk = kwargs.pop('student_pk', None)
        try:
            table = LifeTable.objects.get(pk=table_pk)
            user = User.objects.get(pk=student_pk)
        except Exception:
            raise Http404

        # Get all cells from the life table
        cells = Cell.objects.filter(table=table.pk).order_by('pk').all()

        answers = Answer.objects.filter(student=user, cell__in=cells)
        if not answers.exists():
            raise Http404

        answer_cells_pk = answers.values_list('cell', flat=True)

        # Get all columns from the life table
        columns_id = cells.values_list('column', flat=True).distinct()
        columns_life_table = ColumnLifeTable.objects.filter(pk__in=columns_id).order_by('pk')

        # Puts in context the name of all columns of the life table
        columns_name = columns_life_table.values_list('attribute__name', flat=True).order_by('pk')
        # Get the number of rows from the life table
        quantity_lines = columns_life_table.first().cell_set.count()

        lines_life_table = []
        for line in range(quantity_lines):
            # Gets all cells from row "line" of the life table
            cells_line = cells.filter(line=line).order_by('column__pk').all()
            cells_line_dict = []
            for cell in cells_line:
                if cell.pk in answer_cells_pk:
                    anser = answers.get(cell=cell.pk)
                    cell_ln_dict = {'pk': cell.pk, 'value': cell.value, 'answer': anser.value}
                else:
                    cell_ln_dict = {'pk': cell.pk, 'value': cell.value}
                cells_line_dict.append(cell_ln_dict)
            # Put the line in the lines array
            lines_life_table.append(cells_line_dict)

        context = {
            'table_pk': table_pk,
            'student_pk': student_pk,
            'columns': columns_name,
            'lines': lines_life_table,
        }

        return render(request=request, template_name=self.template_name, context=context)


class AnswerStudentDeleteView(DeleteView):
    model = LifeTable
    template_name = 'lifetable/answer/delete.html'
    success_url = reverse_lazy('list_answer')
    object = None

    def get_object(self, queryset=None):
        table_pk = self.kwargs.get('table_pk', None)
        student_pk = self.kwargs.get('student_pk', None)

        answers = Answer.objects.filter(cell__table=table_pk, student=student_pk)
        if not answers.exists():
            raise Http404

        self.object = answers
        return self.object

    def get_context_data(self, **kwargs):
        context = super(AnswerStudentDeleteView, self).get_context_data(**kwargs)
        context['student_pk'] = self.kwargs.get('student_pk', 0)
        context['table_pk'] = self.kwargs.get('table_pk')

        student = get_object_or_404(User, pk=context.get('student_pk'))
        context['student_name'] = student.first_name
        return context
