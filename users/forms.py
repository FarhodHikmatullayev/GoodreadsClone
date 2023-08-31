from django import forms
from .models import User


# class CreateUserForm(forms.Form):
#     username = forms.CharField(max_length=221)
#     email = forms.EmailField()
#     password = forms.CharField(max_length=221)
#
#     def clean_password(self):
#         print(self.cleaned_data)
#         if len(self.cleaned_data.get('password')) < 8:
#             raise forms.ValidationError('parol 8 ta belgidan kop bolishi kerak')
#         return self.cleaned_data.get('password')
#
#     def save(self):
#         username = self.cleaned_data.get('username')
#         email = self.cleaned_data.get('email')
#         password = self.cleaned_data.get('password')
#
#         user = User.objects.create(
#             username=username,
#             email=email
#         )
#         user.set_password(password)
#         user.save()
#         return user


class CreateUserForm(forms.ModelForm):  # with ModelForm
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data.get('password'))
        user.save()
        return user


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'image')