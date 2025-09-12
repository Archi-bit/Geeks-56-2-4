from django import forms
from .models import Post

# первый вариант
class PostForm(forms.Form):
    image = forms.ImageField(required=True)
    title = forms.CharField(max_length=200, required=True)
    content = forms.CharField(max_length=556, required=True)

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        content = cleaned_data.get("content")
        if (title and content) and (title.lower() == content.lower()):
            raise forms.ValidationError("title and content cannot be the same")

# второй вариант
class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "image"]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        content = cleaned_data.get("content")
        if (title and content) and (title.lower() == content.lower()):
            raise forms.ValidationError("title and content cannot be the sametitle and content cannot be the same")
        return cleaned_data