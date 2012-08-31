from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.core.urlresolvers import reverse

from wiki.models import Wiki
from wiki.gitdb import Repository

@login_required
def tree(request, wiki):
    w = get_object_or_404(Wiki, slug=wiki)

    r = Repository(w.gitdir)

    return HttpResponse(r.get_json_tree())

@login_required
def page(request, wiki):
    w = get_object_or_404(Wiki, slug=wiki)

    r = Repository(w.gitdir)

    path = request.path.split('/wiki/{0}/'.format(wiki))[1]

    # Remove trailing slashes
    if path:
        while path[-1] == '/':
            path = path[:-1]

    if r.is_dir(path):
        pages, name = r.get_tree(path)
        data = {
            'menu_url': reverse('tree', args=[wiki]),
            'pages': pages,
            'page_name': name,
            'wiki': w,
        }

        return render_to_response('pages.html', data, context_instance=RequestContext(request))

    else:
        content, name = r.get_content(path)
        data = {
            'menu_url': reverse('tree', args=[wiki]),
            'page_content': content,
            'page_name': name,
            'wiki': w,
        }

        return render_to_response('page.html', data, context_instance=RequestContext(request))
