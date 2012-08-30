from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from wiki.models import Wiki
from wiki.gitdb import Repository

@login_required
def page(request, wiki):
    w = get_object_or_404(Wiki, slug=wiki)

    r = Repository(w.gitdir)

    path = request.path.split('/wiki/{0}/'.format(wiki))[1]

    # Remove trailing slashes
    while path[-1] == '/':
        path = path[:-1]

    if r.is_dir(path):
        data = {
            'pages': r.get_tree(path),
            'wiki': wiki,
        }

        return render_to_response('pages.html', data, context_instance=RequestContext(request))

    else:
        data = {
            'page_content': r.get_content(path),
            'wiki': wiki,
        }

        return render_to_response('page.html', data, context_instance=RequestContext(request))
