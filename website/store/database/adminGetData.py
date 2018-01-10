import operator
from functools import reduce
from django.db.models import Q
from store.models import Customers, Products


def ifUserExists(query):
    try:
        query = int(query)
    except ValueError:
        try:
            query = str(query)
        except ValueError:
            return False
    if isinstance(query, str):
        splitQuery = query.split(" ")  # Split de query als er een voor en achternaam worden ingevoerd
        searchQueryName = reduce(operator.or_, (Q(name__icontains=item) for item in splitQuery))
        searchQuerySurname = reduce(operator.or_, (Q(surname__icontains=item) for item in splitQuery))
        nameExist = Customers.objects.filter(Q(name__icontains=query) | Q(surname__icontains=query) | Q(email__icontains=query) | Q(searchQueryName) | Q(searchQuerySurname)).exists()
        print(nameExist)
        if nameExist == True:
            return True
        return False
    if isinstance(query, int):
        idExist = Customers.objects.filter(customerID=query).exists()
        if idExist == True:
            return True
        return False

def getUsers(query):
    try:
        query = int(query)
    except ValueError:
        try:
            query = str(query)
        except ValueError:
            #   Just to be safe
            return Customers.objects.all()
    if isinstance(query, str):
        splitQuery = query.split(" ") #Split de query als er een voor en achternaam worden ingevoerd
        searchQueryName = reduce(operator.or_, (Q(name__icontains=item) for item in splitQuery))
        searchQuerySurname = reduce(operator.or_, (Q(surname__icontains=item) for item in splitQuery))
        names = Customers.objects.filter(
            Q(name__icontains=query) |
            Q(surname__icontains=query) |
            Q(email__icontains=query) |
            Q(name__in=splitQuery) |
            Q(surname__in=splitQuery) |
            Q(searchQueryName) | Q(
                searchQuerySurname))\
            .order_by('customerID')
        return names

    if isinstance(query, int):
        id = Customers.objects.filter(customerID=query)
        return id

def ifProductExists(query):
  try:
    query = int(query)
  except ValueError:
    try:
      query = str(query)
    except ValueError:
      return False
  if isinstance(query, str):
    prodExist = Products.objects.filter(Q(prodName__icontains=query)).exists()
    if prodExist == True:
      return True
    return False
  if isinstance(query, int):
    idExist = Products.objects.filter(prodNum=query).exists()
    if idExist == True:
      return True
    return False

def getProducts(query):
    try:
      query = int(query)
    except ValueError:
      try:
        query = str(query)
      except ValueError:
        print("Something went really bad...")
    if isinstance(query, str):
      products = Products.objects.filter(Q(prodName__icontains=query)).order_by('prodNum')
      return products

    if isinstance(query, int):
      id = Products.objects.filter(prodNum=query).order_by('prodNum')
      return id