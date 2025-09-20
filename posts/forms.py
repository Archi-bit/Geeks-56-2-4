from django import forms
from .models import Post
from posts.models import Category

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
    
class SearchForm(forms.Form):
    search = forms.CharField(max_length=290, min_length=1, required=False)
    category_id = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label="Category")
    orderings = (
        (
            "created_at",
            "По дате создания"
        ),
        ("title", "По названию"),
        ("rate", "По рейтингу"),
        ("-created_at", "По дате создания (по убыванию)"),
        ("-title", "По названию (по убыванию)"),
        ("-rate", "По рейтингу (По убыванию)"),
        (
            None,
            "---",
        ),
    )
    ordering = forms.ChoiceField(choices=orderings, required=False)