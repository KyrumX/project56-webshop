from django import template
from ..models import Products, ProductDetails
import urllib.request, json
from ..database.getData import getProdImage, getProdName, getProdPublish, getProdPrice, getProdAuthor, getProdStock
from ..database.getData import getProdName, getProdNum, getProdPrice, getProdStock, getProdGenre, getProdType, getProdAuthor, getProdDesc, getProdImage, getProdLanguage, getProdPublish, getProdRating, getProdTotalPages, getProdData
from ..database.verifyData import verifyProdNum
from ..database.getData import getSearchResults
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
def prodName(prodNum):
    return getProdName(prodNum)

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
def listloop(userAuth):
    cnt = 1
    txt = ""
    for i in range(4):
        txt += "<ul class='list'>"
        for x in range(3):
            txt = txt + "<li><div class='productwrap'><a href='" + prodUrlTag(cnt) + "'><img src='" + prodImageTag(cnt) + "' id='zoom_05' data-zoom-image='https://i.pinimg.com/736x/86/ff/e2/86ffe2b49daf0feed78a1c336753696d--black-panther-comic-digital-comics.jpg'></a><p class='author'>" + prodAuthorTag(cnt) + "</p><p class='name'>" + prodTitleTag(cnt) + "</p><p><i class='fa fa-star' aria-hidden='true'></i><i class='fa fa-star' aria-hidden='true'></i><i class='fa fa-star' aria-hidden='true'></i><i class='fa fa-star' aria-hidden='true'></i><i class='fa fa-star' aria-hidden='true'></i></p><p class='price'>€ " + str(prodPriceTag(cnt)) + "</p>" \
                       "<button name='addToCartItemBoxButton' value='" + str(cnt) + "'class='addtocart'><i class='fa fa-plus' aria-hidden='true'></i><i class='fa fa-shopping-cart' aria-hidden='true'></i></button>"
            if userAuth:
                txt = txt + "<button name='moveToWishListButton' value='" + str(cnt) +"' class='wishlist'><i class='fa fa-heart' aria-hidden='true'></i></button>"
            txt = txt + "<p class='stock'>Voorraad: " + str(prodStockTag(cnt)) + "</p></div></li>"
            cnt += 1
        txt += "</ul>"
    return txt

@register.simple_tag()
def searchList(query, userAuth, filter=""):
    object = getSearchResults(str(query), userAuth, filter)
    return object

@register.simple_tag()
def suggesteditems(prod, type):
    object = ProductDetails.objects.raw("SELECT * FROM store_products INNER JOIN store_productdetails on store_products.\"prodNum\" = store_productdetails.\"prodNum\" WHERE \"prodName\" like '%%" + prod.split()[0].replace("'", "''") + "%%' EXCEPT SELECT * FROM store_products INNER JOIN store_productdetails on store_products.\"prodNum\" = store_productdetails.\"prodNum\" WHERE \"prodName\" = '" + prod.replace("'", "''") + "' LIMIT 3")

    txt = ""
    imgarr = []
    titlearr = []
    pricearr = []
    linkarr = []

    for i in object:
        imgarr.append(i.imageLink)
        titlearr.append(i.prodName)
        pricearr.append(i.prodPrice)
        linkarr.append(i.prodNum)

    cnt = 0

    if type == 'Manga':
        object = ProductDetails.objects.raw("SELECT * FROM store_products INNER JOIN store_productdetails on store_products.\"prodNum\" = store_productdetails.\"prodNum\" WHERE NOT \"prodName\" = '" + prod.replace("'", "''") + "' AND \"type\" = 'Manga' ORDER BY RANDOM() LIMIT 3")

        imgarr = []
        titlearr = []
        pricearr = []
        linkarr = []

        for i in object:
            imgarr.append(i.imageLink)
            titlearr.append(i.prodName)
            pricearr.append(i.prodPrice)
            linkarr.append(i.prodNum)
    elif len(titlearr) < 3 :
        object = ProductDetails.objects.raw("SELECT * FROM store_products INNER JOIN store_productdetails on store_products.\"prodNum\" = store_productdetails.\"prodNum\" WHERE NOT \"prodName\" = '" + prod.replace("'", "''") + "' ORDER BY RANDOM() LIMIT 3")

        imgarr = []
        titlearr = []
        pricearr = []
        linkarr = []

        for i in object:
            imgarr.append(i.imageLink)
            titlearr.append(i.prodName)
            pricearr.append(i.prodPrice)
            linkarr.append(i.prodNum)

    for i in range(3):
        txt += "<li><div class='suggwrap'><a href='/product/"+ str(linkarr[cnt]) +"'><img src='" + str(imgarr[cnt]) + "'></a><p>" + str(titlearr[cnt]) + "</p><p>€ " + str(pricearr[cnt]) + "</p></div></li>"
        cnt += 1
    return txt

@register.simple_tag()
def getOrder(order):
    html = ""
    for e in order:
        html += "<tr style='text-align: center;' align='center'><td style='text-align: center; border-left-width: 0; border-top-color: #ffffff; border-top-width: 1px; border-top-style: solid; border-bottom-width: 0; border-bottom-style: solid; border-bottom-color: #e0e0e0; border-left-style: solid; border-left-color: #e0e0e0; -moz-border-radius-bottomleft: 3px; -webkit-border-bottom-left-radius: 3px; border-bottom-left-radius: 3px; background-image: -moz-linear-gradient(top,  #fbfbfb,  #fafafa); padding: 18px 18px 18px 20px;' align='center'>{0}</td><td style='text-align: center; border-left-width: 0; border-top-color: #ffffff; border-top-width: 1px; border-top-style: solid; border-bottom-width: 0; border-bottom-style: solid; border-bottom-color: #e0e0e0; border-left-style: solid; border-left-color: #e0e0e0; -moz-border-radius-bottomleft: 3px; -webkit-border-bottom-left-radius: 3px; border-bottom-left-radius: 3px; background-image: -moz-linear-gradient(top,  #fbfbfb,  #fafafa); padding: 18px 18px 18px 20px;' align='center'>{1}</td><td style='border-top-color: #ffffff; border-top-width: 1px; border-top-style: solid; border-bottom-width: 0; border-bottom-style: solid; border-bottom-color: #e0e0e0; border-left-width: 1px; border-left-style: solid; border-left-color: #e0e0e0; -moz-border-radius-bottomright: 3px; -webkit-border-bottom-right-radius: 3px; border-bottom-right-radius: 3px; background-image: -moz-linear-gradient(top,  #fbfbfb,  #fafafa); padding: 18px;'>{2}</td></tr>".format(e.productNum.prodNum, prodName(e.productNum.prodNum), e.amount)
    return html

@register.simple_tag()
def getOrderNum(order):
    string = str(order.first().orderNum.orderNum)
    return string