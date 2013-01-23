# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext
from django.utils.timezone import utc
from django.conf import settings

from pompadour_wiki.apps.utils.decorators import render_to, redirect_to
from pompadour_wiki.apps.utils import urljoin

from pompadour_wiki.apps.wiki.models import Wiki
from pompadour_wiki.apps.wiki.forms import EditPageForm

from pompadour_wiki.apps.lock.models import Lock
from pompadour_wiki.apps.filemanager.models import Attachment

from pompadour_wiki.apps.utils.git_db import Repository
from pompadour_wiki.apps.markdown import pompadourlinks

import markdown
import datetime
import os

from collections import defaultdict

@login_required
@render_to('wiki/view.html')
def view_page(request, wiki, path):
    w = get_object_or_404(Wiki, slug=wiki)
    r = Repository(w.gitdir)

    if not path:
        return {'REDIRECT': urljoin(request.path, settings.WIKI_INDEX)}

    # If path is a folder
    if r.is_dir(path):
        if settings.WIKI_INDEX:
            return {'REDIRECT': urljoin(request.path, settings.WIKI_INDEX)}

        pages, name = r.get_tree(path)
        return {'wiki': {
            'name': name,
            'pages': pages,
            'obj': w
        }}

    real_path = u'{0}.md'.format(path)

    # If the page doesn't exist, redirect user to an edit page
    if not r.exists(real_path):
        return {'REDIRECT': reverse('edit-page', args=[wiki, path])}

    # Generate markdown document
    extension = pompadourlinks.makeExtension([
        ('base_url', u'/wiki/{0}/'.format(wiki)),
        ('end_url', ''),
    ])

    md = markdown.Markdown(
        extensions = ['meta', 'codehilite', 'toc', extension],
        safe_mode = True
    )

    content, name, mimetype = r.get_content(real_path)
    content = md.convert(content.decode('utf-8'))

    return {'wiki': {
        'name': os.path.splitext(name)[0],
        'path': real_path,
        'meta': md.Meta,
        'content': content,
        'history': r.get_history(),
        'obj': w,
        'attachments': Attachment.objects.filter(wiki=w, page=os.path.join(wiki, path)),
        'urls': {
            'edit': os.path.join(request.path, 'edit'),
            'remove': os.path.join(request.path, 'remove'),
        },
    }}

@login_required
@render_to('wiki/edit.html')
def edit_page(request, wiki, path):
    locked = False

    # check if a lock exists
    try:
        lock = Lock.objects.get(path=request.path)

        if lock.user != request.user:
            # check if the lock exists since more than 30 minutes
            dt = datetime.datetime.utcnow().replace(tzinfo=utc) - lock.timestamp

            if dt.total_seconds() >= 30*60:
                # The lock has expired
                # Reset it to the current user

                lock.user = request.user
                lock.timestamp = datetime.datetime.utcnow().replace(tzinfo=utc)
                lock.save()
            else:
                locked = True

    except Lock.DoesNotExist:
        lock = Lock()
        lock.path = request.path
        lock.user = request.user
        lock.timestamp = datetime.datetime.utcnow().replace(tzinfo=utc)
        lock.save()

    w = get_object_or_404(Wiki, slug=wiki)
    r = Repository(w.gitdir)
    name = ''

    # Save
    if request.method == 'POST':
        form = EditPageForm(request.POST)

        if form.is_valid():
            new_path = u'{0}.md'.format(u'-'.join(form.cleaned_data['path'].split(u' ')))

            os.environ['GIT_AUTHOR_NAME'] = u'{0} {1}'.format(request.user.first_name, request.user.last_name).encode('utf-8')
            os.environ['GIT_AUTHOR_EMAIL'] = request.user.email
            os.environ['USERNAME'] = str(request.user.username)

            commit = form.cleaned_data['comment'].encode('utf-8') or None

            r.set_content(new_path, form.cleaned_data['content'], commit_msg=commit)

            del(os.environ['GIT_AUTHOR_NAME'])
            del(os.environ['GIT_AUTHOR_EMAIL'])
            del(os.environ['USERNAME'])

            return {'REDIRECT': reverse('view-page', args=[wiki, path])}

    # Edit
    else:
        if not r.is_dir(path) and r.exists(u'{0}.md'.format(path)):
            content, name, mimetype = r.get_content(u'{0}.md'.format(path))
            form = EditPageForm({'path': path, 'content': content, 'comment': None})

        else:
            form = EditPageForm({'path': path})

    return {'wiki': {
        'name': os.path.splitext(name)[0],
        'path': path,
        'locked': locked,
        'lock': lock,
        'obj': w,
        'history': r.get_history(),
        'form': form,
        'attachments': Attachment.objects.filter(wiki=w, page=os.path.join(wiki, path)),
        'path': path,
    }}

@login_required
@redirect_to(lambda wiki, path: reverse('view-page', args=[wiki, path]))
def remove_page(request, wiki, path):
    w = get_object_or_404(Wiki, slug=wiki)
    r = Repository(w.gitdir)

    # Remove page
    os.environ['GIT_AUTHOR_NAME'] = u'{0} {1}'.format(request.user.first_name, request.user.last_name).encode('utf-8')
    os.environ['GIT_AUTHOR_EMAIL'] = request.user.email
    os.environ['USERNAME'] = str(request.user.username)

    r.rm_content(u'{0}.md'.format(path))

    del(os.environ['GIT_AUTHOR_NAME'])
    del(os.environ['GIT_AUTHOR_EMAIL'])
    del(os.environ['USERNAME'])

    # Remove attachements
    Attachment.objects.filter(wiki=w, page=os.path.join(wiki, path)).delete()

    return wiki, ''

@login_required
@render_to('wiki/search.html')
def search(request, wiki):
    w = get_object_or_404(Wiki, slug=wiki)
    r = Repository(w.gitdir)

    results = []

    if request.method == 'POST':
        pattern = request.POST['pattern']

        # Do the search
        out = r.git.grep('-i', '--cached', pattern)

        for line in out.splitlines():
            # Exclude __media__
            if not line.startswith('__media__'):
                sep = line.find(':')

                url = line[:sep]
                match = line[sep + 1:]

                # Remove markdown extension
                if url.endswith('.md'):
                    url = url[:url.rfind('.md')]

                # Append to the results
                results.append ((url, match))

        # Group results
        groups = defaultdict(list)

        for result in results:
            groups[result[0]].append(result[1])

        results = groups.items()
        print results

    return {'wiki': {
        'name': ugettext('Search'),
        'history': r.get_history(),
        'obj': w,
        'results': results,
        'urls': {
            'edit': os.path.join(request.path, 'edit'),
            'remove': os.path.join(request.path, 'remove'),
        },
    }}