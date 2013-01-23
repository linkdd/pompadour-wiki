# -*- coding: utf-8 -*-

from django.template.defaultfilters import slugify
from django.template.loader import render_to_string, get_template
from django.template import RequestContext, Context
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext
from django.conf import settings

from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax

from pompadour_wiki.apps.wiki.models import Wiki
from pompadour_wiki.apps.utils.git_db import Repository
from pompadour_wiki.apps.markdown import pompadourlinks
from pompadour_wiki.apps.utils import logdebug

from pygments import highlight
from pygments.lexers import DiffLexer
from pygments.formatters import HtmlFormatter
import markdown

import os

@dajaxice_register
def add_wiki(request, dform=None):
    dajax = Dajax()

    if not dform:
        return dajax.json()

    wiki = Wiki()
    wiki.name = dform['add-wiki-name'].encode('utf-8')
    wiki.slug = slugify(wiki.name)
    wiki.description = dform['add-wiki-desc'].encode('utf-8')
    wiki.gitdir = os.path.join(settings.WIKI_GIT_DIR, wiki.slug)

    try:
        w = Wiki.objects.get(slug=wiki.slug)

        dajax.assign('#error', 'innerHTML',
                    render_to_string('error.html',
                                     {'error': ugettext(u'Can\'t add wiki, another wiki with the same name ({0}) already exists.').format(wiki.name)},
                                     context_instance=RequestContext(request)
                    )
        )

    except Wiki.DoesNotExist:
        os.environ['GIT_AUTHOR_NAME'] = u'{0} {1}'.format(request.user.first_name, request.user.last_name).encode('utf-8')
        os.environ['GIT_AUTHOR_EMAIL'] = request.user.email
        os.environ['USERNAME'] = str(request.user.username)

        r = Repository.new(wiki.gitdir)

        del(os.environ['GIT_AUTHOR_NAME'])
        del(os.environ['GIT_AUTHOR_EMAIL'])
        del(os.environ['USERNAME'])

        wiki.save()

        dajax.redirect(reverse('view-page', args=[wiki.slug, '']))

    return dajax.json()

@dajaxice_register
def load_menu(request, slug=None, path=None):
    dajax = Dajax()

    if not slug or not path:
        return dajax.json()

    # Retrieve wiki object
    try:
        wiki = Wiki.objects.get(slug=slug)
    except Wikit.DoesNotExist:
        return dajax.json()

    # Get repository tree
    r = Repository(wiki.gitdir)
    tree = r.get_tree()
    node = tree['node']

    # Create template
    tmpl = get_template('wiki/menuitem.html')
    itemid = [0]

    # Generate the menu from the templates
    def buildtree(node):
        ret = u''

        for element in node['children']:              
            # Now parse the file
            element['node']['path'] = os.path.splitext(element['node']['path'])[0]
            element['node']['name'] = os.path.splitext(element['node']['name'])[0]

            if element['node']['type'] == 'tree':
                itemid[0] += 1

                data = {
                    'is_folder_item': True,
                    'checked': element['node']['path'] in path,
                    'wiki': wiki,
                    'node': element['node'],
                    'itemid': itemid[0],
                    'submenu_html': buildtree(element['node'])
                }

                ret = u'{0}\n{1}'.format(ret, tmpl.render(Context(data)))

            else:
                data = {
                    'is_folder_item': False,
                    'checked': False,
                    'wiki': wiki,
                    'node': element['node']
                }

                ret = u'{0}\n{1}'.format(ret, tmpl.render(Context(data)))

        return ret

    # Assign generated HTML to element
    dajax.assign('#wiki-menu', 'innerHTML', buildtree(node))

    return dajax.json()

@dajaxice_register
def edit_preview(request, dform=None, wiki=None):
    dajax = Dajax()

    if not dform or not wiki:
        return dajax.json()

    content = dform['content']

    # Generate markdown document
    extension = pompadourlinks.makeExtension([
        ('base_url', u'/wiki/{0}/'.format(wiki)),
        ('end_url', ''),
    ])

    md = markdown.Markdown(
        extensions = ['meta', 'codehilite', 'toc', extension],
        safe_mode = True
    )

    content = md.convert(content)
    dajax.assign('#edit-preview', 'innerHTML', content)

    return dajax.json()

@dajaxice_register
def show_diff(request, sha=None, parent_sha=None, wiki=None):
    dajax = Dajax()

    if not sha or not parent_sha or not wiki:
        return dajax.json()

    # Retrieve git repository
    try:
        w = Wiki.objects.get(slug=wiki)
    except Wiki.DoesNotExist:
        return dajax.json()

    r = Repository(w.gitdir)

    diff = r.git.diff(parent_sha, sha).decode('utf-8')

    dajax.assign('#diff', 'innerHTML', highlight(diff, DiffLexer(), HtmlFormatter(cssclass='codehilite')))

    return dajax.json()
