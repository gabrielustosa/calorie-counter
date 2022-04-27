from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'name', 'height', 'weight', 'birthday')
        labels = {'username': 'E-mail'}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

# class UserEditForm(UserChangeForm):
#     class Meta:
#         model = User
#         fields = ('name',)
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_method = 'post'
#         self.helper.add_input(Submit('save_customer', 'Salvar'))
#         self.helper.layout = Layout(
#             Row(
#                 Column('first_name'),
#                 Column('last_name')
#             ),
#             'email',
#             'username',
#         )
