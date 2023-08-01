from django.core.exceptions import ValidationError
from django.db.models import IntegerField, CharField, ForeignKey, SET_NULL, BooleanField, TextField

from system.models import User as UserBasic, EcoGeniusModel


class User(UserBasic):
    is_student = BooleanField(
        verbose_name='Aluno',
        default=True,
    )
    course = CharField(
        verbose_name='Curso',
        help_text='Nome do curso',
        max_length=100,
        blank=True,
    )
    period = IntegerField(
        verbose_name='Período',
        help_text='Período letivo',
        default=1,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_student = False
        super(User, self).save(*args, **kwargs)


class AttributeLifeTable(EcoGeniusModel):
    class Meta:
        verbose_name = 'Atributo'
        verbose_name_plural = 'Atributos'

    def __str__(self):
        return self.name

    name = CharField(
        verbose_name='Atributo',
        help_text='Nome do atributo na tabela de vida',
        max_length=100,
        blank=False,
        unique=True,
        error_messages={
            'unique': 'Um atributo com esse nome já existe.',
            'blank': 'Digite o nome do atributo',
        },
    )


class ColumnLifeTable(EcoGeniusModel):
    class Meta:
        verbose_name = 'Coluna'
        verbose_name_plural = 'Colunas'

    def __str__(self):
        return self.attribute.name

    attribute = ForeignKey(
        AttributeLifeTable,
        on_delete=SET_NULL,
        null=True,
    )


class LifeTable(EcoGeniusModel):
    class Meta:
        verbose_name = 'Tabela de vida'
        verbose_name_plural = 'Tabelas de vida'

    def __str__(self):
        return self.name

    name = CharField(
        verbose_name='Nome',
        help_text='Nome da tabela de vida',
        max_length=100,
        null=False,
        blank=False,
        error_messages={
            'blank': 'Digite o nome da tabela de vida',
        },
    )
    description = CharField(
        verbose_name='Descrição',
        help_text='Descrição da tabela de vida',
        max_length=2560,
        null=False,
        blank=False,
        error_messages={
            'blank': 'Digite a descrição da tabela de vida',
        },
    )

    def delete(self, using=None, keep_parents=False):
        cells = Cell.objects.filter(table=self)
        columns_id = cells.values_list('column', flat=True).distinct()
        columns = ColumnLifeTable.objects.filter(pk__in=columns_id)

        columns.delete()
        cells.delete()
        return super(LifeTable, self).delete(using=using, keep_parents=keep_parents)


class Cell(EcoGeniusModel):
    class Meta:
        verbose_name = 'Célula'
        verbose_name_plural = 'Células'

    def __str__(self):
        return self.value

    table = ForeignKey(
        LifeTable,
        on_delete=SET_NULL,
        null=True,
    )
    column = ForeignKey(
        ColumnLifeTable,
        on_delete=SET_NULL,
        null=True,
    )
    value = TextField(
        verbose_name='Valor',
        help_text='Valor da célula da tabela de vida',
        null=True,
        blank=False,
    )
    line = IntegerField(
        verbose_name='Linha',
        help_text='Linha da célula na tabela de vida'
    )


class Answer(EcoGeniusModel):
    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'

    def __str__(self):
        return self.value

    student = ForeignKey(
        User,
        on_delete=SET_NULL,
        null=True,
    )
    cell = ForeignKey(
        Cell,
        on_delete=SET_NULL,
        null=True,
    )
    value = TextField(
        verbose_name='Valor',
        help_text='Valor da célula da tabela de vida',
        null=True,
        blank=False,
    )
