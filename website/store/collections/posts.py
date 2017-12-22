from django.shortcuts import redirect, render

from store.database.WishListOps import addToWishList
from ..database.getData import queryVerbeterFunctie

def searchPost(request):
    filter = request.POST.get('filter')
    if 'language' in request.POST:
        sidefilter = request.POST.get('language')
    elif 'type' in request.POST:
        sidefilter = request.POST.get('type')
    elif 'publisher' in request.POST:
        sidefilter = request.POST.get('publisher')
    elif 'price' in request.POST:
        sidefilter = request.POST.get('price')		
    elif 'score' in request.POST:
        sidefilter = request.POST.get('score')
    elif 'sidefilt' in request.POST:
        sidefilter = request.POST.get('sidefilt')
    else:
        print("Found nothing in searchPost")
        sidefilter = ""
	
    print("This is the sidefilter: ", str(sidefilter))
    if filter != None and sidefilter != None:
        print("llululullululullulululululllu")
        print(sidefilter)
        return redirect("/search/" + queryVerbeterFunctie(str(request.POST.get('searchtext'))) + "/" + filter + "/" + sidefilter)
    elif filter != None and sidefilter == None:
        return redirect("/search/" + queryVerbeterFunctie(str(request.POST.get('searchtext'))) + "/" + filter + "items" + "/items")
    elif sidefilter != None and filter == None:
        return redirect("/search/" + queryVerbeterFunctie(str(request.POST.get('searchtext'))) + "/items/" + sidefilter)
    else:
        return redirect("/search/" + queryVerbeterFunctie(str(request.POST.get('searchtext'))) + "/items" + "/items")

def addToWishListPost(request):
    addToWishList(request, int(request.POST.get('moveToWishListButton')))
    return redirect('/verlanglijst/')