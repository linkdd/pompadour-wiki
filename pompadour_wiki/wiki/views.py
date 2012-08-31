from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse

from wiki.models import Wiki
from wiki.gitdb import Repository

import markdown

def markdown_url_builder(label, base, end):
    return base + '/'.join(label.split('_')) + end

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

    if not r.exists(path):
        raise Http404

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
        md = markdown.Markdown(
            extensions = [ 'meta', 'wikilinks', 'codehilite'],
            extension_configs = {
                'wikilinks': [
                    ('base_url', '/wiki/{0}/'.format(wiki)),
                    ('end_url', '.md'),
                    ('build_url', markdown_url_builder),
                ]
            }
        )
        content, name = r.get_content(path)

        page_content = md.convert(content)

        data = {
            'menu_url': reverse('tree', args=[wiki]),
            'page_content': page_content,
            'page_meta': md.Meta,
            'page_name': name,
            'wiki': w,
        }

        return render_to_response('page.html', data, context_instance=RequestContext(request))
