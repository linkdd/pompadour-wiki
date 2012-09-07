from django import forms
from markitup.widgets import MarkItUpWidget

class EditPageForm(forms.Form):
    path = forms.CharField()
    content = forms.CharField(widget=MarkItUpWidget)

