from django.urls import path
from .views import *
urlpatterns = [
    path('home',home ,name="home"),
    path('home1',home1 ,name="home1"),
    path('register',register_attempt ,name="register_attempt"),
    path('',login_attempt ,name="login_attempt"),
    path('token',token_send ,name="token_send"),
    path('success',success ,name="success"),
    path('verify/<auth_token>',verify ,name="verify"),
    path('error',error_page ,name="error"),
    path('forget',forget_pass,name="forget_pass"),
    path('new_password',new_password,name="new_password"),
    path('forget_auth_code',forget_auth_code,name="forget_auth_code"),
    # book entries
    path('add_book/',add_book,name="add_book"),
    path('edit_book/',edit_book,name="edit_book"),
    path('edit_book/edit_book1/<isbn>/',edit_book1,name="edit_book1"),
    path('book_view/<isbn>/',book_view,name="book_view"),
    
    path('view_books/',view_books,name="view_books"),
    path('subscribe_view_book/',subscribe_view_book,name="subscribe_view_book"),
    path('view_subscribers/',view_subscribers,name="view_subscribers"),
    path('subscriber_issued_books/',subscriber_issued_books,name="subscriber_issued_books"),
    


    path('UCreateChat/',UCreateChat.as_view(),name="UCreateChat"),
    path('UListChat/',UListChat.as_view(),name="UListChat"),

    path('SCreateChat/',SCreateChat.as_view(),name="SCreateChat"),
    path('SListChat/',SListChat.as_view(),name="SListChat"),
    
    
    # issue section
    path('issue_book/',issue_book,name="issuebook"),
    path('subscriber_issued_books/simple_checkout/',simple_checkout,name="simple_checkout"),
    path('return_book/',return_book,name="return_book"),
    path('confirm_return_book/<isbn>/',confirm_return_book,name="confirm_return_book"),
    path('delete_books/<int:myid>/',delete_books,name="delete_books"),
    path('delete_subscribers/<int:myid>/',delete_subscribers,name="delete_subscribers"),
    path('delete_issued_book/<isbn>/',delete_issued_book,name="delete_issued_book"),
    path('view_issued_book/',view_issued_book,name="view_issued_book"),
    path('logout/',logout,name="logout"),
]