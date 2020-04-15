from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group, Permission

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, matricula, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not matricula:
            raise ValueError('The given matricula must be set')
        email = self.normalize_email(email)
        user = self.model(matricula=matricula, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, matricula, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(matricula, email, password, **extra_fields)

    def create_superuser(self, matricula, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_avaliador', True)
        extra_fields.setdefault('is_coordenador', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_avaliador') is not True:
            raise ValueError('Superuser must have is_avaliador=True.')
        if extra_fields.get('is_coordenador') is not True:
            raise ValueError('Superuser must have is_coordenador=True.')

        return self._create_user(matricula, email, password, **extra_fields)