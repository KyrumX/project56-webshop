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

