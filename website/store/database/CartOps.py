from ..models import ShoppingCart, Products

def addToCart(request, prodnum):
    if not checkIfExists(request, prodnum):
        item = ShoppingCart(session_key=request.session.session_key, prodNum=Products(prodNum=prodnum), amount=1)
        item.save()
    else:
        if checkoverstock(request, prodnum):
            incrementEntry(request, prodnum)

def checkIfExists(request, prodnum):
    print("It exists.")
    return ShoppingCart.objects.filter(session_key=request.session.session_key, prodNum=Products(prodNum=prodnum)).exists()

def incrementEntry(request, prodnum):
    existingEntry = ShoppingCart.objects.get(session_key=request.session.session_key, prodNum=Products(prodNum=prodnum))
    existingEntry.amount += 1
    existingEntry.save()

def checkoverstock(request, prodnum):
    amount = ShoppingCart.objects.get(session_key=request.session.session_key, prodNum=Products(prodNum=prodnum)).amount
    print("Currently of this product in cart: ", amount)
    stock = Products.objects.get(prodNum=prodnum).prodStock
    if amount < stock:
        return True
    return False

def cartLength(sessionkey):
    return ShoppingCart.objects.all().filter(session_key=sessionkey).count()

def removeFromCart(request, prodnum):
    ShoppingCart.objects.filter(session_key=request.session.session_key, prodNum=Products(prodNum=prodnum)).delete()

def clearCart(request):
    for e in ShoppingCart.objects.all().filter(session_key=request.session.session_key):
        e.delete()

def setAmount(request, prodnum, amount):
    existingEntry = ShoppingCart.objects.get(session_key=request.session.session_key, prodNum=Products(prodNum=prodnum))
    existingEntry.amount = amount
    existingEntry.save()
