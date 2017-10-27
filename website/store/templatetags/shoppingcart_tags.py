from django import template
from ..database.CartOps import cartLength
from ..database.getData import getProdImage
from ..models import ShoppingCart

register = template.Library()

@register.simple_tag()
def displayCart(sessionkey, userAuth):
    length = cartLength(sessionkey)
    print(length)
    if length == 0:
        html = "<p class='title'>Momenteel zit er nog niks in je winkelwagentje.</p>"
    else:
        html = "<ul class='cartwrap'>"
        cnt = 0
        for e in ShoppingCart.objects.all().filter(session_key=sessionkey):
            amounttxt = "<select name='amount' id='amountselect" + str(cnt) + "' class='amountselect'>"
            for i in range(1, 12):
                if i == e.amount:
                    amounttxt += "<option selected>" + str(e.amount) + "</option>"
                else:
                    if i == 11:
                        amounttxt += "<option>meer..</option>"
                    else:
                        amounttxt += "<option>" + str(i) + "</option>"
            amounttxt += "</select><input type='text' id='meer" + str(cnt) + "' value='" + str(e.amount) + "' style='display: none;' class='amountinput' />"

            #IMG - NAAM - AANTAL - PRIJS
            html += "<li class='cartitem'><div class='productcartimg'><a href='/product/" + str(e.prodNum) + "'><img src='" + getProdImage(e.prodNum) + "' id='zoom_05' data-zoom-image='https://i.pinimg.com/736x/86/ff/e2/86ffe2b49daf0feed78a1c336753696d--black-panther-comic-digital-comics.jpg'></a></div>"
            if userAuth:
                html += "<div class='textplace'><button name='removeFromCartButton' value='" + str(e.prodNum) +"' class='remove'><i class='fa fa-trash' aria-hidden='true'></i><p>verwijderen</p></button><button name='moveToWishListButton' value='" + str(e.prodNum) +"' class='movetowishlist'><i class='fa fa-heart' aria-hidden='true'></i><p>verplaats naar verlanglijstje</p></button><p class='title'>" + e.prodNum.prodName + "</p>"
            else:
                html += "<div class='textplace'><button name='removeFromCartButton' value='" + str(e.prodNum) + "' class='remove'><i class='fa fa-trash' aria-hidden='true'></i><p>verwijderen</p></button><p class='title'>" + e.prodNum.prodName + "</p>"
            html += "<p>Aantal: " + amounttxt + "</p>"
            html += "<p>Prijs: €" + str(e.amount * e.prodNum.prodPrice) + "</p>"
            html += "</div></li>"
            cnt += 1
        html += "</ul>"

    return html


