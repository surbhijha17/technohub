from django import forms

from .models import Article,Comment

class CreateArticle(forms.ModelForm):
    class Meta:
        model=Article
        fields=['title' ,'body','slug','thumb','tags' ]
class CommentForm(forms.ModelForm):
    content = forms.CharField(label="",widget=forms.Textarea(attrs={'class': 'form-control','placeholder':'Leave a Comment...','rows':'2' ,}))
    class Meta:
        model=Comment
        fields=['content',]
