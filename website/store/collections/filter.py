def filterObjects(entries, filteritems):
    if 'language' in filteritems and entries.exists():
        languages = []
        for language in filteritems['language']:
            if language == 'English':
                languages.append(language)
                languages.append('Engels')
                languages.append('en-us')
            elif language == 'Dutch':
                languages.append(languages)
                languages.append('nl-nl')
                languages.append('Nederlands')
        entries = entries.filter(language__in=languages)
    if 'type' in filteritems and entries.exists():
        types = []
        for typex in filteritems['type']: #typex to prevent confusion with the function type()
            if typex == 'comic':
                types.append(typex)
                types.append('Comic')
            elif typex == 'manga':
                types.append(typex)
                types.append('Manga')
            elif typex == 'manga':
                types.append(typex)
                types.append('Manga')
        entries = entries.filter(type__in=types)
    if 'publisher' in filteritems and entries.exists():
        publishers = []
        for publisher in filteritems['publisher']:
            publishers.append(publisher)
        entries = entries.filter(publisher__in=publishers)
    if 'score' in filteritems and entries.exists():
        scores = []
        for score in filteritems['score']:
            scores.append(score)
        entries = entries.filter(rating__in=scores)
    if 'pmax' in filteritems and 'pmin' in filteritems and entries.exists():
        entries = entries.filter(prodNum__prodPrice__lte=filteritems['pmax'], prodNum__prodPrice__gte=filteritems['pmin'])

    return entries