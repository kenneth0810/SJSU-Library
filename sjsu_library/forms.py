from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import LibUser, Book

# predetermined librarian account for simplicity!
LIB_EMAIL = 'librarian@sjsu.edu'
LIB_ID = '123456789'

class CustomUserRegisterForm(UserCreationForm):

    class Meta:
        model = LibUser
        fields = ('email', 'first_name', 'last_name', 'id_number', 'is_librarian', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        domain = email.split('@')[1]
        if domain != 'sjsu.edu':
            raise ValidationError("Only SJSU domains allowed: email@sjsu.edu")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data.get('email')
        id_number = self.cleaned_data.get('id_number')
        is_librarian = self.cleaned_data.get('is_librarian')

        # in case user enters librarian credentials but forgets to indicate that they are the librarian
        if email == LIB_EMAIL and id_number == LIB_ID:
            is_librarian = True

        user.is_librarian = is_librarian

        if commit:
            user.save()
        return user
        
class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = LibUser
        fields = ('email', 'first_name', 'last_name', 'id_number')

# TODO: create a form to add new books
class AddBookForm(ModelForm):

    class Meta:
        model = Book
        fields = ('title', 'author', 'year', 'link', 'count')