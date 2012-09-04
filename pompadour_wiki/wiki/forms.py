from django import forms

class EditPageForm(forms.Form):
    path = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)

