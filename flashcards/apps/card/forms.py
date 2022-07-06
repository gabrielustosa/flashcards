from django import forms


class CardForm(forms.Form):
    word = forms.CharField(label='', max_length=50)
