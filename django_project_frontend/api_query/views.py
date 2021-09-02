from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import main_form
from .models import Weathercache

from azure.servicebus import ServiceBusClient, ServiceBusMessage
from os import getenv
import datetime
from datetime import timedelta
from multiprocessing import Pool
from multiprocessing import cpu_count
from .tests import stress

connstr = getenv('SERVICE_BUS_CONNECTION_STR')
queue_name = getenv('SERVICE_BUS_QUEUE_NAME')

def main_view(request):
    context = {}
    if (request.method == 'POST'):
        form_main = main_form(request.POST)
        # stress the server for env STRESS_MINS minutes
        if request.POST['secret_command'] == getenv('secret_command'):
            processes = cpu_count()
            pool = Pool(processes)
            pool.map(stress, range(processes))
            return HttpResponse('The self-burn process completed. <a href="/">Home</a>')

        # Display - to get data from the DB
        if form_main.is_valid:             
            if (request.POST['behaviour'] == 1):
                data = Weathercache.objects.using('data').filter(date__gte=form_main.cleaned_data['date']).filter(date__lte=form_main.cleaned_data['date_to']).order_by('date__month', 'date__day', 'date__year')
            # Fetch - to upload new data into the DB.
            elif (request.POST['behaviour'] == 2):
                day_from = datetime.datetime.strptime(''.join(filter(str.isdigit, form_main.cleaned_data['date'])), "%d%m%Y").date()
                day_to = datetime.datetime.strptime(''.join(filter(str.isdigit, form_main.cleaned_data['date_to'])), "%d%m%Y").date()

                # iterate over each day in the range and send it to the queue
                messages = []
                while day_from <= day_to:                
                    messages.append(ServiceBusMessage(day_from.strftime("%d%m%Y")))
                    day_from += timedelta(days=1)

                with ServiceBusClient.from_connection_string(connstr) as client:
                    with client.get_queue_sender(queue_name) as sender:
                        sender.send_messages(messages)
                return HttpResponseRedirect('/')
    # get request
    else:
        form_main = main_form()           

    context = { 'data': data,
        'form': form_main,
    }
    return render(request, "index.html", context)
