from django.shortcuts import redirect, render

from ..database.getData import queryVerbeterFunctie

def searchPost(request):
    return redirect("/search/" + queryVerbeterFunctie(str(request.POST.get('searchtext'))))
