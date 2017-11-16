from ..models import Address, Customers, Orders


def saveAddress(request):
    if not Address.objects.filter(customerID=Customers(request.user.id)).exists():
        account_address = request.POST.get('address', '')
        account_number = request.POST.get('number', '')
        account_city = request.POST.get('city', '')
        account_postalcode = request.POST.get('postalcode', '')

        newEntry = Address(customerID=Customers(request.user.id), address=account_address, number=account_number, city=account_city, postalcode=account_postalcode)
        newEntry.save()
    else:
        updateAddress(request)


def updateAddress(request):
    updateEntry = Address.objects.get(customerID=Customers(request.user.id))
    updateEntry.address= request.POST.get('address', '')
    updateEntry.number= request.POST.get('number', '')
    updateEntry.city= request.POST.get('city', '')
    updateEntry.postalcode= request.POST.get('postalcode', '')
    updateEntry.save()

def updateCustomerInfo(request):
    updateInfo = Customers.objects.get(customerID=request.user.id)
    updateInfo.name = request.POST.get('name', '')
    updateInfo.surname = request.POST.get('surname', '')
    updateInfo.telephone = request.POST.get('telephone', '')
    updateInfo.save()

def getOrderAmount(request):
    object = Orders.objects.filter(customerID=Customers(request.user.id)).count()
    return object

def getOrders(request):
    if Orders.objects.filter(customerID=Customers(request.user.id)).exists():
        objects = Orders.objects.all().filter(customerID=Customers(request.user.id))
        return objects
