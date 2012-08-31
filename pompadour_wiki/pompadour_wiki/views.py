from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from wiki.models import Wiki

def home(request):
    wikis = Wiki.objects.all()

    data = {
        'wikis': [wikis[x:x+3] for x in xrange(0, len(wikis), 3)]
    }

    return render_to_response('home.html', data, context_instance=RequestContext(request))
