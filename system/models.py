from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import Model, DateTimeField
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    email = models.EmailField(
        _("Endereço de email"),
        max_length=150,
        unique=True,
        help_text=_(
            "Utilize menos de 150 caracteres..",
        ),
        blank=False,
        validators=[username_validator],
        error_messages={
            "unique": _("Um usuário com esse nome já existe."),
            "blank": _("O campo de email não pode ficar vazio."),
        },
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _("usuário")
        verbose_name_plural = _("usuários")

    def save(self, *args, **kwargs):
        self.username = self.email
        super(User, self).save(*args, **kwargs)


class EcoGeniusModel(Model):
    class Meta:
        abstract = True

    created_at = DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name='Data de criação',
    )
    updated_at = DateTimeField(
        auto_now=True, null=True, blank=True, verbose_name='Data de atualização',
    )
