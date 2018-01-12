import random
import string

from django.contrib.auth.models import User

from store.models import Address, Customers, Orders


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
    print(updateInfo.telephone)
    updateInfo.save()

def editUser(request, userid):
    updateUser = Customers.objects.get(customerID=userid)
    updateAddress = Address.objects.get(customerID=Customers(userid))
    updateUser.name = request.POST.get('name', '')
    updateUser.surname = request.POST.get('surname', '')
    updateUser.telephone = request.POST.get('telephone', '')
    if request.POST.get('isBlocked') == 'on':
        blockedStatus = True
    else:
        blockedStatus = False
    updateUser.isBlocked = blockedStatus
    updateAddress.address= request.POST.get('address', '')
    updateAddress.number= request.POST.get('number', '')
    updateAddress.city= request.POST.get('city', '')
    updateAddress.postalcode= request.POST.get('postalcode', '')
    updateAddress.save()
    updateUser.save()

def getOrderAmount(request):
    object = Orders.objects.filter(customerID=Customers(request.user.id)).count()
    return object

def getOrders(request):
    if Orders.objects.filter(customerID=Customers(request.user.id)).exists():
        objects = Orders.objects.all().filter(customerID=Customers(request.user.id))
        return objects

def checkOrder(request, prodnum):
    if Orders.objects.filter(customerID=Customers(request.user.id), orderNum=prodnum).exists():
        return True
    return False

def checkIfCustomerExist(userid):
    return Customers.objects.filter(customerID=userid).exists()

def checkIfAuthUserExist(userid):
    return User.objects.filter(id=userid).exists()

def deleteUser(request):
    userId = int(request.POST['deleteuser'])
    if checkIfCustomerExist(userId):
        #We do not have to delete the orders or address associated with this user, Django does this automatically :D
        Customers.objects.filter(customerID=userId).delete()

    if checkIfAuthUserExist(userId):
        User.objects.filter(id=userId).delete()

def getUserId(email):
    return User.objects.get(email=email).id

def isUserBlocked(userId):
    customer = Customers.objects.get(customerID=userId)
    return customer.isBlocked

def adminresetpw(request):
    c_id = int(request.POST['resetpwuser'])
    print("Changing pw for user: ", c_id)
    user = User.objects.get(id=c_id)

    newpw = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    print("Old password: ", user.password)

    user.set_password(newpw)

    user.save()

    print("This is the new set password: ", newpw)

    # message = render_to_string('mail/acc_active_email.html', {
    #     'user': user,
    #     'domain': 'Comicfire.com',
    #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
    #     'pwd': newpw,
    # })
    #
    # mail_subject = 'Uw nieuwe wachtwoord.'
    # to_email = user.email
    # email = EmailMessage("Test", "test", to=[user.email])
    # email.send()

    # send_mail(
    #     'Uw nieuwe wachtwoord.',
    #     "Beste lid, <br> Hierbij uw nieuwe wachtwoord: {}".format(str(newpw)),
    #     'admin@comicfire.com',
    #     [user.email],
    #     fail_silently=False,
    # )

