from app.models import *
from app.forms import *
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, render
from django.utils.encoding import smart_text

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
            if form.is_valid():
                post = form.save(commit=False)
                post.opis = request.POST.get('opis')
                post.nazwa = request.POST.get('nazwa')
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


def ticket(request, ticket_id):
    if request.method == 'POST':
        Ticket.objects.filter(id=ticket_id).update(pracownik=smart_text(request.user, encoding='utf-8', strings_only=False, errors='strict'))
        messages.add_message(request, messages.SUCCESS, 'Pomyślnie przypisano pracownika!')
        return redirect('ticket', ticket_id=ticket_id)
    if (request.user.groups.filter(name='Pracownik').exists()):
        try:
            this_ticket = Ticket.objects.get(id=ticket_id)
            context = {'this_ticket': this_ticket}
        except Ticket.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Ticket nie istnieje!')
            return redirect('index')
        return render(request, 'ticket.html', context)
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')


def tickets(request):
    if (request.user.groups.filter(name='Pracownik').exists()):
        tickets_list = Ticket.objects.all().order_by('-id')
        context = {'tickets_list': tickets_list}
        return render(request, 'tickets.html', context)
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')


def add_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.opis = request.POST.get('opis')
            if request.user.is_authenticated:
                post.zglaszajacy = request.user
            else:
                post.zglaszajacy = request.POST.get('zglaszajacy')
            post.save()
            messages.add_message(request, messages.SUCCESS, 'Pomyślnie dodano zgłoszenie!')
            return redirect('index')
        else:
            messages.add_message(request, messages.ERROR, 'Coś poszło nie tak!')
            return redirect('index')
    return render(request, 'add_ticket.html')


def delete_ticket(request, ticket_id):
    post = Ticket.objects.get(id=ticket_id)
    post.delete()
    messages.add_message(request, messages.SUCCESS, 'Pomyślnie usunięto!')
    return redirect('index')


def delete_event(request, event_id):
    post = Event.objects.get(id=event_id)
    post.delete()
    messages.add_message(request, messages.SUCCESS, 'Pomyślnie usunięto!')
    return redirect('index')
