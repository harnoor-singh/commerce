from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *
from . import util


def index(request):
    active_listings = [listing for listing in Listing.objects.filter(is_active=True)]
    if len(active_listings) > 0:
        return render(request, "auctions/index.html", {
            "active_listings": active_listings           
        })
    else: 
        return render(request, "auctions/index.html", {
            "message": "No active listings.",
            "active_listings": False
        })


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

@login_required(login_url="login")
def createListing(request):
    if request.method == "POST":
        listing = Listing(
            creator=User.objects.get(username=request.user),
            title=request.POST["title"],
            description=request.POST["description"],
            starting_bid=request.POST["starting_bid"],
            image_url=request.POST["image_url"]
            )
        listing.save()
        util.add_category(request, listing)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/createListing.html")


def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    bids = Bid.objects.filter(listing=listing)
    comments = Comment.objects.filter(listing=listing)

    bids_list = [bid.bid_value for bid in bids]
    bids_list.append(listing.starting_bid)
    current_bid = max(bids_list)

    if request.user.is_authenticated:
        watchlist =  [listing for listing in request.user.watchlist.all()]
    else:
        watchlist = []
    
    listing_in_watchlist = True if listing in watchlist else False

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bids": bids,
        "comments": comments,
        "len_comments": len(comments),
        "current_bid": current_bid,
        "listing_in_watchlist": listing_in_watchlist
        })


def watchlist(request):
    if request.user.is_authenticated:
        # the all() function is necessary two lines below,
        # otherwise, there is an error.
        user_watchlist = [listing for listing in request.user.watchlist.all()]
        if request.method == "POST":
            if request.POST["listing_bool"] == "True":
                request.user.watchlist.remove(
                    Listing.objects.get(id=int(request.POST["listing_id"])))
                return HttpResponseRedirect(reverse(
                    'listing', args=(request.POST["listing_id"],)))
            else:
                request.user.watchlist.add(
                    Listing.objects.get(id=int(request.POST["listing_id"])))
                return HttpResponseRedirect(reverse(
                    'listing', args=(request.POST["listing_id"],)))

        else:
            return render(request, "auctions/watchlist.html", {
                "watchlist": user_watchlist,
                "len_watchlist": len(user_watchlist),
                "message": False
                })

    else:
        return render(request, "auctions/watchlist.html", {
            "message": True
            })


def categories(request):
    list_of_categories = [category for category in Category.objects.all()]
    return render(request, "auctions/categories.html", {
        "list_of_categories": list_of_categories
        })


def category(request, category_id):
    category = Category.objects.get(id=category_id)
    list_of_listings = [listing for listing in category.category_listings.all()]
    return render(request, "auctions/category.html", {
        "category": category,
        "list_of_listings": list_of_listings
        })



@login_required(login_url="login")
def createComment(request):
    if request.method == "POST":
        comment = Comment(
            author=User.objects.get(username=request.POST["creator"]),
            listing=Listing.objects.get(id=request.POST["listing_id"]),
            comment_text=request.POST["content"]
            )
        comment.save()
        return HttpResponseRedirect(reverse(
            'listing', args=(request.POST["listing_id"],)))

