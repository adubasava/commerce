from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Now


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.name}"
       

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.FloatField(default=0)
    image_url = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="seller")
    active = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")
    time = models.DateTimeField(db_default=Now())

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):    
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="buyer")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="item")
    bid = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.bid} on {self.item} from {self.user}"
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="author")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listing")
    text = models.TextField()
    time = models.DateTimeField(db_default=Now())

    def __str__(self):
        return f"by {self.user} on {self.listing}"
