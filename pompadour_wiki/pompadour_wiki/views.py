from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def home(request):
    return HttpResponse('<a href="/login/">Login</a>')

@login_required
def done(request):
    return HttpResponse('<h1>' + str(request.user.username) + '</h1>')
