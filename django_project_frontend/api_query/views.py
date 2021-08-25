from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import main_form
from .models import Weathercache

from azure.servicebus import ServiceBusClient, ServiceBusMessage
import os
import datetime
from datetime import timedelta


connstr = os.environ['SERVICE_BUS_CONNECTION_STR']
queue_name = os.environ['SERVICE_BUS_QUEUE_NAME']

def main_view(request):
    if request.method == 'POST':
        # stress the server
        if request.POST['secret_command'] == os.environ['secret_command']:
            return HttpResponse('The self-burn process completed. <a href="/">Home</a>')

        if (len(request.POST['date']) <= 10) and (len(request.POST['date_to']) <= 10):
            # convert day string into date object
            day_from = datetime.datetime.strptime(''.join(filter(str.isdigit, request.POST['date'])), "%d%m%Y").date()
            day_to = datetime.datetime.strptime(''.join(filter(str.isdigit, request.POST['date_to'])), "%d%m%Y").date()

            # iterate over each day in the range and send it to the queue
            messages = []
            while day_from <= day_to:                
                messages.append(ServiceBusMessage(day_from.strftime("%d%m%Y")))
                day_from += timedelta(days=1)

            with ServiceBusClient.from_connection_string(connstr) as client:
                with client.get_queue_sender(queue_name) as sender:
                    sender.send_messages(messages)
            return HttpResponseRedirect('/')
                
        else: pass
    context = {}
    data = Weathercache.objects.using('data').order_by('date__month', 'date__day', 'date__year')
    context = {'data': data,
        'form': main_form()
    }
    return render(request, "index.html", context)
