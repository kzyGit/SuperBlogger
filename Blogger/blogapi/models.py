from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.template.defaultfilters import slugify


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, firstname, surname, email, password=None):
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, firstname=firstname,
                          surname=surname, email=self.normalize_email(email))
        user.set_password(password) if password else user.set_password(email)
        user.save()

        return user

    def create_superuser(
            self, username, firstname, surname, email, password=None):
        user = self.create_user(
            username, firstname, surname, email, password)
        user.is_superuser = True
        user.is_admin = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=255)
    firstname = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['firstname', 'surname', 'email', 'password']

    def __str__(self):
        return self.email


class Articles(models.Model):
    title = models.CharField(unique=True, max_length=255)
    body = models.TextField()
    description = models.TextField()
    images = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True)

    user = models.ForeignKey(User, related_name='user',
                             on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Articles, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
