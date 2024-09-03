from django import forms
from django.contrib.auth import get_user_model

# Получение текущей модели пользователя
User = get_user_model()


# Создание формы регистрации пользователя
class UserRegistrationForm(forms.ModelForm):
    # Создание дополнительного поля пароля для повторного ввода при регистрации
    password2 = forms.CharField(label='Повторите пароль',
                                widget=forms.PasswordInput)  # widget=forms.PasswordInput - скрытый ввод

    def clean_password2(self):
        cleaned_data = self.cleaned_data
        if cleaned_data['password'] != cleaned_data['password2']:
            raise forms.ValidationError('Пароли не совпадают!')  # Если пароли не совпадают - генерируем исключение
        return cleaned_data['password2']

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'phone', 'city')
