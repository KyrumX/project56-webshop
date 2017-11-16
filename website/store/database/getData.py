from ..models import Products, ProductDetails
import math

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


def getResult(query):
  object = ProductDetails.objects.raw("SELECT DISTINCT * FROM store_productdetails d, store_products p " +
                                        "WHERE d.\"prodNum\" = p.\"prodNum\" AND " +
                                        "(" +
                                        " prodName LIKE '%" + query + "%'" +
                                        " OR d.genre LIKE '%" + query + "%'" +
                                        " OR d.type LIKE '%" + query + "%'" +
                                        " OR d.publisher LIKE '%" + query + "%'" +
                                        " OR d.language LIKE '%" + query + "%'" +
                                        " OR d.author LIKE '%" + query + "%'" +
                                        " OR p.\"desc\" LIKE '%" + query + "%')" +
                                        " ORDER BY d.\"prodNum\";" +
                                        " LIMIT 1")
  return object

def getSearchResults(query, userAuth):
    query = queryVerbeterFunctie(query)

def getSearchResultsOud(query, userAuth):
    object = ProductDetails.objects.raw("SELECT * FROM store_products INNER JOIN store_productdetails on store_products.\"prodNum\" = store_productdetails.\"prodNum\" WHERE \"prodName\" like '%%" + query + "%%'")
    counter = len(list(object))

  # txt = "" + str(counter)
  # cnt = 0
    authorlist = []
    namelist = []
    urllist = []
    imglist = []
    pricelist = []
    stocklist = []

    for i in object:
        authorlist.append(i.author)
        namelist.append(i.prodName)
        urllist.append(i.prodNum)
        imglist.append(i.imageLink)
        pricelist.append(i.prodPrice)
        stocklist.append(i.prodStock)
    cnt = 0
    txt = ""
    if counter < 4:
        rowscounter = 1
        columncounter = counter
    else:
        if counter % 3 != 0:
            rowscounter = math.ceil(counter / 3)
        else:
            rowscounter = int(counter / 3)
        columncounter = 3

    for i in range(rowscounter):
        txt += "<ul class='list'>"
        if counter % 3 != 0 and i == (rowscounter - 1):
            columncounter = counter % 3
        for x in range(columncounter):
            txt = txt + "<li><div class='productwrap'><a href='/product/" + str(urllist[cnt]) + "'><img src='" + str(imglist[cnt]) + "' id='zoom_05' data-zoom-image='https://i.pinimg.com/736x/86/ff/e2/86ffe2b49daf0feed78a1c336753696d--black-panther-comic-digital-comics.jpg'></a><p class='author'>" + str(authorlist[cnt]) + "</p><p class='name'>" + str(namelist[cnt]) + "</p><p><i class='fa fa-star' aria-hidden='true'></i><i class='fa fa-star' aria-hidden='true'></i><i class='fa fa-star' aria-hidden='true'></i><i class='fa fa-star' aria-hidden='true'></i><i class='fa fa-star' aria-hidden='true'></i></p><p class='price'>€ " + str(pricelist[cnt]) + "</p><button name='addToCartItemBoxButton' value='" + str(urllist[cnt]) + "'class='addtocart'><i class='fa fa-plus' aria-hidden='true'></i><i class='fa fa-shopping-cart' aria-hidden='true'></i></button>"
            if userAuth:
                txt = txt + "<button name='moveToWishListItemBoxButton' value='" + str(urllist[cnt]) +"' class='wishlist'><i class='fa fa-heart' aria-hidden='true'></i></button>"
            txt = txt + "<p class='stock'>Voorraad: " + str(stocklist[cnt]) + "</p></div></li>"
            cnt += 1
        txt += "</ul>"
    return txt

def queryVerbeterFunctie(query):
  if len(query) == 0:
        query = "No query found."
  i = 1
  query = ((query[:1].upper())+(query[1:].lower()))
  while i <= len(query):
    ## If first char is a space, remove it.
    while (query[0]) == " ":
      query = query[1:]
      if query[1] != " ":
        query = query[0].upper() + query[1:]
    ## Removes "the" from the query, since most comics don't use it anymore
    if query[i-1:i+2].lower() == "the" and i < len(query) - 2:
      if i == 1:
        query = (query[i+2:])
        ## Make the function recursive because some parts won't work otherwise :')
        query = queryVerbeterFunctie(query)
        break
    ## If search starts with "the", remove it completely
      else:
        query = (query[:i]) + (query[i+2:])
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
    ## Removes UNICODE except 32, 48-57, 65-90, 97-122, 192-214, 216-246, 248-328, 330-447
    ## bdfhjlnprtvxz
    while 0 <= ord(query[i-1:i]) <= 31 or 33 <= ord(query[i-1:i]) <= 47 or 58 <= ord(query[i-1:i]) <= 64 or 91 <= ord(query[i-1:i]) <= 96 or 123 <= ord(query[i-1:i]) <= 191 or 215 == ord(query[i-1:i]) or 247 == ord(query[i-1:i]) or 329 == ord(query[i-1:i]) or 448 <= ord(query[i-1:i]):
      if ord((query[i-1:i])) != 32 or not(48 <= ord((query[i-1:i])) <= 57 or 65 <= ord((query[i-1:i])) <= 90 or 97 <= ord((query[i-1:i])) <= 122 or 192 <= ord((query[i-1:i])) <= 214 or 216 <= ord((query[i-1:i])) <= 246 or 248 <= ord((query[i-1:i])) <= 328 or 330 <= 447):
        print("origineel " + query)
        query = query[:i-1] + query[i:]
        print(query)
        ## for code in bytearray(mystr, 'ascii'):
    ## if query[i-1:i] != zooi doe andere zooi)
    i += 1
  # j = 0
  # while j < 26:
  #   print(chr(j + 97))
  #   j += 1
  print(query)
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
