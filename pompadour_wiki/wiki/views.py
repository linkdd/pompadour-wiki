from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.urlresolvers import reverse

from wiki.forms import EditPageForm
from wiki.models import Wiki
from wiki.git_db import Repository

from lock.models import Lock

from django.utils.timezone import utc
import datetime

import markdown

def _markdown_url_builder(label, base, end):
    return base + '/'.join(label.split('_')) + end

def _git_path(request, wiki):
    path = request.path.split('/{0}/'.format(wiki))[1]

    # Remove slashes
    while path and path[0] == '/':
        path = path[1:]

    while path and path[-1] == '/':
        path = path[:-1]

    return path

@login_required
def tree(request, wiki):
    w = get_object_or_404(Wiki, slug=wiki)
    r = Repository(w.gitdir)
    return HttpResponse(r.get_json_tree())

@login_required
def diff(request, wiki):
    w = get_object_or_404(Wiki, slug=wiki)
    r = Repository(w.gitdir)
    return HttpResponse(r.get_history())

@login_required
def edit(request, wiki):
    page_locked = False

    # Check if a lock exists
    try:
        lock = Lock.objects.get(path=request.path)
    except Lock.DoesNotExist:
        lock = None

    # Check if the lock exists since more than 30 minutes
    if lock:
        dt = datetime.datetime.utcnow().replace(tzinfo=utc) - lock.timestamp

        if dt.total_seconds() >= 30*60:
            # The lock has expired
            # Reset it to the current user

            lock.user = request.user
            lock.timestamp = datetime.datetime.utcnow().replace(tzinfo=utc)
            lock.save()
        else:
            page_locked = True
    else:
        lock = Lock()
        lock.path = request.path
        lock.user = request.user
        lock.timestamp = datetime.datetime.utcnow().replace(tzinfo=utc)
        lock.save()


    w = get_object_or_404(Wiki, slug=wiki)
    r = Repository(w.gitdir)
    path = _git_path(request, wiki)

    page_name = path

    if request.method == 'POST':
        form = EditPageForm(request.POST)

        if form.is_valid():
            r.set_content(form.cleaned_data['path'], form.cleaned_data['content'])

            return redirect('{0}/{1}'.format(reverse('page', args=[wiki]), path))
    else:
        if r.exists(path) and not r.is_dir(path):
            content, page_name = r.get_content(path)
            form = EditPageForm({'path': path, 'content': content})
        else:
            form = EditPageForm()

    data = {
        'menu_url': reverse('tree', args=[wiki]),
        'page_name': 'Edit: {0}'.format(page_name),
        'page_locked': page_locked,
        'lock': not page_locked and lock or None,
        'edit_path': path,
        'wiki': w,
        'form': form
    }

    return render_to_response('edit.html', data, context_instance=RequestContext(request))


@login_required
def page(request, wiki):
    w = get_object_or_404(Wiki, slug=wiki)
    r = Repository(w.gitdir)
    path = _git_path(request, wiki)

    # If the page doesn't exist, redirect user to an edit page
    if not r.exists(path):
        return redirect('{0}/{1}'.format(reverse('edit', args=[wiki]), path))

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
            extensions = ['meta', 'wikilinks', 'codehilite', 'toc'],
            extension_configs = {
                'wikilinks': [
                    ('base_url', '/wiki/{0}/'.format(wiki)),
                    ('end_url', '.md'),
                    ('build_url', _markdown_url_builder),
                ],
                'codehilite': [
                ],
            },
            safe_mode = True
        )
        content, name = r.get_content(path)

        page_content = md.convert(content.decode('utf-8'))

        data = {
            'menu_url': reverse('tree', args=[wiki]),
            'page_content': page_content,
            'page_meta': md.Meta,
            'page_name': name,
            'edit_url': '/edit/'.join(request.path.split('/wiki/')),
            'wiki': w,
        }

        return render_to_response('page.html', data, context_instance=RequestContext(request))
