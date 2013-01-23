# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from functools import wraps

def render_to(template_name=None, mimetype=None):
    """
        Render function to a template.

        @render_to('template.html')
        def foo(request):
            return {'foo': 'bar'}

        is equivalent to

        def foo(request):
            return render_to_response('template.html', {'foo': 'bar'}, context_instance=RequestContext(request))

        and

        @render_to()
        def foo(request):
            return {'foo': 'bar', 'TEMPLATE': 'template.html'}

        is equivalent to

        def foo(request):
            return render_to_response('template.html', {'foo': 'bar'}, context_instance=RequestContext(request))

        You can, conditionnaly send a HttpResponseRedirect :

        @render_to('template.html')
        def foo(request):
            if bar:
                return {'REDIRECT': 'redirect url'}

            return {'foo': 'bar'}
    """

    def renderer(function):
        @wraps(function)
        def wrapper(request, *args, **kwargs):
            output = function(request, *args, **kwargs)

            if not isinstance(output, dict):
                return output

            redirect_url = output.pop('REDIRECT', False)

            if redirect_url:
                return HttpResponseRedirect(redirect_url)

            template = output.pop('TEMPLATE', template_name)

            return render_to_response(template, output, context_instance=RequestContext(request), mimetype=mimetype)

        return wrapper

    return renderer

def redirect_to(url):
    """
        Perform a HTTP 302 redirect.

        @redirect_to('url')
        def foo(request):
            pass

        @redirect_to(lambda: reverse('home'))
        def bar(request):
            pass

        @redirect_to(lambda arg: reverse('page', args=[arg]))
        def baz(request):
            return 'arg'
    """

    def outer(function):
        @wraps(function)
        def wrapper(request, *args, **kwargs):
            rargs = function(request, *args, **kwargs)

            if not callable(url):
                return HttpResponseRedirect(url)

            elif not rargs:
                return HttpResponseRedirect(url())
            else:
                return HttpResponseRedirect(url(*rargs))

        return wrapper

    return outer

