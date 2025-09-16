from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(min_length=5, required=True, widget=forms.PasswordInput)
    password_confirm = forms.CharField(min_length=5, required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if (password and password) and (password != password_confirm):
            raise forms.ValidationError("Пароли не совпадают!")
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(min_length=5, required=True, widget=forms.PasswordInput)