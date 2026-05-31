from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<int:id>/', views.book_detail, name='book_detail'),

    path('issue/<int:id>/', views.issue_book, name='issue'),
    path('mybooks/', views.my_books, name='my_books'),
    path('return/<int:id>/', views.return_book, name='return'),

    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
]