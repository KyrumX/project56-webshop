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
                 "<div class='bartext'>"
        for e in relevantItems:
            if e == 'Engels':
                if 'English' in selectedFilters:
                    html += "<input type='checkbox' onchange='this.form.submit()' name='language' value='English' id='english' checked>"
                else:
                    html += "<input type='checkbox' onchange='this.form.submit()' name='language' value='English' id='english'>"
                html += "<label for='english'></label><p>Engels</p><br>"
            elif e == 'Nederlands':
                if 'Dutch' in selectedFilters:
                    html += "<input type='checkbox' onchange='this.form.submit()' name='language' value='Dutch' id='dutch' checked>"
                else:
                    html += "<input type='checkbox' onchange='this.form.submit()' name='language' value='Dutch' id='dutch'>"
                html += "<label for='dutch'></label><p>Nederlands</p><br>"
        html += "</div></div>"
        return html
    return ""

@register.simple_tag()
def typeFilter(relevantItems, selectedFilters):
    html = ""
    if relevantItems != None:
        html += "<div class='barwrap'><div class='leftbar commoncolor'>" \
                "<p>Type Boek<i class='fa fa-sort-desc' aria-hidden='true' id='sortdown'></i></p>" \
                "</div>" \
                "<div class='bartext'>"
        for e in relevantItems:
            if e == 'Manga':
                if 'manga' in selectedFilters:
                    html += "<input type='checkbox' onchange='this.form.submit()' name='type' value='manga' id='manga' checked>"
                else:
                    html += "<input type='checkbox' onchange='this.form.submit()' name='type' value='manga' id='manga'>"
                html += "<label for='manga'></label><p>Manga</p><br>"
            elif e == 'Comic':
                if 'comic' in selectedFilters:
                    html += "<input type='checkbox' onchange='this.form.submit()' name='type' value='comic' id='comic' checked>"
                else:
                    html += "<input type='checkbox' onchange='this.form.submit()' name='type' value='comic' id='comic'>"
                html += "<label for='comic'></label><p>Comic</p><br>"
        html += "</div></div>"
        return html
    return ""

@register.simple_tag()
def publisherFilter(relevantItems, selectedFilters):
    html = ""
    if relevantItems != None:
        html += "<div class='barwrap'><div class='leftbar commoncolor'>" \
                "<p>Type Boek<i class='fa fa-sort-desc' aria-hidden='true' id='sortdown'></i></p>" \
                "</div>" \
                "<div class='bartext'>"
        for e in relevantItems:
            if e in selectedFilters:
                html += "<input type='checkbox' onchange='this.form.submit()' value='" + e + "' name='publisher' id='" + e +"' checked>"
            else:
                html += "<input type='checkbox' onchange='this.form.submit()' value='" + e + "' name='publisher' id='" + e +"'>"
            html += "<label for='" + e + "'></label><p>"+ e +"</p><br>"
        html += "</div></div>"
        return html
    return ""

@register.simple_tag()
def orderbyForm(order, size):
    print(order)
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