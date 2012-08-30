from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):
    data = {
        'test': 'test',
    }

    return render_to_response('home.html', data, context_instance=RequestContext(request))
