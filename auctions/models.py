from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Listing is a string because Listing is not defined yet.
    watchlist = models.ManyToManyField('Listing', blank=True, related_name="associated_watchlists")

class Category(models.Model):
    category_name = models.CharField(max_length=64)

    def __str__(self):
        return f"id:{self.id}, {self.category_name}"

class Listing(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    image_url = models.URLField(blank=True)
    category = models.ManyToManyField(Category, blank=True, related_name="category_listings")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"id:{self.id}, title:{self.title}, creator={self.creator}"
    

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids_made")
    bid_value = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bidder} on {self.listing}: {self.bid_value}, bid id:{self.id}"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments_made")
    comment_text = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment made by {self.author} on {self.listing}, comment id:{self.id}"

