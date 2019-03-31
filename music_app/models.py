from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from audiofield.models import AudioFile
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
	"""
	A custom user manager to deal with emails as unique identifiers for auth
	instead of usernames. The default that's used is "UserManager"
	"""
	def create_user(self, phone_number, profile_picture=None, password=None):
		"""
		Creates and saves a User with the given email, date of
		birth and password.
		"""
		if not phone_number:
		    raise ValueError('Users must have an phone number')

		user = self.model(
		    phone_number=self.phone_number,
		    profile_picture=profile_picture,
		    username =self.phone_number,
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, phone_number, password):
		"""
		Creates and saves a superuser with the given email, date of
		birth and password.
		"""
		user = self.create_user(
		    phone_number,
		    password=password,
		)
		user.is_admin = True
		user.save(using=self._db)
		return user


class User(AbstractUser):
    phone_number = PhoneNumberField(unique=True)
    profile_picture = models.ImageField(
        upload_to='user_data/profile_picture', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    

    def __str__(self):
        return f'{self.phone_number}'

    def has_perm(self, perm, obj=None):
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def get_full_name(self):
        return self.phone_number

    def get_short_name(self):
        return self.phone_number


