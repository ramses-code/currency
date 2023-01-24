import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Transaction


def index(request):

    return render(request, "capstone/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "capstone/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "capstone/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "capstone/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "capstone/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "capstone/register.html")

@login_required
def transaction(request):

    if request.method == 'GET':
        return render(request, 'capstone/transaction.html', {
            'transactions': request.user.user_transactions.order_by('-timestamp').all()
        })

    if request.method == 'POST':
        amount = request.POST['hidden_currancy_amount']
        currancy_from = request.POST['hidden_currancy_from']
        currancy_to = request.POST['hidden_currancy_to']
        total = request.POST['hidden_total']

        new_transaction = Transaction(user=request.user, amount=float(amount), currancy_from=currancy_from, currancy_to=currancy_to, total=float(total))
        new_transaction.save()
        return HttpResponseRedirect(reverse('transaction'))