from django.core.urlresolvers import reverse
from django.conf import settings

def nabvar(request):
    urls = {'navbar': [
        ('Home', reverse('home')),
    ]}

    return urls
