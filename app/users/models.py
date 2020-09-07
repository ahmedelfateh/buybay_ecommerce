from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField


class UserManager(BaseUserManager):
    # pylint: disable=arguments-differ
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return super().create_user("", email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return super().create_superuser("", email, password, **extra_fields)


class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"

    username = None  # type: ignore
    email = models.EmailField("Email", blank=True, unique=True)
    gender = models.CharField("Gender", max_length=2, choices=Gender.choices, null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        ordering = ["first_name", "email"]
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "users"

    def __str__(self):
        return f"{self.name} ({self.email})"

    def get_absolute_url(self):
        return reverse("users:user-detail", kwargs={"pk": self.pk})

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    @property
    def last_name_abbr(self):
        """Get an Abbreviated Last Name"""
        return self.last_name[0].upper() + "."

    @property
    def name(self):
        return self.get_full_name()

    @property
    def is_email_verified(self):
        return self.emailaddress_set.filter(email=self.email, verified=True).exists()


class BillingAddress(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.PROTECT)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.country}, {self.street_address}, {self.apartment_address}, {self.zip}"
