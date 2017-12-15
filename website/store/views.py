from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from store.tokens import account_activation_token
from .collections.mails import *
from django.contrib.auth import login, logout, update_session_auth_hash
from .database.getData import getProdName, getProdPrice, getProdStock, getProdGenre, getProdType, getProdAuthor, getProdDesc, getProdImage, getProdLanguage, getProdPublish, getProdRating, getProdTotalPages, getProdData, getStreet, getHouseNumber, getCity, getPostalcode, getCustomerFName, getCustomerLName, getCustomerPhone
from .database.verifyData import verifyProdNum
from .collections.forms import *
from django.http import *
from django.forms import ModelForm
from django.contrib.auth import authenticate
from .database.CartOps import addToCart, removeFromCart
from .database.getData import queryVerbeterFunctie
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate
from .database.CartOps import addToCart, removeFromCart
from .database.WishListOps import removeFromWishList
from .collections.posts import *
from .database.CheckoutOps import *
from .database.AccountOps import *
import os
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from email.mime.image import MIMEImage
from .collections.tools import *


from .database.CartOps import setAmount

# Create your views here.


def index(request):
    if request.method == 'POST':
        if 'searchtext' in request.POST:
            return searchPost(request)
        elif 'addToCartItemBoxButton' in request.POST:
            if not request.session.exists(request.session.session_key):
                request.session.create()
            addToCart(request, int(request.POST.get('addToCartItemBoxButton')))
            return redirect('/winkelwagentje/')
        elif 'moveToWishListButton' in request.POST:
            return addToWishListPost(request)
        elif 'filter' in request.POST:
            return searchPost(request)

    return render(request, 'index.html')


def emailstyle(request):
    return render(request, 'emailstyle.html')


def contact(request):
    if request.user.is_authenticated:
        formClass = ContactForm(initial={'contact_name': str(request.user.first_name + " " + request.user.last_name), 'contact_email': request.user.email})
    else:
        formClass = ContactForm()

    if request.method == 'POST':
        if 'searchtext' in request.POST:
            return searchPost(request)
        elif 'contactsubmitbutton' in request.POST:
            form = ContactForm(data=request.POST)

            if form.is_valid():
                contactRequestMail(request)
                return redirect('messagesend')

    return render(request, 'contact.html', {'contact_form':formClass, })


def register(request):
    args = {}
    if request.method == 'POST':
        if 'searchtext' in request.POST:
            return searchPost(request)
        elif 'registerbutton' in request.POST:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                message = render_to_string('mail/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                mail_subject = 'Activeer uw account!'
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                # form.save()
                return render(request, 'completeregistration.html')
    else:
        form = RegistrationForm()
    args['form'] = form
    return render(request, 'register.html', args)


def faq(request):
    if request.method == 'POST':
        if 'searchtext' in request.POST:
            return searchPost(request)

    return render(request, 'faq.html')


def about(request):
    if request.method == 'POST':
        if 'searchtext' in request.POST:
            return searchPost(request)

    return render(request, 'about.html')


def servicevoorwaarden (request):
    if request.method == 'POST':
        if 'searchtext' in request.POST:
            return searchPost(request)

    return render(request, 'servicevoorwaarden.html')


def retourneren (request):
    if request.method == 'POST':
        if 'searchtext' in request.POST:
            return searchPost(request)

    return render(request, 'retourneren.html')


def privacy(request):
    if request.method == 'POST':
        if 'searchtext' in request.POST:
            return searchPost(request)

    return render(request, 'privacy.html')


def betaling(request):
    if request.method == 'POST':
        if 'searchtext' in request.POST:
            return searchPost(request)

    return render(request, 'betaling.html')


def product(request, item):
    if request.method == 'POST':
        if 'searchtext' in request.POST:
            return searchPost(request)
        elif "addToCartButton" in request.POST:
            if not request.session.exists(request.session.session_key):
                request.session.create()
            addToCart(request, item)
            return redirect('/winkelwagentje/')
        elif "addtowishlistButton" in request.POST:
            addToWishList(request, item)
            return redirect('/verlanglijst/')

    if not verifyProdNum(item):
        return render(request, 'productnietgevonden.html')

    productNumber = (int(item))
    prodName = getProdName(productNumber)
    prodPrice = getProdPrice(productNumber)
    prodStock = getProdStock(productNumber)
    prodGenre = getProdGenre(productNumber)
    prodType = getProdType(productNumber)
    prodPublisher = getProdPublish(productNumber)
    prodPages = getProdTotalPages(productNumber)
    prodLanguage = getProdLanguage(productNumber)
    prodRating = getProdRating(productNumber)
    prodAuthor = getProdAuthor(productNumber)
    prodDesc = getProdDesc(productNumber)
    prodImage = getProdImage(productNumber)
    prodDate = getProdData(productNumber)
    return render(request, 'product.html', {
        'prodNum' : productNumber,
        'prodName' : prodName,
        'prodPrice' : prodPrice,
        'prodStock' : prodStock,
        'prodGenre' : prodGenre,
        'prodType' : prodType,
        'prodPublisher' : prodPublisher,
        'prodPages' : prodPages,
        'prodLanguage' : prodLanguage,
        'prodRating' : range(prodRating),
        'prodAuthor' : prodAuthor,
        'prodDesc' : prodDesc,
        'prodImage' : prodImage,
        'prodDate' : prodDate,
    })


def search(request, query, filter=""):
    if request.method == 'POST':
        print(request.POST)
        if 'addToCartItemBoxButton' in request.POST:
            if not request.session.exists(request.session.session_key):
                request.session.create()
            addToCart(request, int(request.POST.get('addToCartItemBoxButton')))
            return redirect('/winkelwagentje/')
        elif "moveToWishListButton" in request.POST:
            return addToWishListPost(request)
        elif 'filter' in request.POST:
            return searchPost(request)
        elif 'searchtext' in request.POST:
            return searchPost(request)

    # filt = "{}".format(request.POST.get('filter'))
    # print(filt)
    thequery = query
    thefilter = filter
    return render(request, 'searchresults.html', {
        'query' : thequery, 'filt' : thefilter,
    })


def logoutview(request):
    if request.method == 'POST':
            if 'searchtext' in request.POST:
                return searchPost(request)
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    else:
        return redirect('/')


def loginview(request):
    args = {}
    if request.method == "POST":
        print(request.POST)
        if 'searchtext' in request.POST:
            return searchPost(request)
        elif 'loginbutton' in request.POST:
            form = LogginginForm(request.POST)
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')


    else:
        form = LogginginForm()
    args['form'] = form
    return render(request, 'login.html', args)


def registrationcomplete(request):
    if request.method == "POST":
        if 'searchtext' in request.POST:
            return searchPost(request)
    return render(request, 'accountconfirmed.html')


def activate(request, uidb64, token):
    if request.method == 'POST':
            if 'searchtext' in request.POST:
                return searchPost(request)
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return render(request, 'completeregistration.html')
    else:
        return HttpResponse('Activation link is invalid!')


def contactRequestHandeld(request):
    if request.method == "POST":
        if 'searchtext' in request.POST:
            return searchPost(request)
    return render(request, 'mailsend.html')



def shoppingcart(request):
    if request.method == 'POST':
        if 'searchtext' in request.POST:
            return searchPost(request)
        elif 'removeFromCartButton' in request.POST:
            removeFromCart(request, int(request.POST.get('removeFromCartButton')))
            return redirect('/winkelwagentje/')
        elif "moveToWishListButton" in request.POST:
            return addToWishListPost(request)
        elif 'placeorderbutton' in request.POST:
            return redirect('/processorder/')
        elif 'amount' in request.POST:
            setAmount(request, int(request.POST.get('cartItemProdNum')), int(request.POST.get('amount')))
            return redirect('/winkelwagentje/')

    return render(request, 'shoppingcart.html')


def wishlist(request):
    if not request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        if 'searchtext' in request.POST:
            return searchPost(request)
        elif 'removeFromWishListButton' in request.POST:
            removeFromWishList(request, int(request.POST.get('removeFromWishListButton')))
            return redirect('/verlanglijst/')
        elif 'addToCartButton' in request.POST:
            addToCart(request, int(request.POST.get('addToCartButton')))
            return redirect('/winkelwagentje/')
    return render(request, 'wishlist.html')


def processOrder(request):
    if not request.META.get('HTTP_REFERER') is None:
        if '/winkelwagentje/' in request.META.get('HTTP_REFERER') or '/processorder/' in request.META.get('HTTP_REFERER'):
            if request.user.is_authenticated:
                return redirect('/customerdetails/')
            else:
                args = {}
                if request.method == 'POST':
                    if 'searchtext' in request.POST:
                        return searchPost(request)
                    elif 'loginbutton' in request.POST:
                        form = LogginginForm(request.POST)
                        username = request.POST['username']
                        password = request.POST['password']
                        user = authenticate(request, username=username, password=password)
                        if user is not None:
                            login(request, user)
                            return redirect('/customerdetails/')
                        else:
                            args['form'] = form
                            return render(request, 'processorder.html', args)
                else:
                    form = LogginginForm()
                args['form'] = form
                return render(request, 'processorder.html', args)
    else:
        return redirect('/')


def customerdetails(request):
    args = {}
    if not request.META.get('HTTP_REFERER') is None:
        if '/processorder/' in request.META.get('HTTP_REFERER') or '/customerdetails/' in request.META.get('HTTP_REFERER') or ('/winkelwagentje/' in request.META.get('HTTP_REFERER') and request.user.is_authenticated):
            if request.method =='POST':
                if 'searchtext' in request.POST:
                    return searchPost(request)
                elif 'customerdetailssubmitbutton' in request.POST:
                    form = CustomerDetails(data=request.POST)

                    if form.is_valid():
                        request.session['customer_fname'] = request.POST.get('customer_fname', '')
                        request.session['customer_lname'] = request.POST.get('customer_lname', '')
                        request.session['customer_email'] = request.POST.get('customer_email', '')
                        request.session['customer_phone'] = request.POST.get('customer_phone', '')
                        request.session['customer_address'] = request.POST.get('customer_address', '')
                        request.session['customer_adressnum'] = request.POST.get('customer_adressnum', '')
                        request.session['customer_city'] = request.POST.get('customer_city', '')
                        request.session['customer_postalcode'] = request.POST.get('customer_postalcode', '')
                        return redirect('/checkout/')
            else:
                if request.user.is_authenticated:
                    form = CustomerDetails(initial={'customer_phone':getCustomerPhone(request.user.id), 'customer_fname':getCustomerFName(request.user.id), 'customer_lname':getCustomerLName(request.user.id), 'customer_email':request.user.email, 'customer_address':getStreet(request.user.id), 'customer_adressnum':getHouseNumber(request.user.id), 'customer_city':getCity(request.user.id), 'customer_postalcode':getPostalcode(request.user.id)})
                else:
                    form = CustomerDetails()
            args['customerdetailsform'] = form
            return render(request, 'customerdetails.html', args)
        else:
            return redirect('/')
    return redirect('/')


def checkout(request):
    args = {}
    if not request.META.get('HTTP_REFERER') is None:
        if '/customerdetails/' in request.META.get('HTTP_REFERER') or '/checkout/' in request.META.get('HTTP_REFERER'):
            if request.method =='POST':
                if 'searchtext' in request.POST:
                    return searchPost(request)
                elif 'checkoutsubmitbutton' in request.POST:
                    form = CheckoutForm(data=request.POST)

                    if form.is_valid():

                        createOrder(request)
                        return render(request, 'completeorder.html')

            else:

                form = CheckoutForm()
            args['checkoutform'] = form
            return render(request, 'checkout.html', args)
        else:
            return redirect('/')
    return redirect('/')


def account(request):
    if request.method == 'POST':
            if 'searchtext' in request.POST:
                return searchPost(request)
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        return render(request, 'account.html')


def accountedit(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            if 'searchtext' in request.POST:
                return searchPost(request)
            accountinfo_form = CustomerInfoForm(request.POST)
            account_form = AccountForm(request.POST)
            if accountinfo_form.is_valid() and account_form.is_valid():
                updateCustomerInfo(request)
                saveAddress(request)
                return redirect('/account/')
        else:
            Inaddress = Address.objects.get(customerID=request.user.id)
            AddressData = {'address' : Inaddress.address, 'number' : Inaddress.number, 'city' : Inaddress.city, 'postalcode' : Inaddress.postalcode}
            account_form = AccountForm(initial=AddressData)
            Ininfo = Customers.objects.get(customerID=request.user.id)
            CustomerData = {'name': Ininfo.name, 'surname': Ininfo.surname, 'telephone': Ininfo.telephone}
            accountinfo_form = CustomerInfoForm(initial=CustomerData)

        return render(request, 'accountedit.html', {
            'account_form': account_form, 'accountinfo_form' : accountinfo_form,
        })


def changepassword(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            if 'searchtext' in request.POST:
                return searchPost(request)
            password_form = PasswordForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                return redirect('/account/')
        else:
            password_form = PasswordForm(request.user)
        return render(request, 'changepassword.html', {'password_form' : password_form})


def orderDetails(request):
    ordernum = request.GET.get('ordernum', '')

    if not RepresentInt(ordernum):
        raise Http404
    ordernum = int(ordernum)
    if not request.user.is_authenticated or not checkOrder(request, ordernum):
        raise PermissionDenied

    if request.method == 'POST':
        if 'searchtext' in request.POST:
            return searchPost(request)


    return render(request, 'orderdetails.html', {
        'ordernum' : ordernum
    })
