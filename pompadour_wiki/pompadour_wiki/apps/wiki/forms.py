# -*- coding: utf-8 -*-

from django import forms

class EditPageForm(forms.Form):
    path = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)
    comment = forms.CharField(required=False)

