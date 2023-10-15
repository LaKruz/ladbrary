from django.urls import include, path
from .views import (
    BooksView,
    BookView,
    BookViewSet,
    SearchView,
    BookDeleteView,
    BookAddView,
    BookEditView,
)
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'api/books', BookViewSet)

urlpatterns = [
    path('books/', BooksView.as_view(), name='books'),
    path('books/add', BookAddView.as_view(), name='book_add'),
    path('books/<int:pk>', BookView.as_view(), name='book'),
    path('books/<int:pk>/delete', BookDeleteView.as_view(), name='book_delete'),
    path('books/<int:pk>/edit', BookEditView.as_view(), name='book_edit'),
    path('search/', SearchView.as_view(), name='search'),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
] + router.urls
