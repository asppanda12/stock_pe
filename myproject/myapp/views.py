from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.templatetags.static import static
from django.http import HttpResponse
import http.client
import urllib.parse
import json
import requests
import ipaddress
import requests
import json
from requests.structures import CaseInsensitiveDict
import urllib.request
from django.contrib.staticfiles.storage import staticfiles_storage
from .models import UserDetails, Portfolio
from django.contrib.auth.models import User, auth
from django.contrib import messages
import pandas as pdr
import numpy as np
import numpy

# Create your views here.


def get_static(path):
    if settings.DEBUG:
        return find(path)
    else:
        return static(path)


def index(request):
    return render(request, "login.html")


def login1(request):
    return render(request, "login.html")


def home(request):
    return render(request, "home.html")


def register1(request):
    return render(request, "register.html")


def router(request):
    userdetails = UserDetails.objects.get(user=request.user)

    val = UserDetails.objects.get(user=request.user)
    hamara = Portfolio.objects.filter(userdetails=userdetails)

    return render(request, 'binomo.html', {'portfolio': hamara, 'val': val})


def buy(request):
    hamara = Portfolio.objects.all()
    val = UserDetails.objects.get(user=request.user)
    return render(request, "buy.html", {'portfolio': hamara, 'val': val})


def sell(request):
    hamara = Portfolio.objects.all()
    val = UserDetails.objects.get(user=request.user)
    return render(request, "sell.html", {'portfolio': hamara, 'val': val})


def take_form(request):

    goals = request.POST.get("GOAL", False)
    saving = request.POST.get("SAVING", False)
    option = request.POST.get("stocks", False)
    print(goals)
    print(saving)
    print(option == "NTPC")
    if option == "NTPC":
        filepath = get_static('NTPCp.csv')
        df = pdr.read_csv(filepath)

        df2 = df['Close'].tolist()
        goal1 = int(goals)
        savings = int(saving)
        print(goal1)
        today = 131
        no_of_share = (savings/today)+1
        val = 0
        ind = 0
        for i in df2:
            val = i*no_of_share-savings
            if goal1 < int(val):
                break
            else:
                ind = ind+1

        print("valhaya{}", format(val))

        no_of_dd = ind
        print("period ha ya{}", format(no_of_dd))
        per_return = (goal1+savings)/savings
        thisdict = None
        thisdict = {
            "Goal": goal1,
            "saving": savings,
            "Period": no_of_dd,
            "share": no_of_share,
            "per_return": per_return,
            "inflation": 12,
            "stock": option
        }
        print(thisdict)

    return render(request, "index.html", {"thisdict": thisdict})


def buyshare(request):

    context = {}
    portfolio = {}
    hamara = {}
    if request.method == "POST":
        print(request.user)
        no_of_shares = int(request.POST.get('Quantity', False))
        stock_name = request.POST.get('stocks', False)
        stock_cc = int(request.POST.get('stock_cc', False))
        userdetails = UserDetails.objects.get(user=request.user)
        if((no_of_shares*stock_cc) > userdetails.saving):
            messages.info(request, 'pls enter a valid share no')
            return redirect('buyshare')
        userdetails.saving = userdetails.saving-(no_of_shares*stock_cc)
        userdetails.save()

        if Portfolio.objects.filter(userdetails=userdetails).filter(stock_name=stock_name).exists():
            portfolio = Portfolio.objects.filter(
                userdetails=userdetails).filter(stock_name=stock_name)[0]
            previous_no_of_shares = portfolio.no_of_share
            previous_stock_cc = portfolio.stock_cc
            portfolio.no_of_share = previous_no_of_shares+no_of_shares
            if ((portfolio.stock_cc) != 0):
                portfolio.stock_cc = (previous_stock_cc+stock_cc)/2
            else:
                portfolio.stock_cc = stock_cc
            portfolio.save()

        else:
            new_portfolio = Portfolio(
                userdetails=userdetails, stock_name=stock_name, no_of_share=no_of_shares, stock_cc=stock_cc)
            new_portfolio.save()

        hamara = Portfolio.objects.filter(userdetails=userdetails)
        val = {}
        val = UserDetails.objects.get(user=request.user)
    return render(request, 'binomo.html', {'portfolio': hamara, 'val': val})


def sellshare(request):
    if request.user.is_anonymous:
        return redirect('/')
    portfolio = {}
    if request.method == "POST":
        stock_name = request.POST.get('stocks')
        no_of_shares = int(request.POST.get('Quantity'))
        sell_price = int(request.POST.get('selling price'))
        print(stock_name)
        print(no_of_shares)
        print(sell_price)
        userdetails = UserDetails.objects.get(user=request.user)

        if Portfolio.objects.filter(userdetails=userdetails).filter(stock_name=stock_name).exists():
            portfolio = Portfolio.objects.filter(
                userdetails=userdetails).filter(stock_name=stock_name)[0]
            if((portfolio.no_of_share) < no_of_shares):
                messages.info(request, 'pls enter a valid share no')
                return redirect('sellshare')
            portfolio.total_profit = portfolio.total_profit + \
                (no_of_shares*sell_price-no_of_shares*(portfolio.stock_cc))
            if((portfolio.no_of_share) == no_of_shares):
                portfolio.stock_cc = 0
            portfolio.no_of_share = portfolio.no_of_share-no_of_shares
            portfolio.save()
        hamara = Portfolio.objects.filter(userdetails=userdetails)
        val = UserDetails.objects.get(user=request.user)
    return render(request, 'binomo.html', {'portfolio': hamara, 'val': val})


def register(request):

    if request.method == "POST":
        account = request.POST.get('account')
        saving = request.POST.get('saving')

        username = request.POST.get('username')
        password = request.POST.get('password')
        user1 = User.objects.create_user(
            username, 'sameerpanda.2019', password)
        user1.save()

        new_portfolio = UserDetails(user=user1, account=account, saving=saving)
        new_portfolio.save()
        print(new_portfolio)
    hamara = {}
    val = UserDetails.objects.get(user=user1)
    return render(request, 'login.html')


def login(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            userdetails = UserDetails.objects.get(user=request.user)

            val = UserDetails.objects.get(user=request.user)
            hamara = Portfolio.objects.filter(userdetails=userdetails)

            return render(request, 'profile.html', {'portfolio': hamara, 'val': val})
        else:
            return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')
