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

def getResult2(query):
  query = queryVerbeterFunctie(query)
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
# #    WHERE \"prodName\" = 'Fairy Tail - Volume 1'
#   return authorlist, namelist
  rowscounter = counter
  columncounter = counter
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
      txt = txt + "<li><div class='productwrap'><a href='/product/" + str(urllist[cnt]) + "'><img src='" + str(imglist[cnt]) + "' id='zoom_05' data-zoom-image='https://i.pinimg.com/736x/86/ff/e2/86ffe2b49daf0feed78a1c336753696d--black-panther-comic-digital-comics.jpg'></a><p class='author'>" + str(authorlist[cnt]) + "</p><p class='name'>" + str(namelist[cnt]) + "</p><p><i class='fa fa-star' aria-hidden='true'></i><i class='fa fa-star' aria-hidden='true'></i><i class='fa fa-star' aria-hidden='true'></i><i class='fa fa-star' aria-hidden='true'></i><i class='fa fa-star' aria-hidden='true'></i></p><p class='price'>€ " + str(pricelist[cnt]) + "</p><p class='stock'>Voorraad: " + str(stocklist[cnt]) + "</p></div></li>"
      cnt += 1
    txt += "</ul>"
  return txt

def queryVerbeterFunctie(query):
  i = 1
  query = ((query[:1].upper())+(query[1:].lower()))
  while i < len(query):
    if query[i-1:i] == " ":
      query = (query[:i]) + (query[i:i+1].upper()) + (query[i+1:])
    i += 1
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
