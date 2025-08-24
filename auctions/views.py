from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import *


class ListingForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"name"}))
    category = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"category"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control", "placeholder":"Enter a description of the product here"}))
    start_bid = forms.IntegerField(widget=forms.NumberInput())
    image = forms.ImageField(widget=forms.FileInput())

class BidForm(forms.Form):
    bid = forms.IntegerField( label=False, widget=forms.NumberInput(attrs={"class":"form-control mb-2", "placeholder":"Bid"}))

class CommentForm(forms.Form):
    comment = forms.CharField(label=False, widget=forms.Textarea(attrs={"class":"form-control", "placeholder":"Write down your comments here"}))

def watchlist(request, user):
    current_user = User.objects.get(username=user)
    items = WatchList.objects.filter(user=current_user)
    context = {
        "auctions":items
    }
    return render(request, "auctions/watchlist.html", context)

def add(request, user, auct):
    current_user = User.objects.get(username=user)
    auction = AuctionList.objects.get(id=auct)
    new = WatchList(user=current_user, auction=auction)
    new.save()
    return HttpResponseRedirect(reverse("watchlist", args=[current_user.username]))


def remove(request, user, auct):
    current_user = User.objects.get(username=user)
    auction = AuctionList.objects.get(id=auct)
    new = WatchList.objects.get(user=current_user, auction=auction)
    new.delete()
    return HttpResponseRedirect(reverse("watchlist", args=[current_user.username]))

def comment(request, user, auction):
    comment = request.POST["comment"]
    auct = AuctionList.objects.get(name=auction)
    us = User.objects.get(username=user)
    com = Comment(auction=auct, user=us, comment=comment)
    com.save()
    return HttpResponseRedirect(reverse("listing", args=[auct.id, user]))

def speccat(request, cat):
    auctions = AuctionList.objects.filter(category=cat)
    context = {
        "auctions":auctions,
        "name":cat
    }
    return render(request, "auctions/cat.html", context)
    
def cat(request):
    auctions = AuctionList.objects.all()
    cats = set()
    for auction in auctions:
        cats.add(auction.category)
    context = {
        "cats":cats
    }
    return render(request, "auctions/categories.html", context)

def close(request, id):
    listing = AuctionList.objects.get(id=id)
    listing.active = "F"
    listing.save()
    biddings = Bid.objects.filter(auction=listing)
    highest_bid = 0
    winner = None
    for a in biddings:
        if a.bid > highest_bid:
            winner = a.user
    if winner:
        new_winner = Winner(user=winner, auction=listing)
        new_winner.save()
    
    return HttpResponseRedirect(reverse("index"))

def index(request):
    context = {
        "auctions":AuctionList.objects.all()
    }
    return render(request, "auctions/index.html", context)

def listing(request, id, us):   
    listing = AuctionList.objects.get(id=id)
    if us != '_':
        current_user = User.objects.get(username=us)
    try:
        check = WatchList.objects.get(user=current_user, auction=listing)
    except:
        check = None
        
    comments = Comment.objects.filter(auction=listing)

    if request.method == "GET":
        try:
            winner = Winner.objects.get(auction=listing).user
        except:
            winner = None
            
        context = {
            "listing":listing,
            "form":BidForm(),
            "form2":CommentForm(),
            "comments":comments,
            "check":check,
            "winner":winner
        }
        return render(request, "auctions/listing.html", context)
    else:
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.cleaned_data["bid"]
            if listing.actual_bid:
                if bid <= listing.actual_bid:
                    context = {
                        "listing":listing,
                        "form":form,
                        "form2":CommentForm(),
                        "check":check,
                        "comments":comments,
                        "error":f"Your bid must be greater than ${listing.actual_bid}"
                    }
                    return render(request, "auctions/listing.html", context)          
            if bid < listing.start_bid:
                    context = {
                        "listing":listing,
                        "form":form,
                        "form2":CommentForm(),
                        "check":check,
                        "comments":comments,
                        "error":f"Your bid must be greater than or equal to ${listing.start_bid}"
                    }
                    return render(request, "auctions/listing.html", context)
            listing.actual_bid = bid
            listing.save()
            listing = AuctionList.objects.get(id=id)
            user = User.objects.get(username=request.POST["user"]) 
            a = Bid(auction=listing, user=user, bid=bid)
            a.save()
            return HttpResponseRedirect(reverse("listing", args=[id, user]))     
        
        else:
            context = {
                "listing":listing,
                "form2":CommentForm(),
                "comments":comments,
                "check":check,
                "form":form
            }
            return render(request, "auctions/listing.html", context)

def create_listing(request):
    if request.method == "GET":
        context = {
            "form" : ListingForm()
        }
        return render(request,"auctions/create_listing.html", context)
    else:
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            description =form.cleaned_data["description"]
            name = form.cleaned_data["name"]
            start_bid =form.cleaned_data["start_bid"]
            image =request.FILES['image']
            category = form.cleaned_data["category"]
            user = User.objects.get(username=request.POST["user"]) 
            image_name = f"{image}"
            a = AuctionList(user=user, name=name.capitalize(), description=description, start_bid=start_bid, image=image, category=category, image_name=image_name)
            a.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            context = {
                "form":form
            }
            return render(request, "auctions/create_listing.html", context)

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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
