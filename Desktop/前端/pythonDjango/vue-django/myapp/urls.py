from django.conf.urls import url, include
from myapp import views
 
urlpatterns = [
    url(r'add_book$', views.add_book, ),
    url(r'show_books$', views.show_books, ),
    url(r'delete_book$', views.delete_book, ),
    url(r'update_book$', views.update_book, ),

]
