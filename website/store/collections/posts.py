from django.shortcuts import redirect, render

from store.database.WishListOps import addToWishList
from ..database.getData import queryVerbeterFunctie

def searchPost(request):
    return redirect("/search/" + queryVerbeterFunctie(str(request.POST.get('searchtext'))))

def addToWishListPost(request):
    addToWishList(request, int(request.POST.get('moveToWishListButton')))
    return redirect('/verlanglijst/')