from django.contrib.auth.decorators import login_required
from django.urls import path

from lifetable.views.answer import AnswerListView, AnswerCreateView, AnswerView, AnswerStudentListView, \
    AnswerStudentView, AnswerStudentDeleteView
from lifetable.views.attribute_life_table import *
from lifetable.views.life_table import LifeTableListView, LifeTableCreateView, LifeTableUpdateView, LifeTableDeleteView
from lifetable.views.teacher import TeacherListView, TeacherCreateView
from lifetable.views.views import Home, CreateUserView, PasswordChangeView, PasswordResetCompleteView, LoginView

urlpatterns = [
    path('home/', login_required(Home.as_view()), name='home'),

    # Accounts
    path("accounts/login/", LoginView.as_view(), name="login"),
    path('accounts/register/', CreateUserView.as_view(), name='create_user'),
    path('accounts/password_change/done/', PasswordChangeView.as_view(), name='password_change_done'),
    path("accounts/reset/done/", PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    # Attribute life table
    path('atributos/', AttributeLifeTableListView.as_view(), name='list_attributes'),
    path('atributos/novo/', AttributeLifeTableCreateView.as_view(), name='create_attribute'),
    path('atributos/atualizar/<int:pk>/', AttributeLifeTableUpdateView.as_view(), name='update_attribute'),
    path('atributos/apagar/<int:pk>/', AttributeLifeTableDeleteView.as_view(), name='delete_attribute'),

    # Life table
    path('tabelas_de_vida/', LifeTableListView.as_view(), name='list_life_table'),
    path('tabelas_de_vida/novo/', LifeTableCreateView.as_view(), name='create_life_table'),
    path('tabelas_de_vida/atualizar/<int:pk>/', LifeTableUpdateView.as_view(), name='update_life_table'),
    path('tabelas_de_vida/apagar/<int:pk>/', LifeTableDeleteView.as_view(), name='delete_life_table'),

    # Answers
    path('respostas/', AnswerListView.as_view(), name='list_answer'),
    path('respostas/responder/<int:table_pk>', AnswerCreateView.as_view(), name='create_answer'),
    path('respostas/visualizar/<int:table_pk>/', AnswerView.as_view(), name='view_answer'),
    path('respostas/<int:table_pk>/', AnswerStudentListView.as_view(), name='list_answer_student'),
    path('respostas/<int:table_pk>/visualizar/<int:student_pk>/', AnswerStudentView.as_view(),
         name='view_answer_student'),
    path('respostas/<int:table_pk>/apagar/<int:student_pk>/', AnswerStudentDeleteView.as_view(),
         name='delete_answer_student'),

    # Teachers
    path('professores/', TeacherListView.as_view(), name='list_teachers'),
    path('professores/novo/', TeacherCreateView.as_view(), name='create_teacher'),
]
