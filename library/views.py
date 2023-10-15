import django_filters
from django.contrib.auth import login
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from rest_framework.viewsets import ModelViewSet

from .forms import RegistrationFrom, BookAddForm, BookEditForm
from .models import Book, Comment
from .serializers import BookSerializer


class Register(View):
    def get(self, request):
        form = RegistrationFrom()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = RegistrationFrom(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('books')
        return render(request, 'registration/register.html', {'form': form})


class BooksView(ListView):
    paginate_by = 1
    model = Book
    context_object_name = 'books'
    template_name = 'books.html'


class BookView(View):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        comments = book.comments.all()
        context = {
            'book': book,
            'comments': comments,
        }
        return render(request, 'book.html', context)

    def post(self, request, pk):
        '''Публикация комментария на странице книги.'''
        comment = request.POST.get('comment')
        book = get_object_or_404(Book, pk=pk)
        if request.user.is_authenticated:
            comment_object = Comment(
                user=request.user,
                book=book,
                text=comment,
            )
            comment_object.save()
        return redirect(book)


class BookDeleteView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            book = get_object_or_404(Book, pk=pk)
            book.delete()
        return redirect('books')


class BookAddView(View):
    def get(self, request):
        form = BookAddForm()
        return render(request, 'book_add.html', {'form': form})

    def post(self, request):
        form = BookAddForm(request.POST, request.FILES)
        if form.is_valid() and request.user.is_authenticated:
            book = form.save()
            return redirect(book)
        return render(request, 'book_add.html', {'form': form})


class BookEditView(View):
    def get(self, request, pk):
        form = BookEditForm(instance=Book.objects.get(pk=pk))
        return render(request, 'book_edit.html', {'form': form})

    def post(self, request, pk):
        form = BookEditForm(
            instance=Book.objects.get(pk=pk),
            data=request.POST,
            files=request.FILES,
        )
        if form.is_valid() and request.user.is_authenticated:
            book = form.save()
            return redirect(book)
        return render(request, 'book_edit.html', {'form': form})


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class FilteredListView(ListView):
    filterset_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(
            self.request.GET,
            queryset=queryset,
        )
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class BookFilterSet(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = ['name', 'author__name']

    @property
    def qs(self):
        parent = super().qs
        q = getattr(self, 'data', None)['q']

        return parent.filter(name__icontains=q) \
            |  parent.filter(author__name__icontains=q)


class SearchView(FilteredListView):
    model = Book
    template_name = 'search.html'
    paginate_by = 1
    filterset_class = BookFilterSet
