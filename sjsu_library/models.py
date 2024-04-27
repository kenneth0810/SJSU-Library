from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext as _
from .managers import CustomUserManager

# custom user model
class LibUser(AbstractUser):
    username = models.CharField(_('Username'), max_length=20, unique=False, null=True, default=None)
    first_name = models.CharField(_('First Name'), max_length=30)
    last_name = models.CharField(_('Last Name'), max_length=30)
    email = models.EmailField(_('SJSU Email'), unique=True)
    id_number = models.CharField(_('ID Number'), max_length=9, validators=[MinLengthValidator(9), RegexValidator(regex='^[0-9]{9}$', message=_('ID number must be a 9 digit number.'))], unique=True)
    is_librarian = models.BooleanField(_('I am a librarian'), default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'id_number')

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Book(models.Model):
    title = models.CharField(_('Title'), max_length=100, )
    author = models.CharField(_('Author'), max_length=50)
    year = models.IntegerField(_('Year'), null=True)
    link = models.CharField(_('Link'), max_length=150, null=True)
    count = models.IntegerField(_('Count'), default=5)

    def __str__(self):
        return f'{self.title} by {self.author}'

# relastionship between book and borrower
class BorrowedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(LibUser, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField(default=(timezone.now() + timezone.timedelta(weeks=2)))

    def __str__(self):
        return f"{self.book.title} by {self.book.author}, borrowed by {self.borrower.email}"