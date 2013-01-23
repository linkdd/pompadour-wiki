# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from pompadour_wiki.apps.wiki.models import Wiki

def pompadour(request):
    data = {'pompadour': {
        'title': u'Pompadour Wiki',
        'navbar': []
    }}

    for w in Wiki.objects.all():
        e = (w.name, reverse('view-page', args=[w.slug, '']))

        data['pompadour']['navbar'].append(e)

    return data
