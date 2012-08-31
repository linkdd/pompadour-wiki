from django.core.urlresolvers import reverse
from django.conf import settings

from wiki.models import Wiki

def _infos():
    infos = {
        'title': 'Pompadour Wiki'
    }

    return infos

def _navbar():
    urls = {'navbar': [
        ('Home', reverse('home')),
    ]}

    for w in Wiki.objects.all():
        entry = (w.name, '/wiki/{0}/'.format(w.slug))

        urls['navbar'].append(entry)

    return urls

def pompadour(request):
    data = {'pompadour': {}}

    data['pompadour'].update(_infos())
    data['pompadour'].update(_navbar())

    return data
