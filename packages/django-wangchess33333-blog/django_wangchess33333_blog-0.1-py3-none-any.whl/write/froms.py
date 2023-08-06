from django import forms
class Write(forms.Form):
    title2 = forms.CharField(label="title", max_length=300, widget=forms.TextInput(attrs={'class': 'form-control'}))
    body = forms.CharField(label="body",  widget=forms.TextInput(attrs={'class': 'form-control'}))
