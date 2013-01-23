# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from pompadour_wiki.apps.utils.decorators import render_to

from pompadour_wiki.apps.wiki.models import Wiki

@login_required
@render_to('index.html')
def home(request):
    wikis = Wiki.objects.all()

    return {"wiki": {
        "array": [wikis[x:x+3] for x in range(0, len(wikis), 3)]
    }}

@render_to('index.html')
def login_failed(request, message, status=None, template_name=None, exception=None):
    return {'error': message}

@render_to('files/files.html')
def test(request):
    return {}
