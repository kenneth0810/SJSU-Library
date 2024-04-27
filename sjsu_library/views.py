from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from .forms import CustomUserChangeForm, CustomUserRegisterForm, AddBookForm
from django.contrib import messages
from .models import LibUser, Book, BorrowedBook
from django.utils import timezone

# predetermined librarian account for simplicity!
LIB_EMAIL = 'librarian@sjsu.edu'
LIB_ID = '123456789'

# custom wrapper to redirect to login page if an unauthorized user accesses a restricted page
def login_required_decorator(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'You need to log in to perform that action.')
            return redirect('library-login')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper

def home(request):
    if request.method == 'GET' and request.user.is_authenticated:
        return redirect('library-books')
    contents = {
        'title': 'Home',
    }
    return render(request, 'sjsu_library/home.html', contents)

def about(request):
    contents = {
        'title': 'About',
    }
    return render(request, 'sjsu_library/about.html', contents)

def register(request):
    if request.method == 'POST':
        form = CustomUserRegisterForm(request.POST)
        if form.is_valid():
            form.save(commit=False)

            is_lib = form.cleaned_data.get('is_librarian')
            email = form.cleaned_data.get('email')
            id_number = form.cleaned_data.get('id_number')
             
            if email == LIB_EMAIL and id_number == LIB_ID:
                form.save()
                messages.success(request, 'Your librarian account was registered successfully.')
                return redirect('library-login')
            elif email == LIB_EMAIL and id_number != LIB_ID or email != LIB_EMAIL and id_number == LIB_ID:
                messages.warning(request, 'You are using the librarian\'s credentials, but either the email field or ID number field is incorrect. Please try again.')
            else:
                if not is_lib:
                    form.save()
                    first_name = form.cleaned_data.get('first_name')
                    last_name = form.cleaned_data.get('last_name')
                    messages.success(request, f'Hi {first_name} {last_name}! Your student account was registered successfully.')
                    return redirect('library-login')
                else:
                    messages.warning(request, 'Registration failed. Your credentials are not valid for a librarian account.')
    else:
        form = CustomUserRegisterForm()
    
    contents = {
        'title': 'Register',
        'form': form
    }
    return render(request, 'sjsu_library/register.html', contents)

@login_required_decorator
def books(request):
    all_books = Book.objects.all()
    borrowed_books_id = None
    if request.user.is_authenticated:
        borrowed_books_id = [book.book.id for book in BorrowedBook.objects.filter(borrower=request.user)]
   
    contents = {
        'title': 'Books',
        'books': all_books,
        'borrowed_books_id': borrowed_books_id
    }

    return render(request, 'sjsu_library/books.html', contents)

@login_required_decorator
def account(request):
    if not request.user.is_librarian:
        borrowed_books = list(BorrowedBook.objects.filter(borrower=request.user))
        borrowed_books.sort(key=lambda x: x.return_date)
        contents = {
            'title': 'Account',
            'borrowed_books': borrowed_books
        }
        return render(request, 'sjsu_library/account.html', contents)
    else:
        return HttpResponseForbidden('You do not have access to view this page.')

@login_required_decorator
def users(request):
    if request.user.is_librarian:
        all_users = LibUser.objects.filter(is_librarian=False, is_superuser=False)
        contents = {
            'title': 'Users',
            'users': all_users
        }
        return render(request, 'sjsu_library/users.html', contents)
    else:
        return HttpResponseForbidden('You do not have access to view this page.')

@login_required_decorator
def borrow_book(request, book_id):
    if request.method == 'POST':
        book = Book.objects.get(pk=book_id)
        borrowed = BorrowedBook.objects.create(borrower=request.user, book=book)
        book.count -= 1
        book.save()
        messages.success(request, f'Now borrowing {book.title} by {book.author}. Please see your account to view return dates.')
        return redirect('library-books')
    else:
        return HttpResponseNotAllowed(['POST'])
    
@login_required_decorator
def return_book(request, book_id):
    if request.method == 'POST':
        book = BorrowedBook.objects.get(pk=book_id, borrower=request.user)
        book.book.count += 1
        book.book.save()
        messages.success(request, f'You returned {book.book.title} by {book.book.author}.')
        book.delete()
        return redirect('library-account')
    else:
        return HttpResponseNotAllowed(['POST'])

@login_required_decorator
def renew_book(request, book_id):
    if request.method == 'POST':
        book = BorrowedBook.objects.get(pk=book_id, borrower=request.user)
        book.return_date += timezone.timedelta(weeks=1)
        book.save()
        messages.success(request, 'Book renewed.')
        return redirect('library-account')
    else:
        return HttpResponseNotAllowed(['POST'])
    
@login_required_decorator
def delete_book(request, book_id):
    if request.method == 'POST':
        book = Book.objects.get(pk=book_id)
        messages.warning(request, f'Deleted {book.title} by {book.author}.')
        book.delete()
        return redirect('library-books')
    else:
        return HttpResponseNotAllowed(['POST'])
    
@login_required_decorator
def delete_user(request, user_id):
    if request.method == 'POST':
        user = LibUser.objects.get(pk=user_id)
        messages.warning(request, f'Deleted user: {user.first_name} {user.last_name}, {user.email}, {user.id_number}.')
        user.delete()
        return redirect('library-users')
    else:
        return HttpResponseNotAllowed(['POST'])

# TODO: create a view function to render the form to add new books  
@login_required_decorator
def add_book(request):
    pass

@login_required_decorator
def switch_view(request):
    if request.method == 'POST' and request.user.is_superuser:
        request.user.is_librarian = not request.user.is_librarian
        request.user.save()
        return redirect('library-books')
    else:
        return HttpResponseNotAllowed(['POST'])