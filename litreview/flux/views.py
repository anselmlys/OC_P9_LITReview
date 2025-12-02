from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from . import forms


@login_required
def home(request):
    return render(request, 'flux/home.html')


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
