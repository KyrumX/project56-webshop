from django import template

register = template.Library()

@register.simple_tag()
def languageFilter(objects, languages):
    html = ""
    categories = isCategoryRelevant(objects, 'language')
    if categories != None:
        html +=  "<div class='barwrap'>" \
                 "<div class='leftbar commoncolor'>" \
                 "<p>Taal<i class='fa fa-sort-desc' aria-hidden='true' id='sortdown'></i></p></div>" \
                 "<div class='bartext'>"
        for e in categories:
            if e == 'Engels':
                if 'English' in languages:
                    html += "<input type='checkbox' onchange='this.form.submit()' name='language' value='English' id='english' checked>"
                else:
                    html += "<input type='checkbox' onchange='this.form.submit()' name='language' value='English' id='english'>"
                html += "<label for='english'></label><p>Engels</p><br>"
            elif e == 'Nederlands':
                if 'Dutch' in languages:
                    html += "<input type='checkbox' onchange='this.form.submit()' name='language' value='Dutch' id='dutch' checked>"
                else:
                    html += "<input type='checkbox' onchange='this.form.submit()' name='language' value='Dutch' id='dutch'>"
                html += "<label for='dutch'></label><p>Nederlands</p><br>"
        html += "</div></div>"
        return html
    return ""

@register.simple_tag()
def typeFilter(objects, types):
    html = ""
    categories = isCategoryRelevant(objects, 'type')
    if categories != None:
        html += "<div class='barwrap'><div class='leftbar commoncolor'>" \
                "<p>Type Boek<i class='fa fa-sort-desc' aria-hidden='true' id='sortdown'></i></p>" \
                "</div>" \
                "<div class='bartext'>"
        for e in categories:
            if e == 'Manga':
                if 'manga' in types:
                    html += "<input type='checkbox' onchange='this.form.submit()' name='type' value='manga' id='manga' checked>"
                else:
                    html += "<input type='checkbox' onchange='this.form.submit()' name='type' value='manga' id='manga'>"
                html += "<label for='manga'></label><p>Manga</p><br>"
            elif e == 'Comic':
                if 'comic' in types:
                    html += "<input type='checkbox' onchange='this.form.submit()' name='type' value='comic' id='comic' checked>"
                else:
                    html += "<input type='checkbox' onchange='this.form.submit()' name='type' value='comic' id='comic'>"
                html += "<label for='comic'></label><p>Comic</p><br>"
        html += "</div></div>"
        return html
    return ""

@register.simple_tag()
def publisherFilter(objects, publishers):
    html = ""
    categories = isCategoryRelevant(objects, 'publisher')
    if categories != None:
        html += "<div class='barwrap'><div class='leftbar commoncolor'>" \
                "<p>Type Boek<i class='fa fa-sort-desc' aria-hidden='true' id='sortdown'></i></p>" \
                "</div>" \
                "<div class='bartext'>"
        for e in categories:
            if e in publishers:
                html += "<input type='checkbox' onchange='this.form.submit()' value='" + e + "' name='publisher' id='" + e +"' checked>"
            else:
                html += "<input type='checkbox' onchange='this.form.submit()' value='" + e + "' name='publisher' id='" + e +"'>"
            html += "<label for='" + e + "'></label><p>"+ e +"</p><br>"
        html += "</div></div>"
        return html
    return ""

def isCategoryRelevant(objects, field):
    categories = []
    found = objects.distinct(field)
    for e in found:
        if field == 'language':
            if len(categories) >= 2:
                break
            if (e.language == 'English' or e.language == 'en-us' or e.language == 'Engels') and 'Engels' not in categories:
                categories.append('Engels')
            elif (e.language == 'Dutch' or e.language == 'nl-nl' or e.language == 'Nederlands') and 'Nederlands' not in categories:
                categories.append('Nederlands')
        elif field == 'type':
            if len(categories) >= 2:
                break
            if (e.type == 'Manga' or e.type == 'manga') and 'Manga' not in categories:
                categories.append('Manga')
            elif (e.type == 'Comic' or e.type == 'comic') and 'Comic' not in categories:
                categories.append('Comic')
        elif field == 'publisher':
            categories.append(e.publisher)
    if len(categories) >= 2:
        return categories
    else:
        return None
