from app.models import *
from app.forms import *
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, render
from django.utils.encoding import smart_text
from reportlab.pdfgen import canvas
from django.http import HttpResponse


def index(request):
    event_list = Wydarzenie.objects.all().order_by('-id')
    context = {'event_list': event_list}
    return render(request, 'index.html', context)


def delete(request, del_id):
    post = eval(str(request.POST.get('name'))).objects.get(id=del_id)
    post.delete()
    messages.add_message(request, messages.SUCCESS, 'Pomyślnie usunięto!')
    return redirect('index')


def event(request, event_id):
    try:
        entry = Wydarzenie.objects.get(id=event_id)
        context = {'entry': entry}
    except Wydarzenie.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Wydarzenie nie istnieje!')
        return redirect('index')
    return render(request, 'event.html', context)


def add_event(request):
    if (request.user.groups.filter(name='Pracownik').exists()):
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


def edit_event(request, event_id):
    try:
        this_item = Wydarzenie.objects.get(id=event_id)
        context = {'this_item': this_item}
    except Wydarzenie.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Takie wydarzenie nie istnieje!')
        return redirect('index')
    if (request.user.groups.filter(name='Pracownik').exists()):
        building_list = Budynek.objects.all()
        context['building_list'] = building_list
        if request.method == 'POST':
            form = EventForm(request.POST, instance=this_item)
            if form.is_valid():
                post = form.save(commit=False)
                post.opis = request.POST.get('opis')
                post.nazwa = request.POST.get('nazwa')
                post.data = request.POST.get('data')
                post.budynek.id = request.POST.get('budynek')
                post.save()
                messages.add_message(request, messages.SUCCESS, 'Pomyślnie edytowano wydarzenie!')
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
            entry = Ticket.objects.get(id=ticket_id)
            context = {'entry': entry}
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

def edit_ticket(request, ticket_id):
    try:
        this_item = Ticket.objects.get(id=ticket_id)
        context = {'this_item': this_item}
    except Ticket.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Takie zgłoszenie nie istnieje!')
        return redirect('index')
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=this_item)
        if form.is_valid():
            post = form.save(commit=False)
            post.opis = request.POST.get('opis')
            if request.user.is_authenticated:
                post.zglaszajacy = str(request.user)
            else:
                post.zglaszajacy = request.POST.get('zglaszajacy')
            post.save()
            messages.add_message(request, messages.SUCCESS, 'Pomyślnie edytowano zgłoszenie!')
            return redirect('index')
        else:
            messages.add_message(request, messages.ERROR, 'Coś poszło nie tak!')
            return redirect('index')
    return render(request, 'add_ticket.html', context)


def invoice(request, invoice_id):
    if (request.user.groups.filter(name='Pracownik').exists()):
        try:
            entry = Faktura.objects.get(id=invoice_id)
            context = {'entry': entry}
        except Faktura.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Faktura nie istnieje!')
            return redirect('index')
        return render(request, 'invoice.html', context)
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')


def invoices(request):
    if (request.user.groups.filter(name='Pracownik').exists()):
        invoice_list = Faktura.objects.all().order_by('-id')
        context = {'invoice_list': invoice_list}
        return render(request, 'invoices.html', context)
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')


def add_invoice(request):
    if (request.user.groups.filter(name='Pracownik').exists()):
        issuers_list = Wystawca.objects.all()
        owners_list = Wlasciciel.objects.all()
        context = {'issuers_list': issuers_list, 'owners_list': owners_list}
        if request.method == 'POST':
            form = FakturaForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.wartosc_netto = float(request.POST.get('wartosc_netto'))
                post.wystawca.id = int(request.POST.get('wystawca'))
                post.wlasciciel.id = int(request.POST.get('wlasciciel'))
                post.save()
                messages.add_message(request, messages.SUCCESS, 'Pomyślnie dodano fakture!')
                return redirect('invoice', invoice_id=post.id)
            else:
                messages.add_message(request, messages.ERROR, 'Coś poszło nie tak!')
                return redirect('index')
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')
    return render(request, 'add_invoice.html', context)


def edit_invoice(request, invoice_id):
    try:
        this_item = Faktura.objects.get(id=invoice_id)
        context = {'this_item': this_item}
    except Faktura.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Taka faktura nie istnieje!')
        return redirect('index')
    if (request.user.groups.filter(name='Pracownik').exists()):
        issuers_list = Wystawca.objects.all()
        owners_list = Wlasciciel.objects.all()
        context['issuers_list'] = issuers_list
        context['owner_list'] = owners_list
        if request.method == 'POST':
            form = FakturaForm(request.POST, instance=this_item)
            if form.is_valid():
                post = form.save(commit=False)
                post.wartosc_netto = float(request.POST.get('wartosc_netto'))
                post.wystawca.id = int(request.POST.get('wystawca'))
                post.wlasciciel.id = int(request.POST.get('wlasciciel'))
                post.save()
                messages.add_message(request, messages.SUCCESS, 'Pomyślnie edytowano fakture!')
                return redirect('invoice', invoice_id=post.id)
            else:
                messages.add_message(request, messages.ERROR, 'Coś poszło nie tak!')
                return redirect('index')
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')
    return render(request, 'add_invoice.html', context)


def issuer(request, issuer_id):
    if (request.user.groups.filter(name='Pracownik').exists()):
        try:
            entry = Wystawca.objects.get(id=issuer_id)
            context = {'entry': entry}
        except Wystawca.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Wystawca nie istnieje!')
            return redirect('index')
        return render(request, 'issuer.html', context)
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')


def issuers(request):
    if (request.user.groups.filter(name='Pracownik').exists()):
        issuers_list = Wystawca.objects.all().order_by('-id')
        context = {'issuers_list': issuers_list}
        return render(request, 'issuers.html', context)
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')


def add_issuer(request):
    if (request.user.groups.filter(name='Pracownik').exists()):
        if request.method == 'POST':
            form = WystawcaForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.nazwa = request.POST.get('nazwa')
                post.kod_pocztowy = request.POST.get('kod_pocztowy')
                post.miasto = request.POST.get('miasto')
                post.ulica = request.POST.get('ulica')
                post.telefon = request.POST.get('telefon')
                post.email = request.POST.get('email')
                post.save()
                messages.add_message(request, messages.SUCCESS, 'Pomyślnie dodano wystawce!')
                return redirect('issuers', issuer_id=post.id)
            else:
                messages.add_message(request, messages.ERROR, 'Coś poszło nie tak!')
                return redirect('index')
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')
    return render(request, 'add_issuer.html')


def edit_issuer(request, issuer_id):
    try:
        this_item = Wystawca.objects.get(id=issuer_id)
        context = {'this_item': this_item}
    except Wystawca.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Taki wystawca nie istnieje!')
        return redirect('index')
    if (request.user.groups.filter(name='Pracownik').exists()):
        if request.method == 'POST':
            form = WystawcaForm(request.POST, instance=this_item)
            if form.is_valid():
                post = form.save(commit=False)
                post.nazwa = request.POST.get('nazwa')
                post.kod_pocztowy = request.POST.get('kod_pocztowy')
                post.miasto = request.POST.get('miasto')
                post.ulica = request.POST.get('ulica')
                post.telefon = request.POST.get('telefon')
                post.email = request.POST.get('email')
                post.save()
                messages.add_message(request, messages.SUCCESS, 'Pomyślnie edytowano wystawce!')
                return redirect('issuers', issuer_id=post.id)
            else:
                messages.add_message(request, messages.ERROR, 'Coś poszło nie tak!')
                return redirect('index')
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')
    return render(request, 'add_issuer.html', context)


def owner(request, owner_id):
    if (request.user.groups.filter(name='Pracownik').exists()):
        try:
            entry = Wlasciciel.objects.get(id=owner_id)
            context = {'entry': entry}
        except Wlasciciel.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Właściciel nie istnieje!')
            return redirect('index')
        return render(request, 'owner.html', context)
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')


def owners(request):
    if (request.user.groups.filter(name='Pracownik').exists()):
        owners_list = Wlasciciel.objects.all().order_by('-id')
        context = {'owners_list': owners_list}
        return render(request, 'owners.html', context)
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')


def add_owner(request):
    flat_list = Mieszkanie.objects.all()
    context = {'flat_list': flat_list}
    if (request.user.groups.filter(name='Pracownik').exists()):
        if request.method == 'POST':
            form = WlascicielForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.imie = request.POST.get('imie')
                post.nazwisko = request.POST.get('nazwisko')
                post.telefon = request.POST.get('telefon')
                post.email = request.POST.get('email')
                post.mieszkanie.id = int(request.POST.get('mieszkanie'))
                post.save()
                messages.add_message(request, messages.SUCCESS, 'Pomyślnie dodano właściciela!')
                return redirect('owners', owner_id=post.id)
            else:
                messages.add_message(request, messages.ERROR, 'Coś poszło nie tak!')
                return redirect('index')
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')
    return render(request, 'add_owner.html', context)


def edit_owner(request, owner_id):
    try:
        this_item = Wlasciciel.objects.get(id=owner_id)
        context = {'this_item': this_item}
    except Wlasciciel.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Taki właściciel nie istnieje!')
        return redirect('index')
    if (request.user.groups.filter(name='Pracownik').exists()):
        flat_list = Mieszkanie.objects.all()
        context = {'flat_list': flat_list}
        if request.method == 'POST':
            form = WlascicielForm(request.POST, instance=this_item)
            if form.is_valid():
                post = form.save(commit=False)
                post.imie = request.POST.get('imie')
                post.nazwisko = request.POST.get('nazwisko')
                post.telefon = request.POST.get('telefon')
                post.email = request.POST.get('email')
                post.mieszkanie.id = int(request.POST.get('mieszkanie'))
                post.save()
                messages.add_message(request, messages.SUCCESS, 'Pomyślnie edytowano właściciela!')
                return redirect('owners', owner_id=post.id)
            else:
                messages.add_message(request, messages.ERROR, 'Coś poszło nie tak!')
                return redirect('index')
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')
    return render(request, 'add_owner.html', context)



def counter(request, counter_id):
    if (request.user.groups.filter(name='Pracownik').exists()):
        try:
            entry = Licznik.objects.get(id=counter_id)
            context = {'entry': entry}
        except Licznik.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Licznik nie istnieje!')
            return redirect('index')
        return render(request, 'counter.html', context)
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')


def counters(request):
    if (request.user.groups.filter(name='Pracownik').exists()):
        counters_list = Licznik.objects.all().order_by('-id')
        context = {'counters_list': counters_list}
        return render(request, 'counters.html', context)
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')


def add_counter(request):
    if (request.user.groups.filter(name='Pracownik').exists()):
        if request.method == 'POST':
            form = LicznikForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.typ = request.POST.get('typ')
                post.cena_netto = float(request.POST.get('cena_netto'))
                post.save()
                messages.add_message(request, messages.SUCCESS, 'Pomyślnie dodano licznik!')
                return redirect('counter', counter_id=post.id)
            else:
                messages.add_message(request, messages.ERROR, 'Coś poszło nie tak!')
                return redirect('index')
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')
    return render(request, 'add_counter.html')


def edit_counter(request, counter_id):
    try:
        this_item = Licznik.objects.get(id=counter_id)
        context = {'this_item': this_item}
    except Licznik.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Taki licznik nie istnieje!')
        return redirect('index')
    if (request.user.groups.filter(name='Pracownik').exists()):
        if request.method == 'POST':
            form = LicznikForm(request.POST, instance=this_item)
            if form.is_valid():
                post = form.save(commit=False)
                post.typ = request.POST.get('typ')
                post.cena_netto = float(request.POST.get('cena_netto'))
                post.save()
                messages.add_message(request, messages.SUCCESS, 'Pomyślnie edytowano licznik!')
                return redirect('counter', counter_id=post.id)
            else:
                messages.add_message(request, messages.ERROR, 'Coś poszło nie tak!')
                return redirect('index')
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')
    return render(request, 'add_counter.html', context)


def counter_state(request, counter_state_id):
    if (request.user.groups.filter(name='Pracownik').exists()):
        try:
            entry = StanLicznik.objects.get(id=counter_state_id)
            context = {'entry': entry}
        except StanLicznik.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Stan licznika nie istnieje!')
            return redirect('index')
        return render(request, 'counter_state.html', context)
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')


def counter_states(request):
    if (request.user.groups.filter(name='Pracownik').exists()):
        counter_state_list = StanLicznik.objects.all().order_by('-id')
        context = {'counter_state_list': counter_state_list}
        return render(request, 'counter_states.html', context)
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')


def add_counter_state(request):
    if (request.user.groups.filter(name='Pracownik').exists()):
        counters_list = Licznik.objects.all()
        flat_list = Mieszkanie.objects.all()
        context = {'counters_list': counters_list, 'flat_list': flat_list}
        if request.method == 'POST':
            form = StanLicznikForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.typ.id = int(request.POST.get('typ'))
                post.mieszkanie.id = int(request.POST.get('mieszkanie'))
                post.stan = float(request.POST.get('stan'))
                post.save()
                messages.add_message(request, messages.SUCCESS, 'Pomyślnie dodano stan licznika!')
                return redirect('counter_state', counter_state_id=post.id)
            else:
                messages.add_message(request, messages.ERROR, 'Coś poszło nie tak!')
                return redirect('index')
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')
    return render(request, 'add_counter_state.html', context)


def edit_counter_state(request, counter_state_id):
    try:
        this_item = Licznik.objects.get(id=owner_id)
        context = {'this_item': this_item}
    except Licznik.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Taki licznik nie istnieje!')
        return redirect('index')
    if (request.user.groups.filter(name='Pracownik').exists()):
        counters_list = Licznik.objects.all()
        flat_list = Mieszkanie.objects.all()
        context = {'counters_list': counters_list}
        context = {'flat_list': flat_list}
        if request.method == 'POST':
            form = StanLicznikFormForm(request.POST, instance=this_item)
            if form.is_valid():
                post = form.save(commit=False)
                post.typ.id = int(request.POST.get('typ'))
                post.mieszkanie.id = int(request.POST.get('mieszkanie'))
                post.stan = float(request.POST.get('stan'))
                post.save()
                messages.add_message(request, messages.SUCCESS, 'Pomyślnie edytowano stan licznika!')
                return redirect('counter_state', counter_state_id=post.id)
            else:
                messages.add_message(request, messages.ERROR, 'Coś poszło nie tak!')
                return redirect('index')
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')
    return render(request, 'add_counter_state.html', context)


def add_worker(request):
    table = {
        ord('ą'): 'a',
        ord('ć'): 'c',
        ord('ę'): 'e',
        ord('ł'): 'l',
        ord('ń'): 'n',
        ord('ó'): 'o',
        ord('ś'): 's',
        ord('ź'): 'z',
        ord('ż'): 'z',
        ord('Ą'): 'A',
        ord('Ć'): 'C',
        ord('Ę'): 'E',
        ord('Ł'): 'L',
        ord('Ń'): 'N',
        ord('Ó'): 'O',
        ord('Ś'): 'S',
        ord('Ź'): 'Z',
        ord('Ż'): 'Z',
    }
    position_list = Stanowisko.objects.all()
    address_list = Adres.objects.all()
    groups = Group.objects.all()
    context = {'position_list': position_list, 'address_list': address_list, 'groups': groups}
    if (request.user.groups.filter(name='Pracownik').exists()):
        if request.method == 'POST':
            form = PracownikForm(request.POST)
            if form.is_valid():
                username = request.POST.get('imie')[:1] + request.POST.get('nazwisko')
                username.translate(table)
                user, created = User.objects.get_or_create(username=username.lower())
                while not created:
                    i = 1
                    user, created = User.objects.get_or_create(username=username.lower() + str(i))
                    i += 1
                user.set_password(username.lower() + '!1')
                user.email = request.POST.get('email')
                user.groups.add(int(request.POST.get('stanowisko')))
                user.save()
                post = form.save(commit=False)
                post.imie = request.POST.get('imie')
                post.nazwisko = request.POST.get('nazwisko')
                post.telefon = request.POST.get('telefon')
                post.email = request.POST.get('email')
                post.stanowisko.id = int(request.POST.get('stanowisko'))
                post.adres.id = int(request.POST.get('adres'))
                post.user = user
                post.save()
                messages.add_message(request, messages.SUCCESS, 'Pomyślnie dodano pracownika!')
                return redirect('index')
            else:
                messages.add_message(request, messages.ERROR, 'Coś poszło nie tak!')
                return redirect('index')
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')
    return render(request, 'add_worker.html', context)


def add_position(request):
    if (request.user.groups.filter(name='Pracownik').exists()):
        if request.method == 'POST':
            form = StanowiskoForm(request.POST)
            if form.is_valid():
                group, created = Group.objects.get_or_create(name=request.POST.get('nazwa'))
                if not created:
                    messages.add_message(request, messages.ERROR, 'Podane stanowisko już istnieje!')
                    return redirect('index')
                group.save()
                post = form.save(commit=False)
                post.nazwa = request.POST.get('nazwa')
                post.pensja = request.POST.get('pensja')
                post.save()
                messages.add_message(request, messages.SUCCESS, 'Pomyślnie dodano stanowisko!')
                return redirect('positions', position_id=post.id)
            else:
                messages.add_message(request, messages.ERROR, 'Coś poszło nie tak!')
                return redirect('index')
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')
    return render(request, 'add_position.html')


def edit_position(request, position_id):
    try:
        this_item = Stanowisko.objects.get(id=position_id)
        context = {'this_item': this_item}
    except Stanowisko.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Takie stanowisko nie istnieje!')
        return redirect('index')
    if (request.user.groups.filter(name='Pracownik').exists()):
        if request.method == 'POST':
            form = StanowiskoForm(request.POST, instance=this_item)
            if form.is_valid():
                group, created = Group.objects.get_or_create(name=request.POST.get('nazwa'))
                if not created:
                    messages.add_message(request, messages.ERROR, 'Podane stanowisko już istnieje!')
                    return redirect('index')
                group.save()
                post = form.save(commit=False)
                post.nazwa = request.POST.get('nazwa')
                post.pensja = request.POST.get('pensja')
                post.save()
                messages.add_message(request, messages.SUCCESS, 'Pomyślnie edytowano stanowisko!')
                return redirect('positions', position_id=post.id)
            else:
                messages.add_message(request, messages.ERROR, 'Coś poszło nie tak!')
                return redirect('index')
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')
    return render(request, 'add_position.html', context)


def overtime(request, overtime_id):
    if (request.user.groups.filter(name='Pracownik').exists()):
        try:
            entry = Nadgodziny.objects.get(id=overtime_id)
            context = {'entry': entry}
        except Nadgodziny.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Podane nadgodziny nie istnieją!')
            return redirect('index')
        return render(request, 'overtime.html', context)
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')


def overtimes(request):
    if (request.user.groups.filter(name='Pracownik').exists()):
        overtime_list = Nadgodziny.objects.all().order_by('-id')
        context = {'overtime_list': overtime_list}
        return render(request, 'overtimes.html', context)
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')


def add_overtime(request):
    if (request.user.groups.filter(name='Pracownik').exists()):
        worker_list = Pracownik.objects.all()
        context = {'worker_list': worker_list}
        if request.method == 'POST':
            form = NadgodzinyForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.ilosc = float(request.POST.get('ilosc'))
                post.pracownik.id = int(request.POST.get('pracownik'))
                post.save()
                messages.add_message(request, messages.SUCCESS, 'Pomyślnie dodano nadgodziny pracownikowi!')
                return redirect('overtime', overtime=post.id)
            else:
                messages.add_message(request, messages.ERROR, 'Coś poszło nie tak!')
                return redirect('index')
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')
    return render(request, 'add_overtime.html', context)


def edit_overtime(request, overtime):
    try:
        this_item = Pracownik.objects.get(id=overtime)
        context = {'this_item': this_item}
    except Pracownik.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Taki pracownik nie istnieje!')
        return redirect('index')
    if (request.user.groups.filter(name='Pracownik').exists()):
        worker_list = Pracownik.objects.all()
        context = {'worker_list': worker_list}
        if request.method == 'POST':
            form = NadgodzinyForm(request.POST, instance=this_item)
            if form.is_valid():
                post = form.save(commit=False)
                post.ilosc = float(request.POST.get('ilosc'))
                post.pracownik.id = int(request.POST.get('pracownik'))
                post.save()
                messages.add_message(request, messages.SUCCESS, 'Pomyślnie edytowano nadgodziny!')
                return redirect('overtime', overtime=post.id)
            else:
                messages.add_message(request, messages.ERROR, 'Coś poszło nie tak!')
                return redirect('index')
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')
    return render(request, 'add_overtime.html', context)


def building_address(request, building_address_id):
    if (request.user.groups.filter(name='Pracownik').exists()):
        try:
            entry = AdresBudynek.objects.get(id=building_address_id)
            context = {'entry': entry}
        except AdresBudynek.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Podane adres nie istnieje!')
            return redirect('index')
        return render(request, 'building_address.html', context)
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')


def add_building_address(request):
    if (request.user.groups.filter(name='Pracownik').exists()):
        if request.method == 'POST':
            form = AdresBudynekForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.kod_pocztowy = request.POST.get('kod_pocztowy')
                post.miasto = request.POST.get('miasto')
                post.ulica = request.POST.get('ulica')
                post.save()
                messages.add_message(request, messages.SUCCESS, 'Pomyślnie dodano adres budynku!')
                return redirect('building_address', building_address_id=post.id)
            else:
                messages.add_message(request, messages.ERROR, 'Coś poszło nie tak!')
                return redirect('index')
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')
    return render(request, 'add_building_address.html')


def edit_building_address(request, building_address_id):
    try:
        this_item = AdresBudynek.objects.get(id=building_address_id)
        context = {'this_item': this_item}
    except AdresBudynek.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Taki adres budynku nie istnieje!')
        return redirect('index')
    if (request.user.groups.filter(name='Pracownik').exists()):
        if request.method == 'POST':
            form = AdresBudynekForm(request.POST, instance=this_item)
            if form.is_valid():
                post = form.save(commit=False)
                post.kod_pocztowy = request.POST.get('kod_pocztowy')
                post.miasto = request.POST.get('miasto')
                post.ulica = request.POST.get('ulica')
                post.save()
                messages.add_message(request, messages.SUCCESS, 'Pomyślnie edytowano adres budynku!')
                return redirect('building_address', building_address_id=post.id)
            else:
                messages.add_message(request, messages.ERROR, 'Coś poszło nie tak!')
                return redirect('index')
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')
    return render(request, 'add_building_address.html', context)


def address(request, address_id):
    if (request.user.groups.filter(name='Pracownik').exists()):
        try:
            entry = Adres.objects.get(id=address_id)
            context = {'entry': entry}
        except Adres.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Podane adres nie istnieje!')
            return redirect('index')
        return render(request, 'address.html', context)
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')


def add_address(request):
    if (request.user.groups.filter(name='Pracownik').exists()):
        if request.method == 'POST':
            form = AdresForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.kod_pocztowy = request.POST.get('kod_pocztowy')
                post.miasto = request.POST.get('miasto')
                post.ulica = request.POST.get('ulica')
                post.save()
                messages.add_message(request, messages.SUCCESS, 'Pomyślnie dodano adres!')
                return redirect('address', address_id=post.id)
            else:
                messages.add_message(request, messages.ERROR, 'Coś poszło nie tak!')
                return redirect('index')
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')
    return render(request, 'add_address.html')


def edit_address(request, address_id):
    try:
        this_item = Adres.objects.get(id=address_id)
        context = {'this_item': this_item}
    except Adres.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Taki adres nie istnieje!')
        return redirect('index')
    if (request.user.groups.filter(name='Pracownik').exists()):
        if request.method == 'POST':
            form = AdresForm(request.POST, instance=this_item)
            if form.is_valid():
                post = form.save(commit=False)
                post.kod_pocztowy = request.POST.get('kod_pocztowy')
                post.miasto = request.POST.get('miasto')
                post.ulica = request.POST.get('ulica')
                post.save()
                messages.add_message(request, messages.SUCCESS, 'Pomyślnie edytowano adres!')
                return redirect('address', address_id=post.id)
            else:
                messages.add_message(request, messages.ERROR, 'Coś poszło nie tak!')
                return redirect('index')
    else:
        messages.add_message(request, messages.ERROR, 'Nie możesz tego zrobić!')
        return redirect('index')
    return render(request, 'add_address.html', context)


def pdf(request, invoice_id):
    if (request.user.groups.filter(name='Pracownik').exists()):
        try:
            this_invoice = Faktura.objects.get(id=invoice_id)
        except Faktura.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Faktura nie istnieje!')
            return redirect('index')
        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="faktura.pdf"'

        # Create the PDF object, using the response object as its "file."
        p = canvas.Canvas(response)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        p.drawString(100, 100, this_invoice.wlasciciel.imie)

        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()
        return response