from django import forms

class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

