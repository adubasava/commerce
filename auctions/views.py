from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import NewListingForm
from django.contrib.auth.decorators import login_required

from .models import User, Category, Listing, Bid, Comment


# View all of the currently active auction listings
def index(request):
    # Counter for Watchlist menu badge (not required by specification)
    try:
        count = len(request.user.watchlist.all())
        return render(request, "auctions/index.html", {
            "listings": Listing.objects.filter(active=True),
            "count": count
        })
    except AttributeError:
        return render(request, "auctions/index.html", {
            "listings": Listing.objects.filter(active=True),
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


# Create Listing
def create(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            listing = Listing()
            listing.title = form.cleaned_data["title"]
            listing.description = form.cleaned_data["description"]
            listing.starting_bid = form.cleaned_data["starting_bid"]
            listing.image_url = form.cleaned_data["image_url"]
            listing.category = form.cleaned_data["category"]
            listing.user = request.user
            listing.save()            
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponse("Input is not valid")
    else:
        form = NewListingForm
        count = len(request.user.watchlist.all())
        return render(request, "auctions/create.html", {
            "form": form,
            "count": count
        })
    

# Listing Page
def listing(request, id):
    listing = Listing.objects.get(pk=id)        
    bid = Bid.objects.filter(item=listing).last()
    inWatchlist = request.user in listing.watchlist.all()
    comments = Comment.objects.filter(listing=listing)
    isOwner = request.user == listing.user
    # Number of bids for the listing (not required by specification)
    total = len(Bid.objects.filter(item=listing))
    # Number of comments for the listing (not required by specification)
    totalCom = len(Comment.objects.filter(listing=listing))
    # Counter for Watchlist menu badge (not required by specification)
    try:
        count = len(request.user.watchlist.all())
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "inWatchlist": inWatchlist,
            "comments": comments,
            "isOwner": isOwner,
            "bid": bid,
            "total": total,
            "totalCom": totalCom,
            "count": count
        })
    except AttributeError:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "inWatchlist": inWatchlist,
            "comments": comments,
            "isOwner": isOwner,
            "bid": bid,
            "total": total,
            "totalCom": totalCom,
        })


# Watchlist Page
@login_required
def watchlist(request):   
    count = len(request.user.watchlist.all())
    return render(request, "auctions/watchlist.html", {
        "watchlist": request.user.watchlist.all(),
        "count": count
    })
    

# Add to Watchlist
@login_required
def add(request, id):
    listing = Listing.objects.get(pk=id)
    listing.watchlist.add(request.user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))  
    

# Remove from Watchlist
@login_required
def remove(request, id):
    listing = Listing.objects.get(pk=id)
    listing.watchlist.remove(request.user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))  


# Add Comment
@login_required
def comment(request, id):
    comment = Comment(
        user=request.user,
        listing = Listing.objects.get(pk=id),
        text = request.POST["comment"],
    )
    comment.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))


# Place Bid
def bid(request, id):
    listing = Listing.objects.get(pk=id)
    old = Bid.objects.filter(item=listing).last()
    bid = float(request.POST["bid"])
    comments = Comment.objects.filter(listing=listing)
    total = len(Bid.objects.filter(item=listing))
    # if other bids have been placed already
    if old:
        # new bid is greater than oldest one
        if bid > old.bid:
            new = Bid(user=request.user, bid=bid, item=listing)
            new.save()
            listing.starting_bid = new.bid
            listing.save()
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "comments": comments,
                "total": total+1
            })
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "message": "You bid is not bigger than previous one!",
                "comments": comments,
                "total": total
            })
    # if there are no other bids
    else:
        # new bid is at least as large as the starting bid
        if bid >= listing.starting_bid:
            new = Bid(user=request.user, bid=bid, item=listing)
            new.save()
            listing.starting_bid = new.bid
            listing.save()
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "comments": comments,
                "total": total+1
            })
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "message": "You bid is less than previous one!",
                "comments": comments,
                "total": total
            })
        

# Close Auction
@login_required
def close(request, id):    
    listing = Listing.objects.get(pk=id)
    listing.active = False
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))  


# Show list of all categories
def categories(request):  
    count = len(request.user.watchlist.all()) 
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all(),
        "count": count
    })


# All active listings in a particular category
def category(request, name):
    try:
        category = Category.objects.filter(name=name)[0]
        listings = Listing.objects.filter(category=category, active="True")
        return render(request, "auctions/category.html", {
            "listings": listings,
            "name": name,
        })
    except (ValueError, IndexError):
        return render(request, "auctions/categories.html", {
            "categories": Category.objects.all()
        })