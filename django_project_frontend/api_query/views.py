from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import main_form
from .models import Weathercache

from azure.servicebus import ServiceBusClient, ServiceBusMessage
import os

connstr = os.environ['SERVICE_BUS_CONNECTION_STR']
queue_name = os.environ['SERVICE_BUS_QUEUE_NAME']

def main_view(request):
    if request.method == 'POST':
        if (len(request.POST['date']) <= 10):
            with ServiceBusClient.from_connection_string(connstr) as client:
                with client.get_queue_sender(queue_name) as sender:
                    # Sending a single message
                    single_message = ServiceBusMessage(''.join(filter(str.isdigit, request.POST['date'])))
                    sender.send_messages(single_message)
                    return HttpResponseRedirect('/')
        else: pass
    context = {}
    data = Weathercache.objects.using('data').order_by('date__month', 'date__day', 'date__year')
    context = {'data': data,
        'form': main_form()
    }
    return render(request, "index.html", context)
