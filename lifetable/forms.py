import pandas as pandas
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm as AuthenticationFormBasic, UsernameField
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from lifetable.models import User, AttributeLifeTable, LifeTable, ColumnLifeTable, Cell, Answer


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'course', 'period', 'email']

    def __init__(self, *args, **kwargs):
        is_student = kwargs.pop('is_student', False)
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.instance.is_student = is_student

        if not is_student:
            self.fields.pop('course')
            self.fields.pop('period')

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Div(
                Field('first_name', wrapper_class='col-md-6'),
                Field('last_name', wrapper_class='col-md-6'),
                Field('email', wrapper_class='col-md-6') if is_student else Field('email', wrapper_class='col-md-12'),
                Field('course', wrapper_class='col-md-3'),
                Field('period', wrapper_class='col-md-3'),
                Field('password1', wrapper_class='col-md-6'),
                Field('password2', wrapper_class='col-md-6'),
                css_class='form-row',
            ),
        )

    def clean(self):
        # Checks if the user is a student and if he filled in the period and course
        if self.instance.is_student:
            if not self.cleaned_data.get('course'):
                raise ValidationError("Informe o curso")
            if not self.cleaned_data.get('period'):
                raise ValidationError("Informe o periodo letivo")
        return super(UserCreateForm, self).clean()


class AuthenticationForm(AuthenticationFormBasic):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True}), label='Email')


class AttributeLifeTableForm(ModelForm):
    class Meta:
        model = AttributeLifeTable
        fields = '__all__'


class LifeTableForm(ModelForm):
    file = forms.FileField(
        label='Planilha',
        help_text='Carregue a planilha(arquivo do tipo ".csv") com os dados da tabela de vida.',
        required=False,
        max_length=100,
    )

    class Meta:
        model = LifeTable
        fields = [
            'name', 'description', 'file',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'cols': 256, 'rows': 10}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.df_columns_names = None
        self.df_life_table = None

    def clean(self):
        # get spreadsheet
        self.file = self.cleaned_data.get('file')
        # Return error if it is a new table without a worksheet
        if not self.file and not self.instance.pk:
            raise ValidationError('Envie a planilha da tabela de vida que deseja cadastrar')
        # Complete in case of data update without worksheet
        elif not self.file:
            return super(LifeTableForm, self).clean()

        # Read data from spreadsheet
        try:
            self.df_life_table = pandas.read_csv(self.file)
            self.df_columns_names = self.df_life_table.columns.values.tolist()
        except Exception:
            raise ValidationError(
                'Não foi possivel ler os dados contidos na planilha. '
                'Verifique se o arquivo é do tipo ".csv" e se os dados foram preenchidos corretamente'
            )

        # Checks if all dataframe attributes exist in the database
        for df_column_name in self.df_columns_names:
            try:
                attribute = AttributeLifeTable.objects.get(name=df_column_name)
                if not attribute:
                    raise Exception
            except Exception:
                raise ValidationError('A coluna ' + df_column_name + ' não foi encontrada no banco de dados, '
                                                                     'verifique se o nome está correto')
        return super(LifeTableForm, self).clean()

    def save(self, commit=True):
        # Return error if it is a new table without a worksheet
        if not self.file and not self.instance.pk:
            raise ValidationError('Envie a planilha da tabela de vida que deseja cadastrar')
        # Update case data without worksheet
        elif not self.file:
            return super(LifeTableForm, self).save()
        # Delete data in case of table update
        elif self.file and self.instance.pk:
            cells = Cell.objects.filter(table=self.instance.pk)
            columns_id = cells.values_list('column', flat=True).distinct()
            columns = ColumnLifeTable.objects.filter(pk__in=columns_id)

            columns.delete()
            cells.delete()

        # Looks for the attributes referring to the dataframe columns and
        # creates the instances of the life table columns
        columns = []
        for df_column_name in self.df_columns_names:
            try:
                attribute = AttributeLifeTable.objects.get(name=df_column_name)
                if attribute:
                    column = ColumnLifeTable.objects.create(attribute=attribute)
                    columns.append(column)
                else:
                    raise Exception
            except Exception:
                raise ValidationError('A coluna ' + df_column_name + ' não foi encontrada no banco de dados, '
                                                                     'verifique se o nome está correto')

        # Creates the life table and the cells that make it up
        life_table = super(LifeTableForm, self).save(commit=commit)
        for column in columns:
            values = self.df_life_table[column.attribute.name]
            for line, value in enumerate(values):
                Cell.objects.create(
                    table=life_table,
                    column=column,
                    value=value,
                    line=line,
                )

        return super(LifeTableForm, self).save(commit=commit)


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = '__all__'

    def __init__(self, cell_pk, student_pk, value=None, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)

        cell = Cell.objects.get(pk=cell_pk)
        student = User.objects.get(pk=student_pk)

        self.fields['cell'].initial = cell
        self.fields['student'].initial = student

        if value:
            self.fields['value'].initial = value
