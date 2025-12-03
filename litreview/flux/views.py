from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from . import forms
from . import models


@login_required
def home(request):
    return render(request, 'flux/home.html')


@login_required
def tickets(request):
    tickets = models.Ticket.objects.all()
    return render(request, 'flux/tickets.html', {'tickets': tickets})


@login_required
def create_ticket(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            return redirect('home')
    return render(request, 'flux/create_ticket.html', context={'form': form})


@login_required
def modify_ticket(request, ticket_id):
    ticket = models.Ticket.objects.get(id=ticket_id)

    if request.method == 'POST':
        form = forms.TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = forms.TicketForm(instance=ticket)

    return render(request,
                  'flux/modify_ticket.html',
                  {'form': form})


@login_required
def delete_ticket(request, ticket_id):
    ticket = models.Ticket.objects.get(id=ticket_id)

    if request.method == 'POST':
        ticket.delete()
        return redirect('tickets')

    return render(request, 'flux/delete_ticket.html', {'ticket': ticket})
