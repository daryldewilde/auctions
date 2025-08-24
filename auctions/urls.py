from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing_<int:id>_<str:us>", views.listing, name="listing"),
    path("close_<int:id>", views.close, name="close"),
    path("comment_<str:user>_<str:auction>", views.comment, name="comment"),
    path("watchlist<str:user>", views.watchlist, name="watchlist"),
    path("add_to_watchlist_<str:user>_<str:auct>", views.add, name="add_to_watchlist"),
    path("remove_from_watchlist_<str:user>_<str:auct>", views.remove, name="remove_from_watchlist"),
    path("category", views.cat, name="categories"),
    path("cat_<str:cat>", views.speccat, name="cat")
    

]
