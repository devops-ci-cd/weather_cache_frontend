from django.shortcuts import render
from .forms import main_form
from .models import Weathercache

def main_view(request):
    context = {}
    data = Weathercache.objects.using('data').all()
    context = {'data': data,
        'form': main_form()
    }
    return render(request, "index.html", context)
