from django.db.models import Max, Min


def get_max_price_prodDetails(objects):
    maxp = objects.all().aggregate(Max('prodNum__prodPrice'))
    return maxp['prodNum__prodPrice__max']

def get_min_price_prodDetails(objects):
    maxp = objects.all().aggregate(Min('prodNum__prodPrice'))
    return maxp['prodNum__prodPrice__min']