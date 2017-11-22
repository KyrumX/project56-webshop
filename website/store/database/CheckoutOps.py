from django.db.models import Max

from ..models import Orders, OrderDetails, ShoppingCart, Customers, Address
from django.utils import timezone
from .CartOps import clearCart

def createOrder(request):
    date = timezone.now().date()
    status = "Processed"

    if not request.user.is_authenticated:
        custID = createCustomer(request)
    else:
        custID = request.user.id

    orderEntry = Orders(orderNum=getNewOrderNum(), orderDate=date, orderStatus=status, customerID=Customers(customerID=custID))
    orderEntry.save()
    for e in ShoppingCart.objects.all().filter(session_key=request.session.session_key):
        orderDetailsEntry = OrderDetails(amount=e.amount, orderNum=Orders(orderNum=orderEntry.orderNum), productNum=e.prodNum)
        orderDetailsEntry.save()

    createAddress(request, custID) #Sla het adres op, of update deze indien nodig

    c = request.session['customer_email']

    # contact_name = request.POST.get('contact_name', '')
    # contact_email = request.POST.get('contact_email', '')
    # contact_content = request.POST.get('content', '')
    html_content = render_to_string('templates/mail/order_complete_email.html')
    text_content = render_to_string('templates/mail/order_complete_email.txt')

    email = EmailMultiAlternatives("Your order details", text_content, 'noreply@comicfire.com', [c])
    email.attach_alternative(html_content, "text/html")
    # email.attach_file('static/images/comicfirelogo2.png')
    email.mixed_subtype = 'related'

    email.send()

    clearCart(request) #Maak de shoppingcart weer leeg

def getNewOrderNum():
    maxC = Orders.objects.all().aggregate(Max('orderNum'))
    if maxC.get('orderNum__max') == None:
        return 1
    else:
        return maxC.get('orderNum__max') + 1

def createCustomer(request):
    customerEntry = Customers(customerID=getNewCustomerNum(), email=request.session['customer_email'], name=request.session['customer_fname'], surname=request.session['customer_lname'], telephone=request.session['customer_phone'], isRegistered=False)
    customerEntry.save()
    return customerEntry.customerID

def getNewCustomerNum():
    maxC = Customers.objects.all().aggregate(Max('customerID'))
    if maxC.get('customerID__max') == None:
        return 1
    else:
        return maxC.get('customerID__max') + 1

def createAddress(request, custID):
    if request.user.is_authenticated:
        updateAddress(request, custID)
    else:
        addressEntry = Address(address=request.session['customer_address'], number=request.session['customer_adressnum'], city=request.session['customer_city'], postalcode=request.session['customer_postalcode'], customerID=Customers(customerID=custID))
        addressEntry.save()

def updateAddress(request, custID):
    if not Address.objects.filter(customerID=Customers(customerID=custID)).exists():
        newEntry = Address(address=request.session['customer_address'], number=request.session['customer_adressnum'], city=request.session['customer_city'], postalcode=request.session['customer_postalcode'], customerID=Customers(customerID=custID))
        newEntry.save()
    else:
        existingEntry = Address.objects.get(customerID=Customers(customerID=custID))
        existingEntry.address = request.session['customer_address']
        existingEntry.number=request.session['customer_adressnum']
        existingEntry.city=request.session['customer_city']
        existingEntry.postalcode=request.session['customer_postalcode']
        existingEntry.save()