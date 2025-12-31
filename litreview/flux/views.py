from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from . import forms
from . import models


@login_required
def home(request):
    '''
    Display a feed of tickets and reviews from the user and followed users.
    Also display reviews in response to tickets from logged-in user.
    '''
    # Retrieve logged-in user
    user = request.user

    # Get ids of users followed by logged-in user
    followed_user_ids = models.UserFollows.objects.filter(
        user=user
    ).values_list("followed_user_id", flat=True)

    posts = []

    # Retrieve tickets and reviews written by logged-in user and by followed users
    # Retrieve also all reviews in response to logged-in user tickets
    tickets = models.Ticket.objects.filter(Q(user=user) | Q(user__in=followed_user_ids))
    reviews = models.Review.objects.filter(
        Q(user=user) | Q(user__in=followed_user_ids) | Q(ticket__user=user)
    ).distinct()

    # Add type to distinguish tickets and reviews then append all to posts
    for ticket in tickets:
        ticket.type = "ticket"
        posts.append(ticket)

    for review in reviews:
        review.type = "review"
        posts.append(review)

    # Sort posts by antechronological order
    posts = sorted(posts, key=lambda post: post.time_created, reverse=True)

    # Retrieve ids of all tickets already reviewed by logged-in user to avoid reviewing tickets twice
    reviewed_tickets_id = models.Review.objects.filter(user=user).values_list("ticket_id", flat=True)

    star_range = range(1, 6)

    return render(
        request,
        "flux/home.html",
        {"posts": posts, "reviewed_tickets_id": reviewed_tickets_id, "star_range": star_range},
    )


@login_required
def subscriptions(request):
    '''
    Allow the user to manage their subscriptions to other users.
    Also display who the user follow and who follow the user.
    '''
    user_subscriptions = models.UserFollows.objects.filter(user=request.user)
    subscriptions_to_user = models.UserFollows.objects.filter(followed_user=request.user)

    subscribe_form = forms.UserSubscriptionForm(user=request.user)
    unsubscribe_form = forms.CancelUserSubscriptionForm()

    if request.method == "POST":
        if "subscribe" in request.POST:
            subscribe_form = forms.UserSubscriptionForm(request.POST, user=request.user)
            if subscribe_form.is_valid():
                user_follows = subscribe_form.save(commit=False)
                user_follows.user = request.user
                user_follows.save()
                return redirect("subscriptions")
        if "unsubscribe" in request.POST:
            unsubscribe_form = forms.CancelUserSubscriptionForm(request.POST)
            if unsubscribe_form.is_valid():
                subscription_id = unsubscribe_form.cleaned_data["subscription_id"]
                user_follows = get_object_or_404(models.UserFollows, pk=subscription_id, user=request.user)
                user_follows.delete()
                return redirect("subscriptions")

    else:
        subscribe_form = forms.UserSubscriptionForm(user=request.user)

    return render(
        request,
        "flux/subscriptions.html",
        {
            "subscribe_form": subscribe_form,
            "unsubscribe_form": unsubscribe_form,
            "user_subscriptions": user_subscriptions,
            "subscriptions_to_user": subscriptions_to_user,
        },
    )


@login_required
def posts(request):
    '''Display a feed containing the tickets and reviews of the user.'''
    user = request.user

    tickets = models.Ticket.objects.filter(user=user)
    reviews = models.Review.objects.filter(user=user)

    posts = []

    for ticket in tickets:
        ticket.type = "ticket"
        posts.append(ticket)

    for review in reviews:
        review.type = "review"
        posts.append(review)

    posts = sorted(posts, key=lambda post: post.time_created, reverse=True)

    star_range = range(1, 6)

    return render(request, "flux/posts.html", {"posts": posts, "star_range": star_range})


@login_required
def create_ticket(request):
    '''Allow the user to create a new ticket.'''
    form = forms.TicketForm()
    if request.method == "POST":
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            return redirect("home")
    return render(request, "flux/create_ticket.html", context={"form": form})


@login_required
def create_review(request, ticket_id):
    '''Allow the user to create a new review.'''
    ticket = models.Ticket.objects.get(id=ticket_id)
    form = forms.ReviewForm()

    page_title = "Créer une critique"

    if request.method == "POST":
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("home")

    return render(
        request, "flux/create_or_modify_review.html", {"ticket": ticket, "form": form, "page_title": page_title}
    )


@login_required
def create_ticket_and_review(request):
    '''Allow the user to create a new ticket and a new review.'''
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()

    if request.method == "POST":
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
            return redirect("home")

    return render(
        request, "flux/create_ticket_and_review.html", {"ticket_form": ticket_form, "review_form": review_form}
    )


@login_required
def modify_ticket(request, ticket_id):
    '''Allow the user to modify a ticket.'''
    ticket = get_object_or_404(models.Ticket, pk=ticket_id, user=request.user)

    if request.method == "POST":
        form = forms.TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect("posts")
    else:
        form = forms.TicketForm(instance=ticket)

    return render(request, "flux/modify_ticket.html", {"form": form, "ticket": ticket})


@login_required
def modify_review(request, ticket_id, review_id):
    '''Allow the user to modify a review.'''
    review = get_object_or_404(models.Review, pk=review_id, user=request.user)
    ticket = models.Ticket.objects.get(id=ticket_id)

    page_title = "Modifier votre critique"

    if request.method == "POST":
        form = forms.ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("posts")
    else:
        form = forms.ReviewForm(instance=review)

    return render(
        request, "flux/create_or_modify_review.html", {"ticket": ticket, "form": form, "page_title": page_title}
    )


@login_required
def delete_ticket(request, ticket_id):
    '''Allow the user to delete a ticket.'''
    ticket = get_object_or_404(models.Ticket, pk=ticket_id, user=request.user)

    if request.method == "POST":
        ticket.delete()
        return redirect("posts")

    return render(request, "flux/delete_ticket.html", {"ticket": ticket})


@login_required
def delete_review(request, ticket_id, review_id):
    '''Allow the user to delete a review.'''
    review = get_object_or_404(models.Review, pk=review_id, user=request.user)
    ticket_id = models.Ticket.objects.get(id=ticket_id)

    if request.method == "POST":
        review.delete()
        return redirect("posts")

    return render(request, "flux/delete_review.html", {"review": review})
