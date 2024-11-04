from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='book_category'),
    path('books/<int:genre_id>/', views.books_views, name='book_list'),
    path('book/<int:book_id>/', views.detail_views, name='detail'),
    path('members/', views.register_member, name='register_member'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('borrow/<int:book_copy_id>/', views.borrow_book, name='borrow_book'),
    path('borrow_members/', views.borrowed_member, name='borrow_members'),


]