from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Role(models.Model):
    """This entails the part played by a user in the application

    Args:
        models ([type]): [description]

    Raises:
        ValueError: [description]

    Returns:
        [type]: [description]
    """
    name = models.CharField(max_length=20,unique=True)

    def __str__(self):
        return self.name

class MyAccountManager(BaseUserManager):
    """defines the methods to manage the custom user to be created

    Args:
        BaseUserManager ([type]): [description]

    Returns:
        [type]: [description]
    """

    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have and email address")

        user = self.model(
            email=self.normalize_email(email),
            password = password
        )
        user.role = Role.objects.get(name = "customer")
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,password):
        user = self.create_user(
            email=self.normalize_email(email),
            password = password
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.role = Role.objects.get(name="staff")

        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    """This is the user instance

    Args:
        models ([type]): [description]

    Returns:
        [type]: [description]
    """
    email = models.EmailField(verbose_name='email',unique=True)
    role = models.ForeignKey(Role,on_delete=models.PROTECT)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    member_since = models.DateTimeField(auto_now_add=True,editable=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.first_name + " " + self.last_name

    def deactivate_account(self):
        """
        This makes a user's account inactive"""
        self.is_active = False
        self.save()

    def reinstate(self):
        """This allows for a users whose account was inactive to be reinstated
        """
        self.is_active = True
        self.save()

MALE = "Male"
FEMALE = "Female"
RATHER_NOT_SAY = "Rather_Not_Say"

gender_choices = (
    (MALE,"Male"),
    (FEMALE,"Female"),
    (RATHER_NOT_SAY,"Rather_Not_Say")
)
class Profile(models.Model):
    """This is any changable info on the user

    Args:
        models ([type]): [description]
    """
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    phone_number = PhoneNumberField(region="KE")
    bio = models.TextField()
    location = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to="profiles/")
    gender = models.CharField(max_length=50,choices=gender_choices)
    receive_notifications_via_email = models.BooleanField(default=True)