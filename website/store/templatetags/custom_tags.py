from django import template
import urllib.request, json
from ..database.getData import getProdImage, getProdName, getProdPublish, getProdPrice, getProdAuthor, getProdStock

register = template.Library()

@register.assignment_tag

def any_function():
    with urllib.request.urlopen('https://gateway.marvel.com/v1/public/comics?ts=1&format=comic&formatType=comic&noVariants=true&orderBy=-title&limit=1&apikey=144ba3e33cfbf7edd53ed87d7b64c23a&hash=2c814cdb9f5c3d39bbf973ec7fcc6c6b') as url:
        data = json.loads(url.read().decode())
        title =  data['data']['results'][0]['title']
        desc = 'description: ' + data['data']['results'][0]['description']
        count = 'pagecount: ', data['data']['results'][0]['pageCount']
        fullurl = str(data['data']['results'][0]['thumbnail']['path']) + '.jpg'
    return "{0}, {1}, {2}, {3}".format(title, desc, count, fullurl)

def getRows(getal):
    return (int(getal / 3))


@register.simple_tag()
def prodImageTag(prodNum):
    return getProdImage(prodNum)

@register.simple_tag()
def prodUrlTag(prodNum):
    url = "/product/" + str(prodNum)
    return url

@register.simple_tag()
def prodTitleTag(prodNum):
    return getProdName(prodNum)

@register.simple_tag()
def prodPublTag(prodNum):
    return getProdPublish(prodNum)

@register.simple_tag()
def prodPriceTag(prodNum):
    return getProdPrice(prodNum)

@register.simple_tag()
def prodAuthorTag(prodNum):
    return getProdAuthor(prodNum)

@register.simple_tag()
def prodStockTag(prodNum):
    return getProdStock(prodNum)

@register.simple_tag()
def listloop():
    cnt = 1
    txt = ""
    for i in range(10):
        txt += "<ul class='list'>"
        for x in range(3):
            txt = txt + "<li><div class='productwrap'><a href='" + prodUrlTag(cnt) + "'><img src='" + prodImageTag(cnt) + "' id='zoom_05' data-zoom-image='https://i.pinimg.com/736x/86/ff/e2/86ffe2b49daf0feed78a1c336753696d--black-panther-comic-digital-comics.jpg'></a><p class='author'>" + prodAuthorTag(cnt) + "</p><p class='name'>" + prodTitleTag(cnt) + "</p><p><i class='fa fa-star' aria-hidden='true'></i><i class='fa fa-star' aria-hidden='true'></i><i class='fa fa-star' aria-hidden='true'></i><i class='fa fa-star' aria-hidden='true'></i><i class='fa fa-star' aria-hidden='true'></i></p><p class='price'>€ " + str(prodPriceTag(cnt)) + "</p><p class='addtocart'><i class='fa fa-plus' aria-hidden='true'></i><i class='fa fa-shopping-cart' aria-hidden='true'></i></p><p class='wishlist'><i class='fa fa-heart' aria-hidden='true'></i></p><p class='stock'>Voorraad: " + str(prodStockTag(cnt)) + "</p></div></li>"
            cnt += 1
        txt += "</ul>"
    return txt
