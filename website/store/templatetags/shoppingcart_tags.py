from django import template
from ..database.CartOps import cartLength
from ..database.getData import getProdImage, getProdStock
from ..models import ShoppingCart
from decimal import Decimal
register = template.Library()

@register.simple_tag()
def displayCartItem(e, userAuth):
    html = "<ul class='cartwrap'>"
    amounttxt = "<select name='amount' id='amountselect' class='amountselect' onchange='this.form.submit()'>"
    for i in range(1, getProdStock(e.prodNum.prodNum) + 1):
        if i == e.amount:
            amounttxt += "<option selected>" + str(e.amount) + "</option>"
        else:
            amounttxt += "<option>" + str(i) + "</option>"
    amounttxt += "</select><input type='text' id='meer' value='" + str(e.amount) + "' style='display: none;' class='amountinput' />"

        # IMG - NAAM - AANTAL - PRIJS
    html += "<li class='cartitem'><div class='productcartimg'><a href='/product/" + str(e.prodNum) + "'><img src='" + getProdImage(e.prodNum) + "' id='zoom_05' data-zoom-image='https://i.pinimg.com/736x/86/ff/e2/86ffe2b49daf0feed78a1c336753696d--black-panther-comic-digital-comics.jpg'></a></div>"
    if userAuth:
        html += "<div class='textplace'><button name='removeFromCartButton' value='" + str(e.prodNum) + "' class='remove'><i class='fa fa-trash' aria-hidden='true'></i><p>verwijderen</p></button><button name='moveToWishListButton' value='" + str(e.prodNum) + "' class='movetowishlist'><i class='fa fa-heart' aria-hidden='true'></i><p>Voeg toe aan verlanglijstje</p></button><p class='title'>" + e.prodNum.prodName + "</p>"
    else:
        html += "<div class='textplace'><button name='removeFromCartButton' value='" + str(e.prodNum) + "' class='remove'><i class='fa fa-trash' aria-hidden='true'></i><p>Verwijderen</p></button><p class='title'>" + e.prodNum.prodName + "</p>"
    html += "<p>Aantal: " + amounttxt + "</p>"
    html += "<p>Prijs: €" + str(e.amount * e.prodNum.prodPrice) + "</p>"
    html += "</div></li>"
    html += "</ul>"
    return html

@register.simple_tag()
def getItemClass():
    return ItemClass()

@register.simple_tag()
def incItemClass(item):
    item.increment()

@register.simple_tag()
class ItemClass:
    def __init__(self):
        self.total = 0
    def increment(self):
        self.total += 1
    def total(self):
        return self.total

@register.simple_tag()
def cartEmpty(sessionkey):
    if cartLength(sessionkey) == 0:
        return True
    else:
        return False

@register.simple_tag()
def cartItems(sessionkey):
    return ShoppingCart.objects.all().filter(session_key=sessionkey)

@register.simple_tag()
def getTotal(cartobjects):
    topay = 0
    products = 0
    for e in cartobjects:
        topay += e.amount * e.prodNum.prodPrice
        products += e.amount

    if topay >= 100:
        verzendkosten = "<p style='color: #4d884d;'>Gratis</p>"
        grandtotal = topay
    else:
        verzendkosten = "<p>€ 3.50</p>"
        grandtotal = Decimal(float(topay) + 3.50)
        grandtotal = round(grandtotal, 2)

    text = """<div class='totalsum'>
                 <div class='korting'><p>Vul hier uw kortingscode in</p></div>
                 <div class='pricesum'>
                     <table style='border-bottom: solid 1px rgba(0, 0, 0, 0.26);'>
                         <tbody>
                         <tr><td><p>Totaal producten<span style='font-size: 8px'>({0})</span>:</p></td><td style='text-align: right; font-weight: 700;'><p>€ {1}</p></td></tr>
                         <tr><td><p>Verzendkosten:</p></td><td style='text-align: right; font-weight: 700;'>{2}</td></tr>
                         </tbody>
                     </table>
                     <table>
                     <tbody>
                     <tr>
                     <td style='font-weight: 700;'><p>Totaal</p></td>
                     <td style='font-weight: 700;'><p style='text-align: right; color: #534b4a;'>€ {3}</p></td>
                     </tr>
                     </tbody>
                     </table>
                 </div>
    </div>""".format(products, topay, verzendkosten, str(grandtotal))
    return text