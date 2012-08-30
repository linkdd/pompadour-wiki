from django.core.urlresolvers import reverse
from django.conf import settings


def _infos():
    infos = {
        'title': 'Pompadour Wiki'
    }

    return infos

def _navbar():
    urls = {'navbar': [
        ('Home', reverse('home')),
    ]}

    return urls

def pompadour(request):
    data = {'pompadour': {}}

    data['pompadour'].update(_infos())
    data['pompadour'].update(_navbar())

    return data
