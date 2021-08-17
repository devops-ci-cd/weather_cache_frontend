from django.shortcuts import render
from .forms import main_form
from .models import Weathercache

def main_view(request):
    context = {}
    context['form'] = main_form()
    data = Weathercache.objects.using('data').all()
    context['data'] = {'data': data}
    return render(request, "index.html", context)
