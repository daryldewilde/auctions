from django.contrib import admin
from .models import *
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email")

class BidAdmin(admin.ModelAdmin):
    list_display = ("auction", "user", "bid")
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ("auction", "user")
    
class AuctionListAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "category", "start_bid")
    
class WinnerAdmin(admin.ModelAdmin):
    list_display = ("user", "auction")
    
class WatchListAdmin(admin.ModelAdmin):
    list_display = ("auction", "user")
    
admin.site.register(User, UserAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(AuctionList, AuctionListAdmin)
admin.site.register(Winner, WinnerAdmin)
admin.site.register(WatchList, WatchListAdmin)