from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from . import forms
from . import models


@login_required
def home(request):
    return render(request, 'flux/home.html')


@login_required
def tickets(request):
    tickets = models.Ticket.objects.all()
    reviews = models.Review.objects.all()
    return render(request, 'flux/tickets.html', {'tickets': tickets, 'reviews': reviews})


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
def create_review(request, ticket_id):
    ticket = models.Ticket.objects.get(id=ticket_id)
    form = forms.ReviewForm()

    page_title = "Créer une critique"

    if request.method == 'POST':
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')

    return render(request, 'flux/create_or_modify_review.html',
                  {'ticket': ticket, 'form': form, 'page_title': page_title})


@login_required
def create_ticket_and_review(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()

    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if any([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')

    return render(request,
                  'flux/create_ticket_and_review.html',
                  {'ticket_form': ticket_form,
                   'review_form': review_form})


@login_required
def modify_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, pk=ticket_id, user=request.user)

    if request.method == 'POST':
        form = forms.TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = forms.TicketForm(instance=ticket)

    return render(request,
                  'flux/modify_ticket.html',
                  {'form': form, 'ticket': ticket})


@login_required
def modify_review(request, ticket_id, review_id):
    review = get_object_or_404(models.Review, pk=review_id, user=request.user)
    ticket = models.Ticket.objects.get(id=ticket_id)

    page_title = "Modifier votre critique"

    if request.method == 'POST':
        form = forms.ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = forms.ReviewForm(instance=review)

    return render(request, 'flux/create_or_modify_review.html',
                  {'ticket': ticket, 'form': form, 'page_title': page_title})


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, pk=ticket_id, user=request.user)

    if request.method == 'POST':
        ticket.delete()
        return redirect('tickets')

    return render(request, 'flux/delete_ticket.html', {'ticket': ticket})

@login_required
def delete_review(request, ticket_id, review_id):
    review = get_object_or_404(models.Review, pk=review_id, user=request.user)
    ticket = models.Ticket.objects.get(id=ticket_id)

    if request.method == 'POST':
        review.delete()
        return redirect('tickets')
    
    return render(request, 'flux/delete_review.html', {'review': review})
