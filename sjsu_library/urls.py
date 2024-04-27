from django.urls import path
from django.contrib.auth import views as auth_views
from . import views as lib_views

urlpatterns = [
    path('', lib_views.home, name='library-home'),
    path('about/', lib_views.about, name='library-about'),
    path('register/', lib_views.register, name='library-register'),
    path('login/', auth_views.LoginView.as_view(template_name='sjsu_library/login.html'), name='library-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='sjsu_library/logout.html'), name='library-logout'),
    path('books/', lib_views.books, name='library-books'),
    path('account/', lib_views.account, name='library-account'),
    path('users/', lib_views.users, name='library-users'),
    path('borrow/<int:book_id>/', lib_views.borrow_book, name='borrow-book'),
    path('return/<int:book_id>/', lib_views.return_book, name='return-book'),
    path('renew/<int:book_id>/', lib_views.renew_book, name='renew-book'),
    path('delete-book/<int:book_id>/', lib_views.delete_book, name='delete-book'),
    path('delete-user/<int:user_id>/', lib_views.delete_user, name='delete-user'),
    path('switch-view', lib_views.switch_view, name='switch-view')
]