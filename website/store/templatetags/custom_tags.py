import json
import urllib.request
from random import randint

from django import template
from django.db.models import Avg

from ..database.getData import getProdName, getProdPrice, getProdStock, getProdAuthor, getProdDesc, getProdImage, \
    getProdPublish, getProdRating
from ..database.getData import getVisitsChart
from ..models import ProductDetails, Reviews
from ..models import UserVisits, Dates, OrderDetails, Orders, Products
from django.db.models import Max

register = template.Library()

@register.simple_tag()

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

def getMaxid():
    maxid = Products.objects.aggregate(Max('prodNum'))
    id = maxid.get('prodNum__max')
    return id

@register.simple_tag()
def topProdNameTag():
    return getProdName(getMaxid())

@register.simple_tag()
def topProdPublTag():
    return getProdPublish(getMaxid())

@register.simple_tag()
def topProdUrlTag():
    url = "/product/" + str(getMaxid())
    return url

@register.simple_tag()
def topProdImageTag():
    return getProdImage(getMaxid())

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

# Text shortener gemaak door Selim :D. Pakt helft van de text en zet daar puntjes achter (bij het eerst volgende spatie teken)

@register.simple_tag()
def textshortener(txt):
    cnt = 0
    list = []
    for i in txt:
        cnt += 1
        if i == " ":
            list.append(cnt - 1)

    lastspace = list[int(len(list) / 2)]

    return txt[:lastspace] + "..."

@register.simple_tag()
def listloop(userAuth):
    cnt = 1
    mod = 1
    txt = ""
    randomlyselectedprod = randint(1, 69)

    prodratingtxt = ""
    for r in range(getProdRating(randomlyselectedprod)):
        prodratingtxt += "<i class='fa fa-star' aria-hidden='true'></i>"

    print("This is the length of the desc: ", len(getProdDesc(randomlyselectedprod)))

    if len(getProdDesc(randomlyselectedprod)) > 550:
        proddesc = textshortener(getProdDesc(randomlyselectedprod))
        txt += """<div class="startwrap" style="border-radius: 3px"><div class="itemoftheday"><div class="itempart1"><p>Uitgelicht Product</p></div><div class="itempart2"><p>{0}</p></div></div>
            <div class="leftstart"><a href="{1}"><img src="{2}"></a></div>
            <div class="rightstart"><h1>{3}</h1><p style="padding-bottom: 50px;">{4}</p><a href="/product/{5}"><p id="leesmeer"><i class="fa fa-angle-double-right" aria-hidden="true"></i>Lees meer</p></a></div></div>""".format(prodratingtxt,  prodUrlTag(randomlyselectedprod), getProdImage(randomlyselectedprod), getProdName(randomlyselectedprod), proddesc, randomlyselectedprod)
    else:
        txt += """<div class="startwrap" style="border-radius: 3px"><div class="itemoftheday"><div class="itempart1"><p>Uitgelichte Product</p></div><div class="itempart2"><p>{0}</p></div></div>
            <div class="leftstart"><a href="{1}"><img src="{2}"></a></div>
            <div class="rightstart"><a href="{3}"><h1>{4}</h1></a><p>{5}</p></div></div>""".format(prodratingtxt,  prodUrlTag(randomlyselectedprod), getProdImage(randomlyselectedprod), prodUrlTag(randomlyselectedprod), getProdName(randomlyselectedprod), getProdDesc(randomlyselectedprod))

    for i in range(4):
        txt += "<ul class='list'>"
        for x in range(3):
            stock = checkstock(True, cnt)
            button = checkstock(False, cnt)

            # txt = txt + "<li><div class='productwrap'><a href='" + prodUrlTag(cnt) + "'><img src='" + prodImageTag(cnt) + "' id='zoom_05' data-zoom-image='https://i.pinimg.com/736x/86/ff/e2/86ffe2b49daf0feed78a1c336753696d--black-panther-comic-digital-comics.jpg'></a><p class='author'>" + prodAuthorTag(cnt) + "</p><p class='name'>" + prodTitleTag(cnt) + "</p><p><i class='fa fa-star' aria-hidden='true'></i><i class='fa fa-star' aria-hidden='true'></i><i class='fa fa-star' aria-hidden='true'></i><i class='fa fa-star' aria-hidden='true'></i><i class='fa fa-star' aria-hidden='true'></i></p><p class='price'>€ " + str(prodPriceTag(cnt)) + "</p>" + button
            # if userAuth:
            #     txt = txt + "<button name='moveToWishListButton' value='" + str(cnt) +"' class='wishlist'><i class='fa fa-heart' aria-hidden='true'></i></button>"
            # txt = txt + stock

            rating = getRating(cnt)
            prodratingtxt = ""
            for r in rating:
                prodratingtxt += "<i class='fa fa-star' aria-hidden='true'></i>"

            txt = txt + "<li><div class='productwrap'><a href='" + prodUrlTag(cnt) + "'><img src='" + prodImageTag(cnt) + "' id='zoom_05'></a><p class='author'>" + prodAuthorTag(cnt) + "</p><p class='name'>" + prodTitleTag(cnt) + "</p><p>{0}</p><p class='price'>€ ".format(prodratingtxt) + str(prodPriceTag(cnt)) + "</p>" + button
            if userAuth:
                txt = txt + "<button name='moveToWishListButton' value='" + str(cnt) +"' class='wishlist'><i class='fa fa-heart' aria-hidden='true'></i></button>"
            txt = txt + stock

            cnt += 10
            if cnt >= 60:
                mod += 1
                cnt = mod

        txt += "</ul>"
    return txt

def checkstock(numbercheck, prodnumber):
    if numbercheck:
        print("in numbercheck")
        if prodStockTag(prodnumber) <= 0:
            print("uitverkocht")
            return "<p class='stock' style='color: #d45f5f;'>Uitverkocht!</p>"
        else:
            print("in stock: ", str(prodStockTag(prodnumber)))
            return "<p class='stock'>Voorraad: " + str(prodStockTag(prodnumber)) + "</p>"
    else:
        if prodStockTag(prodnumber) <= 0:
            return "<button name='addToCartItemBoxButton' id='outofstock' type=button class='addtocart tooltip'><i class='fa fa-ban' aria-hidden='true'></i><span class='tooltiptext'>Dit product is momenteel helaas uitverkocht.</span></button>"
        else:
            return "<button name='addToCartItemBoxButton' value='" + str(prodnumber) + "'class='addtocart'><i class='fa fa-plus' aria-hidden='true'></i><i class='fa fa-shopping-cart' aria-hidden='true'></i></button>"

@register.simple_tag()
def isInStock(prodnumber):
    if prodStockTag(prodnumber) <= 0:
        return False
    return True

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

@register.simple_tag()
def incrementVisit(is_staff, cID=-1):
    all = UserVisits.objects.all().filter(customerID=cID)
    print("cID = ", cID)
    print(all)
    if not all:
        print("none found")
        if is_staff == "false":
            print("Nothing found. Adding to db")
            uservisit = UserVisits(customerID=cID, visits=1, is_staff=False)
            uservisit.save()
        else:
            print("User is Staff. Adding to db")
            uservisit = UserVisits(customerID=cID, visits=1, is_staff=True) 
            uservisit.save()
    else:
        print("Already found. Incrementing...")
        c = UserVisits.objects.all().filter(customerID=cID)

        for e in c:
            #amountvisits = e.visits + 1
            UserVisits.objects.filter(customerID=cID).update(visits = e.visits + 1)
        #UserVisits.objects.filter(customerID=cID).update(visits = visits)
    lel = UserVisits.objects.get(customerID=cID)
    date = Dates(customerID=lel)
    date.save()
    return ""


@register.simple_tag()
def latestReviews(prodnum):
    reviews = Reviews.objects.all().filter(prodNum=prodnum)

    if not reviews.exists():
        print("no existo!")
        return "<p style='text-align:center; padding-top: 1%;'>Er zijn nog geen recensies geschreven voor dit product.</p>"


    html = "<ul class='mainrec'>"
    for i in reviews:
        rating = ""
        for x in range(i.rating):
            num = ""
            num2 = ""
            if i.date.day < 10 and i.date.month < 10:
                num = 0
                num2 = 0
            elif i.date.day < 10:
                num = 0
            elif i.date.month < 10:
                num2 = 0

            dateformat = "{0}{1}-{2}{3}-{4}".format(num, i.date.day, num2, i.date.month, i.date.year)
            print(dateformat)

            rating += "<i class='fa fa-star' aria-hidden='true'></i>"

        print("This is customer ID: ", i.customerID)
        html += "<ul class='rec'><ul class='recen'><li>{0} {1} op {2}</li><li>{3}</li><li>{4}</li></ul></ul>".format(i.customerID.name, i.customerID.surname, dateformat, rating, i.review)
    html += "</ul>"

    return html

@register.simple_tag()
def getRating(prodnum):
    reviews = Reviews.objects.all().filter(prodNum=prodnum)
    rating = ""
    if reviews.exists():
        for i in range(int(reviews.aggregate(Avg('rating'))['rating__avg'])):
            rating += "x"
        return rating
    else:
        for i in range(getProdRating(prodnum)):
            rating += "x"
        return rating
def visitchart():
    return getVisitsChart()

def testingOrder():
    order = OrderDetails.objects.all().filter(orderNum=Orders(orderNum=orderEntry.orderNum))  # Returnt een Array van alle Items die besteld zijn
    for i in order:
        print("Dit is Productnum: ", str(i.productNum))
        print("Dit is Amount", str(i.amount))
    return string
