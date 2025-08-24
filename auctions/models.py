from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class User(AbstractUser):
    pass

class AuctionList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction" )
    name = models.CharField(max_length=50)
    category = models.CharField( max_length=50)
    description = models.CharField(max_length=250)
    start_bid = models.IntegerField()
    actual_bid = models.IntegerField(null=True)
    image = models.ImageField(upload_to='auctions/static/auctions/images')
    image_name = models.CharField(max_length=50)
    active = models.CharField(default='T', max_length=1)
    date_created = models.DateTimeField(default = datetime.now)
    
    def __str__(self):
        return f"{self.name}"
    
class Bid(models.Model):
    auction = models.ForeignKey(AuctionList, on_delete=models.CASCADE, related_name="bid")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bid') 
    bid = models.IntegerField()
    date_created = models.DateTimeField(default = datetime.now)
    
    def __str__(self):
        return f"{self.user} placed {self.bid} on {self.auction}"
    
class Comment(models.Model):
    auction = models.ForeignKey(AuctionList, on_delete=models.CASCADE, related_name="comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    comment = models.CharField(max_length=50)
    date_created = models.DateTimeField(default = datetime.now)
    
    def __str__(self):
        return f"{self.auction} was commented by {self.user}"

class Winner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wins")
    auction = models.ForeignKey(AuctionList, on_delete=models.CASCADE, related_name="wins")
    
    def __str__(self):
        return f"{self.user} won the {self.auction} auction"

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    auction = models.ForeignKey(AuctionList, on_delete=models.CASCADE, related_name="watchlist")
    
    def __str__(self):
        return f"{self.user} is watching {self.auction}"