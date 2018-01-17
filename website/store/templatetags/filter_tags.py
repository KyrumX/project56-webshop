from django import template

from store.collections.filter import isCategoryRelevant

register = template.Library()

@register.simple_tag()
def languageFilter(relevantItems, selectedFilters):
    html = ""
    if relevantItems != None:
        html +=  "<div class='barwrap'>" \
                 "<div class='leftbar commoncolor'>" \
                 "<p>Taal<i class='fa fa-sort-desc' aria-hidden='true' id='sortdown'></i></p></div>" \
                 "<div class='bartext'><div class='insidebar'>"
        for e in relevantItems:
            if e == 'Engels':
                if 'English' in selectedFilters:
                    html += "<input type='checkbox' onchange='combineForms()' name='language' value='English' id='english' checked>"
                else:
                    html += "<input type='checkbox' onchange='combineForms()' name='language' value='English' id='english'>"
                html += "<label for='english'></label><p>Engels</p><br>"
            elif e == 'Nederlands':
                if 'Dutch' in selectedFilters:
                    html += "<input type='checkbox' onchange='combineForms()' name='language' value='Dutch' id='dutch' checked>"
                else:
                    html += "<input type='checkbox' onchange='combineForms()' name='language' value='Dutch' id='dutch'>"
                html += "<label for='dutch'></label><p>Nederlands</p><br>"
        html += "</div></div></div>"
        return html
    return ""

@register.simple_tag()
def typeFilter(relevantItems, selectedFilters):
    html = ""
    if relevantItems != None:
        html += "<div class='barwrap'><div class='leftbar commoncolor'>" \
                "<p>Type Boek<i class='fa fa-sort-desc' aria-hidden='true' id='sortdown'></i></p>" \
                "</div>" \
                "<div class='bartext'><div class='insidebar'>"
        for e in relevantItems:
            if e == 'Manga':
                if 'manga' in selectedFilters:
                    html += "<input type='checkbox' onchange='combineForms()' name='type' value='manga' id='manga' checked>"
                else:
                    html += "<input type='checkbox' onchange='combineForms()' name='type' value='manga' id='manga'>"
                html += "<label for='manga'></label><p>Manga</p><br>"
            elif e == 'Comic':
                if 'comic' in selectedFilters:
                    html += "<input type='checkbox' onchange='combineForms()' name='type' value='comic' id='comic' checked>"
                else:
                    html += "<input type='checkbox' onchange='combineForms()' name='type' value='comic' id='comic'>"
                html += "<label for='comic'></label><p>Comic</p><br>"
        html += "</div></div></div>"
        return html
    return ""

@register.simple_tag()
def publisherFilter(relevantItems, selectedFilters):
    html = ""
    if relevantItems != None:
        html += "<div class='barwrap'><div class='leftbar commoncolor'>" \
                "<p>Uitgever<i class='fa fa-sort-desc' aria-hidden='true' id='sortdown'></i></p>" \
                "</div>" \
                "<div class='bartext'><div class='insidebar'>"
        for e in relevantItems:
            if e in selectedFilters:
                html += "<input type='checkbox' onchange='combineForms()' value='" + e + "' name='publisher' id='" + e +"' checked>"
            else:
                html += "<input type='checkbox' onchange='combineForms()' value='" + e + "' name='publisher' id='" + e +"'>"
            html += "<label for='" + e + "'></label><p>"+ e +"</p><br>"
        html += "</div></div></div>"
        return html
    return ""

@register.simple_tag()
def orderbyForm(order, size):
    txt = """<div class='sorton commoncolor' style='border-radius: 3px'>
         <p>Totale Resultaten: </p>
         <p id='fifteen'>{0}</p>
         <p></p>
         <select name='orderby' onchange='combineForms()'>""".format(str(size))

    if order == "asc":
        txt += "<option>Relevantie</option><option value='asc' selected>Naam: A - Z</option><option value='desc'>Naam: Z - A</option><option value='priceasc' name='filterasc'>Prijs: Oplopend</option><option value='pricedesc' name='filterdesc'>Prijs: Aflopend</option>"
    elif order == "desc":
        txt += "<option>Relevantie</option><option value='asc' name='filterasc'>Naam: A - Z</option><option value='desc' name='filterdesc' selected>Naam: Z - A</option><option value='priceasc' name='filterasc'>Prijs: Oplopend</option><option value='pricedesc' name='filterdesc'>Prijs: Aflopend</option>"
    elif order == "priceasc":
        txt += "<option>Relevantie</option><option value='asc'>Naam: A - Z</option><option value='desc'>Naam: Z - A</option><option value='priceasc' name='filterasc' selected>Prijs: Oplopend</option><option value='pricedesc' name='filterdesc'>Prijs: Aflopend</option>"
    elif order == "pricedesc":
        txt += "<option>Relevantie</option><option value='asc'>Naam: A - Z</option><option value='desc'>Naam: Z - A</option><option value='priceasc' name='filterasc'>Prijs: Oplopend</option><option value='pricedesc' name='filterdesc' selected>Prijs: Aflopend</option>"
    else:
        txt += "<option selected>Relevantie</option><option value='asc'>Naam: A - Z</option><option value='desc'>Naam: Z - A</option><option value='priceasc' name='filterasc'>Prijs: Oplopend</option><option value='pricedesc' name='filterdesc'>Prijs: Aflopend</option>"
    txt += """</select>
    	 <p id='sortp'>Sorteren op: </p>
    	 </div>"""
    # txt += "</form>"
    return txt

@register.simple_tag()
def searchList(results, userAuth):
    if not results:
        txt = """<b><p id='geenproduct'>Helaas hebben we geen product kunnen vinden voor uw zoekopdracht!</p></b><img src="/static/images/sadbatmanisbestbatman.png" id='sadbatman'>"""
        return txt

    # Structuur url: localhost:8000/search/Hulk/{smallfilter bvb 'asc'}/{sidefilter aka 'Dutch'}/
    # Voorbeeld beide filters url: localhost:8000/search/Hulk/priceasc/marvel/

    # 'items' wilt zeggen dat er geen filter is
    # geen smallfilter: localhost:8000/search/Hulk/items/English
    # geen sidefilter: localhost:8000/search/Hulk/asc/items/
    # helemaal geen filter localhost:8000/search/Hulk/items/items/

    txt = ""

    # TODO: Hall of Shame Code right here
    # qrytxt = "SELECT * FROM store_products INNER JOIN store_productdetails on store_products.\"prodNum\" = store_productdetails.\"prodNum\" WHERE \"prodName\" like '%%" + query + "%%' " + filter
    # object = ProductDetails.objects.raw("SELECT * FROM store_products INNER JOIN store_productdetails on store_products.\"prodNum\" = store_productdetails.\"prodNum\" WHERE \"prodName\" like '%%" + query + "%%' " + filter)

    counter = 0
    for e in results:
        if counter == 0:
            txt += "<ul class='list'>"
        txt = txt + "<li><div class='productwrap'><a href='/product/" + str(
            e.prodNum.prodNum) + "'><img src='" + e.imageLink + "' id='zoom_05' data-zoom-image='https://i.pinimg.com/736x/86/ff/e2/86ffe2b49daf0feed78a1c336753696d--black-panther-comic-digital-comics.jpg'></a><p class='author'>" + e.author + "</p><p class='name'>" + e.prodNum.prodName + "</p><p></p>"
        for i in range(0, e.rating):
            txt = txt + "<i class='fa fa-star' aria-hidden='true'></i>"
        txt = txt + "<p class='price'>€ " + str(
            e.prodNum.prodPrice) + "</p>"
        if e.prodNum.prodStock >= 1:
            txt += "<button name='addToCartItemBoxButton' value='" + str(
            e.prodNum.prodNum) + "'class='addtocart'><i class='fa fa-plus' aria-hidden='true'></i><i class='fa fa-shopping-cart' aria-hidden='true'></i></button>"
        else:
            txt += "<button name='addToCartItemBoxButton' id='outofstock' type=button class='addtocart tooltip'><i class='fa fa-ban' aria-hidden='true'></i><span class='tooltiptext'>Dit product is momenteel helaas uitverkocht.</span></button>"
        if userAuth:
            txt = txt + "<button name='moveToWishListButton' value='" + str(
                e.prodNum.prodNum) + "' class='wishlist'><i class='fa fa-heart' aria-hidden='true'></i></button>"
        if e.prodNum.prodStock >= 1:
            txt = txt + "<p class='stock'>Voorraad: " + str(e.prodNum.prodStock) + "</p></div></li>"
        else:
            txt = txt + "<p class='stock' style='color: #d45f5f;'>Uitverkocht!</p></div></li>"
        if counter == 2:
            txt += "</ul>"
            counter = 0
        else:
            counter = counter + 1
    return txt

@register.simple_tag()
def getAllProducts(objects, userAuth):
    if not objects:
        txt = """<b><p id='geenproduct'>Helaas hebben we geen product kunnen vinden voor uw zoekopdracht!</p></b><img src="/static/images/sadbatmanisbestbatman.png" id='sadbatman'>"""
        return txt

    txt = ""
    counter = 0
    for e in objects:
        if counter == 0:
            txt += "<ul class='list'>"
        txt = txt + "<li><div class='productwrap'><a href='/product/" + str(e.prodNum.prodNum) + "'><img src='" + e.imageLink + "' id='zoom_05' data-zoom-image='https://i.pinimg.com/736x/86/ff/e2/86ffe2b49daf0feed78a1c336753696d--black-panther-comic-digital-comics.jpg'></a><p class='author'>" + e.author + "</p><p class='name'>" + e.prodNum.prodName + "</p><p></p>"
        for i in range(0, e.rating):
            txt = txt + "<i class='fa fa-star' aria-hidden='true'></i>"
        txt += "<p class='price'>€ " + str(e.prodNum.prodPrice) + "</p>"
        if e.prodNum.prodStock >= 1:
            txt = txt + "<button name='addToCartItemBoxButton' value='" + str(e.prodNum.prodNum) + "'class='addtocart'><i class='fa fa-plus' aria-hidden='true'></i><i class='fa fa-shopping-cart' aria-hidden='true'></i></button>"
        else:
            txt += "<button name='addToCartItemBoxButton' id='outofstock' type=button class='addtocart tooltip'><i class='fa fa-ban' aria-hidden='true'></i><span class='tooltiptext'>Dit product is momenteel helaas uitverkocht.</span></button>"
        if userAuth:
            txt = txt + "<button name='moveToWishListButton' value='" + str(e.prodNum.prodNum) + "' class='wishlist'><i class='fa fa-heart' aria-hidden='true'></i></button>"
        if e.prodNum.prodStock >= 1:
            txt = txt + "<p class='stock'>Voorraad: " + str(e.prodNum.prodStock) + "</p></div></li>"
        else:
            txt = txt + "<p class='stock' style='color: #d45f5f;'>Uitverkocht!</p></div></li>"
        if counter == 2:
            txt += "</ul>"
            counter = 0
        else:
            counter = counter + 1
    return txt