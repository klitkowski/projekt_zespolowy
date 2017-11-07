from app.models import *
from app.forms import *
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, render

# User in group: request.user.groups.filter(name='group_name').exists()


def index(request):
    event_list = Wydarzenie.objects.all().order_by('-id')
    context = {'event_list': event_list}
    return render(request, 'index.html', context)


def event(request, event_id):
    try:
        this_event = Wydarzenie.objects.get(id=event_id)
        context = {'this_event': this_event}
    except Wydarzenie.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Wydarzenie nie istnieje!')
        return redirect('index')
    return render(request, 'event.html', context)


def add_event(request):
    if (request.user.groups.filter(name='Administrator Budynku').exists()):
        building_list = Budynek.objects.all()
        context = {'building_list': building_list}
        if request.method == 'POST':
            form = EventForm(request.POST)
            print(form)
            if form.is_valid():
                post = form.save(commit=False)
                post.nazwa = request.POST.get('opis')
                post.opis = request.POST.get('nazwa')
                post.data = request.POST.get('data')
                post.budynek.id = request.POST.get('budynek')
                post.save()
                messages.add_message(request, messages.SUCCESS, 'Pomyślnie dodano wydarzenie!')
                return redirect('event', event_id=post.id)
            else:
                messages.add_message(request, messages.ERROR, 'Coś poszło nie tak!')
                return redirect('index')
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')
    return render(request, 'add_event.html', context)
