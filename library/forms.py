from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Book


class RegistrationFrom(UserCreationForm):
    class Meta:
        model=User
        fields = ['username', 'email', 'password1', 'password2'] 

    
class BookAddForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
    

class BookEditForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

    def validate_unique(self) -> None:
        '''
        Переопределение валидации
        для возможности редактирования полей,
        не указанных в unique_together.
        '''
        name = self.cleaned_data['name']
        author = self.cleaned_data['author']
        publish_year = self.cleaned_data['publish_year']
        book = Book.objects.get(
            name=name,
            author=author,
            publish_year=publish_year,
        )
        if not self.instance == book:
            return super().validate_unique()