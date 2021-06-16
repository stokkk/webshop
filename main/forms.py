from django import forms


class CommentForm(forms.Form):
    # username = forms.CharField(max_length=100, widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'id': 'name',
    #     'placeholder': 'Имя пользователя'}
    # ))
    # email = forms.EmailField(max_length=100, widget=forms.EmailInput(
    #     attrs={'class': 'form-control', 'id': 'email',
    #     'placeholder': 'E-mail'}
    # ))
    comment = forms.CharField(max_length=1024, widget=forms.Textarea(
        attrs={'class': 'form-control', 'id': 'comment', 'rows': '9',
        'placeholder': 'Ваш комментарий'}
    ))
    rate = forms.FloatField(widget=forms.HiddenInput(
        attrs={'value': '5'}
    ))