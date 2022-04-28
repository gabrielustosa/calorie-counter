from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from datetime import date

from calorie.apps.meal import models as meal


def get_age(birthdate):
    today = date.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)

        weight = extra_fields['weight']
        height = extra_fields['height']
        age = get_age(extra_fields['birthday'])

        if extra_fields['sex'] == 'M':
            user.max_calories = (13.75 * weight) + (5 * height) - (6.76 * age) + 66.5
        elif extra_fields['sex'] == 'F':
            user.max_calories = (9.56 * weight) + (1.85 * height) - (4.68 * age) + 665
        user.save(using=self.db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser precisa precisa estar como True')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_staff precisa precisa estar como True')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField('E-mail', unique=True)
    is_staff = models.BooleanField('Equipe', default=False)
    name = models.CharField('Nome', max_length=150)
    height = models.PositiveIntegerField('Altura em cm')
    weight = models.IntegerField('Peso')
    birthday = models.DateField()
    max_calories = models.PositiveIntegerField('Meta de calorias', default=0)
    current_calories = models.PositiveIntegerField('Calorias atuais', default=0)
    sex = models.CharField(max_length=2, choices=[
        ('M', 'MASCULINO'),
        ('F', 'FEMININO'),
    ])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'height', 'weight', 'birthday', 'sex']

    def __str__(self):
        return self.email

    objects = UserManager()


