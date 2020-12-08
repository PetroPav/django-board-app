from django import forms
from boards.models import Topic, Post

class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
               attrs={'rows':5,'placeholder':"What's on your mind?"}
               ),
        max_length=4000,
        help_text='Enter a maximum of 4000 characters'
        )

    class Meta:
        model = Topic
        fields = ['subject','message']

class PostForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
               attrs={'rows':5,'placeholder':"What's on your mind?"}
               ),
        max_length=4000,
        )

    class Meta:
        model = Post
        fields = ['message',]