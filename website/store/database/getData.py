from ..models import Products, ProductDetails, Address, Customers
import math
from django.db.models import Q

def getProdNum(prNum):
    object = Products.objects.get(prodNum = prNum)
    return object.prodNum

def getProdName(prNum):
    object = Products.objects.get(prodNum = prNum)
    return object.prodName

def getProdPrice(prNum):
    object = Products.objects.get(prodNum = prNum)
    return object.prodPrice

def getProdStock(prNum):
    object = Products.objects.get(prodNum = prNum)
    return object.prodStock

def getProdGenre(prNum):
    object = ProductDetails.objects.get(prodNum = prNum)
    return object.genre

def getProdType(prNum):
    object = ProductDetails.objects.get(prodNum = prNum)
    return object.type

def getProdPublish(prNum):
    object = ProductDetails.objects.get(prodNum = prNum)
    return object.publisher

def getProdTotalPages(prNum):
    object = ProductDetails.objects.get(prodNum = prNum)
    return object.totalPages

def getProdLanguage(prNum):
    object = ProductDetails.objects.get(prodNum = prNum)
    return object.language

def getProdRating(prNum):
    object = ProductDetails.objects.get(prodNum = prNum)
    return object.rating

def getProdAuthor(prNum):
    object = ProductDetails.objects.get(prodNum = prNum)
    return object.author

def getProdDesc(prNum):
    object = ProductDetails.objects.get(prodNum = prNum)
    return object.desc

def getProdImage(prNum):
    object = ProductDetails.objects.get(prodNum = prNum)
    #print(object)
    return object.imageLink

def getSearchResults(query, userAuth, filter=""):
    # filter = request.POST.get('filter')
    selected = ""
    print(filter)
    if filter == "asc":
        filter = "ORDER BY \"prodName\" ASC"
        selected = "asc"
    elif filter == "desc":
        filter = "ORDER BY \"prodName\" DESC"
        selected = "desc"
    elif filter == "priceasc":
        filter = "ORDER BY \"prodPrice\" ASC"
        selected = "priceasc"
    elif filter == "pricedesc":
        filter = "ORDER BY \"prodPrice\" DESC"
        selected = "pricedesc"
    else:
        filter = ""

    #TODO: Hall of Shame Code right here
    #qrytxt = "SELECT * FROM store_products INNER JOIN store_productdetails on store_products.\"prodNum\" = store_productdetails.\"prodNum\" WHERE \"prodName\" like '%%" + query + "%%' " + filter
    #object = ProductDetails.objects.raw("SELECT * FROM store_products INNER JOIN store_productdetails on store_products.\"prodNum\" = store_productdetails.\"prodNum\" WHERE \"prodName\" like '%%" + query + "%%' " + filter)

    resultsProductName = Products.objects.filter(prodName__icontains=query).order_by("prodPrice")
    results = ProductDetails.objects.filter(Q(genre__icontains=query) | Q(type__icontains=query) | Q(publisher__icontains=query) | Q(language__icontains=query) | Q(author__icontains=query) | Q(desc__icontains=query) | Q(pubDatum__icontains=query) | Q(prodNum__in=resultsProductName))

    txt = """<div class='sorton commoncolor' style='border-radius: 3px'>
         <p>Totale Resultaten: </p>
         <p id='fifteen'>{0}</p>
         <p></p>
         <select name='filter' onchange='this.form.submit()'>""".format(str(len(list(results))))

    if selected == "asc":
        txt += "<option>Relevantie</option><option value='asc' selected>Naam: A - Z</option><option value='desc'>Naam: Z - A</option><option value='priceasc' name='filterasc'>Prijs: Oplopend</option><option value='pricedesc' name='filterdesc'>Prijs: Aflopend</option>"
    elif selected == "desc":
        txt += "<option>Relevantie</option><option value='asc' name='filterasc'>Naam: A - Z</option><option value='desc' name='filterdesc' selected>Naam: Z - A</option><option value='priceasc' name='filterasc'>Prijs: Oplopend</option><option value='pricedesc' name='filterdesc'>Prijs: Aflopend</option>"
    elif selected == "priceasc":
        txt += "<option>Relevantie</option><option value='asc'>Naam: A - Z</option><option value='desc'>Naam: Z - A</option><option value='priceasc' name='filterasc' selected>Prijs: Oplopend</option><option value='pricedesc' name='filterdesc'>Prijs: Aflopend</option>"
    elif selected == "pricedesc":
        txt += "<option>Relevantie</option><option value='asc'>Naam: A - Z</option><option value='desc'>Naam: Z - A</option><option value='priceasc' name='filterasc'>Prijs: Oplopend</option><option value='pricedesc' name='filterdesc' selected>Prijs: Aflopend</option>"
    else:
        txt += "<option selected>Relevantie</option><option value='asc'>Naam: A - Z</option><option value='desc'>Naam: Z - A</option><option value='priceasc' name='filterasc'>Prijs: Oplopend</option><option value='pricedesc' name='filterdesc'>Prijs: Aflopend</option>"
    txt += """</select>
	 <p id='sortp'>Sorteren op: </p>
	 </div>"""

    counter = 0
    for e in results:
        if counter == 0:
            txt += "<ul class='list'>"
        txt = txt + "<li><div class='productwrap'><a href='/product/" + str(e.prodNum.prodNum) + "'><img src='" + e.imageLink + "' id='zoom_05' data-zoom-image='https://i.pinimg.com/736x/86/ff/e2/86ffe2b49daf0feed78a1c336753696d--black-panther-comic-digital-comics.jpg'></a><p class='author'>" + e.author + "</p><p class='name'>" + getProdName(e.prodNum.prodNum) + "</p><p><i class='fa fa-star' aria-hidden='true'></i><i class='fa fa-star' aria-hidden='true'></i><i class='fa fa-star' aria-hidden='true'></i><i class='fa fa-star' aria-hidden='true'></i><i class='fa fa-star' aria-hidden='true'></i></p><p class='price'>€ " + str(e.prodNum.prodPrice) + "</p><button name='addToCartItemBoxButton' value='" + str(e.prodNum.prodNum) + "'class='addtocart'><i class='fa fa-plus' aria-hidden='true'></i><i class='fa fa-shopping-cart' aria-hidden='true'></i></button>"
        if userAuth:
            txt = txt + "<button name='moveToWishListButton' value='" + str(e.prodNum.prodNum) + "' class='wishlist'><i class='fa fa-heart' aria-hidden='true'></i></button>"
        txt = txt + "<p class='stock'>Voorraad: " + str(e.prodNum.prodStock) + "</p></div></li>"
        if counter == 2:
            txt += "</ul>"
            counter = 0
        else:
            counter = counter + 1
    return txt

def queryVerbeterFunctie(query):
  try:
    query = removeUnwanted(query)
    i = 1
    query = ((query[:1].upper())+(query[1:].lower()))
    query = (query.translate("!@#$%^~`&*()_+=-{[]}\|\"\';:?/>.<,"))
    while i <= len(query):
      # Remove unwanted characters.
      if 33 <= ord(query[i-1:i]) <= 47:
        query = queryVerbeterFunctie(query[:i-1] + query[i:])
        print("Removed")
      if 58 <= ord(query[i-1:i]) <= 64:
        query = queryVerbeterFunctie(query[:i-1] + query[i:])
        print("Removed")
      if 91 <= ord(query[i-1:i]) <= 96:
        query = queryVerbeterFunctie(query[:i-1] + query[i:])
        print("Removed")
      if 122 <= ord(query[i-1:i]):
        query = queryVerbeterFunctie(query[:i-1] + query[i:])
        print("Removed")
      ## If first char is a space, remove it.
      if query[0].isspace():
        if query.__len__() > 0:
          query = queryVerbeterFunctie(query[1:])
        else:
          query = "Empty Query"
      ## Replace spider-man with Spiderman
      if query[i-1:i+6].lower() == "spiderman":
          query = "Spider-man"
      ## Replace ironman with Iron Man
      if query[i-1:i+6].lower() == "ironman":
        query = "Iron Man"
      ## Replace captainamerica with Captain America
      if query[i-1:i+13].lower() == "captainamerica":
        query = "Captain America"
      else:
        if query[i-1:i+2].lower() == "cpt":
          query = "Captain"
      ## Replace next letter with an uppercase after a space is found
      if query[i-1:i] == " ":
        query = (query[:i]) + (query[i:i+1].upper()) + (query[i+1:])
      ## Removes "the" from the query, since most comics don't use it anymore
      if query[i-1:i+2].lower() == "the" and i < len(query) - 2 and not query[i-1:i+3].lower() == "they":
        if i == 1:
          query = (query[i+2:])
          ## Make the function recursive because some parts won't work otherwise :')
          query = query[:i] + query[i+2:]
          i = 0;
      ## If search starts with "the", remove it completely
        else:
          query = (query[:i]) + (query[i+2:])
      i += 1

    print(query)
    return query
  except :
    print("Stop Jasper.")
    return query

def removeUnwanted(query):
  # Resolves empty query errors
  if query == "" or len(query) == 0:
    query = "No query found"
  return query
 
def getPublisherBox(publisherQuery):
  object = ProductDetails.objects.get(publisher = publisherQuery)
  return object.prodNum

def getRatingBox(ratingQuery):
  object = ProductDetails.objects.get(rating = ratingQuery)
  return object.prodNum

def getTypeBox(typeQuery):
  object = ProductDetails.objects.get(type = typeQuery)
  return object.prodNum

def getLanguageBox(languageQuery):
  object = ProductDetails.objects.get(language = languageQuery)
  return object.prodNum

def getPriceBox(priceMin, priceMax):
  object = ProductDetails.objects.raw('SELECT * FROM ProductDetails'
                                      'WHERE prodPrice >= ' + priceMin +
                                      'AND prodPrice <= ' + priceMax)
  return object.prodNum

def getProdData(prNum):
  object = ProductDetails.objects.get(prodNum = prNum)
  return object.pubDatum[0:10]

def getCustomer(id):
    object = Customers.objects.get(customerID=id)
    return object

def getCustomerFName(id):
    customer = getCustomer(id)
    object = customer.name
    return object

def getCustomerLName(id):
    customer = getCustomer(id)
    object = customer.surname
    return object

def getCustomerPhone(id):
    customer = getCustomer(id)
    object = customer.telephone
    return object

def getCustomerAddress(id):
    object = Address.objects.get(customerID=Customers(customerID=id))
    return object

def getStreet(id):
    address = getCustomerAddress(id)
    object = address.address
    return object

def getHouseNumber(id):
    address = getCustomerAddress(id)
    object = address.number
    return object

def getCity(id):
    address = getCustomerAddress(id)
    object = address.city
    return object

def getPostalcode(id):
    address = getCustomerAddress(id)
    object = address.postalcode
    return object
