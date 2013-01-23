# -*- coding: utf-8 -*-

from django import forms

class UploadDocumentForm(forms.Form):
    path = forms.CharField()
    doc = forms.FileField()