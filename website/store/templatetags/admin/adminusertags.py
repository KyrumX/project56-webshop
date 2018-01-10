from django import template
from django.db.models import QuerySet
from ...collections.tools import *
from django.contrib.auth.models import User
from ...database.adminGetData import *
from django.shortcuts import *
from ...collections.tools import TransBool

register = template.Library()

@register.simple_tag()
def userFound(query):
    #Deze functie checkt simpelweg of er wel een user is die overeenkomt met de ID of Naam
    return ifUserExists(query)

@register.simple_tag()
def productFound(query):
    #Deze functie checkt simpelweg of er wel een user is die overeenkomt met de ID of Naam
    return ifProductExists(query)

@register.simple_tag()
def getUserRole(userid):
    userid = int(userid)
    if User.objects.get(id=userid).is_superuser == True:
        return "Sysop"
    else:
        return "Medewerker"

@register.simple_tag()
def displayUsers(query):
    #Deze functie convert alle gevonden users naar items in een table
    users = getUsers(query)
    value = query
    if value != "":
        value = 'value = "{}"'.format(query)
    else:
        value = 'placeholder = "Clark Kent"'

    searchhtml = """<form method="GET">
				<div class="searchplace">
					<input type="text" name="query" pattern="[a-zA-Z0-9@.\s]+" title="Gebruikers ID, e-mail of naam" {0}>
					<button><p><i class="fa fa-search" aria-hidden="true"></i>Zoeken</p></button>
					</div>
				</form>""".format(value)
    rowcount = 0
    if users == None:
        return searchhtml
    resulthtml = "<div class='table1'><table><tr><th>ID</th><th>Naam</th><th>Achternaam</th><th>E-mail</th><th>Geregistreerd</th><th style='text-align: center;'>Geblokkeerd</th><th style='text-align: center;'>Edit</th></tr>"
    counthtml = ""
    for e in users:
        rowcount += 1
        isRegistered = TransBool(e.isRegistered)
        resulthtml += "<tr><td>" + str(e.customerID) + "</td><td>" + e.name + "</td><td>" + e.surname + "</td><td>" + e.email + "</td><td>" + isRegistered + "</td>"
        if e.isRegistered:
            isBlocked = TransBool(e.isBlocked)
            resulthtml += "<td>" + isBlocked + "</td><td><form action='/admin/edit/user/" + str(e.customerID) +"'><button type='submit' value='Bewerken'/>Bewerken</button></form></td></tr>"
        else:
            resulthtml += "<td>n.v.t.</td><td>n.v.t.</td>"
    resulthtml += "</table></div>"
    if query != "":
        counthtml += "<div class='aantal'><p>Aantal zoekresultaten voor '{0}': {1}</p></div>".format(query, str(rowcount))
    else:
        counthtml = "<div class='aantal'><p>Totaal aantal zoekresultaten: {}</p></div>".format(str(rowcount))
    html = searchhtml + counthtml + resulthtml
    return html

@register.simple_tag()
def displayProducts(query):
    #Deze functie convert alle gevonden users naar items in een table

    products = getProducts(query)
    value = query
    if value != "":
        value = 'value = "{}"'.format(query)
    else:
        value = 'placeholder = "Hulk"'

    searchhtml = """<form method="GET">
				<div class="searchplace">
					<input type="text" name="query" pattern="[a-zA-Z0-9@.\s]+" title="Gebruikers ID, e-mail of naam" {0}>
					<button><p><i class="fa fa-search" aria-hidden="true"></i>Zoeken</p></button>
					</div>
				</form>""".format(value)
    rowcount = 0
    if products == None:
        return searchhtml
    resulthtml = "<div class='table1'><table><tr><th>ID</th><th>Naam</th><th>Prijs</th><th style='text-align: center;'>Edit</th></tr>"
    counthtml = ""
    for e in products:
        rowcount += 1
        resulthtml += "<tr><td>" + str(e.prodNum) + "</td><td>" + e.prodName + "</td><td>" + str(e.prodPrice) + "</td>" \
            "<td><form action='/admin/edit/product/" + str(e.prodNum) +"'><button type='submit' value='Bewerken'/>Bewerken</button></form></td></tr>"
    resulthtml += "</table></div>"
    if query != "":
        counthtml += "<div class='aantal'><p>Aantal zoekresultaten voor '{0}': {1}</p></div>".format(query, str(rowcount))
    else:
        counthtml = "<div class='aantal'><p>Totaal aantal zoekresultaten: {}</p></div>".format(str(rowcount))
    html = searchhtml + counthtml + resulthtml
    return html

@register.simple_tag()
def redirectTo(destination):
    redirect(destination)

@register.simple_tag()
def isSameUser(request, id):
    if request.user.id == int(id):
        return True
    return False

@register.simple_tag()
def isSameProduct(request, id):
    if request.user.id == int(id):
        return True
    return False

@register.simple_tag()
def getMonth(month):
    if month == 1:
        return "januari"
    elif month == 2:
        return "februari"
    elif month == 3:
        return "maart"
    elif month == 4:
        return "april"
    elif month == 5:
        return "mei"
    elif month == 6:
        return "juni"
    elif month == 7:
        return "juli"
    elif month == 8:
        return "augustus"
    elif month == 9:
        return "september"
    elif month == 10:
        return "oktober"
    elif month == 11:
        return "november"
    else:
        return "december"
