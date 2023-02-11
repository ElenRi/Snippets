from django.forms import ModelForm, TextInput, Textarea
from MainApp.models import Snippet, Comment


class SnippetForm(ModelForm):
    class Meta:
        model = Snippet
        # Описываем поля, которые будем заполнять в форме
        fields = ['name', 'lang', 'code']
        labels = {'name': '', 'lang': '', 'code': ''}
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Название сниппета'}),
            'code': Textarea(attrs={'placeholder': 'Код сниппета'}),
        }

class CommentForm(ModelForm):
   class Meta:
       model = Comment
       fields = ['text']
       labels = { 'text': ''}
       widgets ={
           'text': Textarea(attrs={'placeholder': 'Текст комментария'})
       }