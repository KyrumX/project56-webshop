from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from store.tokens import account_activation_token
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .database.getData import getProdName, getProdNum, getProdPrice, getProdStock, getProdGenre, getProdType, getProdAuthor, getProdDesc, getProdImage, getProdLanguage, getProdPublish, getProdRating, getProdTotalPages, getProdData
from .database.verifyData import verifyProdNum
from .collections.forms import ContactForm
from .collections.forms import RegistrationForm, LogginginForm
from django.http import *
from .database.getData import getResult
from .database.getData import getResult2
from .templatetags.custom_tags import resulttest
from django.contrib.auth import authenticate
from .database.CartOps import addToCart, removeFromCart
from .database.WishListOps import addToWishList, removeFromWishList

# Create your views here.

def index(request):
    print("Session key: " + str(request.session.session_key))
    if request.method == 'POST':
        if 'searchtext' in request.POST:
            return redirect("search/" + (str(request.POST.get('searchtext'))))

    return render(request, 'index.html')

def contact(request):
    formClass = ContactForm

    if request.method == 'POST':
        if 'searchtext' in request.POST:
            return redirect("/search/" + (str(request.POST.get('searchtext'))))
        form = formClass(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get('contact_name', '')
            contact_email = request.POST.get('contact_email', '')
            contact_content = request.POST.get('content', '')

            template = get_template('mail/contact_template.txt')
            context = {
                    'contact_name' : contact_name,
                    'contact_email' : contact_email,
                    'contact_content' : contact_content,
                }

            content = template.render(context)

            email = EmailMessage(
                "Nieuwe contact aanvraag",
                content,
                'noreply@comicfire.com',
                ['admin@comicfire.com'],
                headers = {'Reply-to': contact_email}
            )
            email.send()
            return redirect('messagesend')

    return render(request, 'contact.html', {'contact_form':formClass, })

def register(request):
    args = {}
    if request.method == 'POST':
        if 'searchtext' in request.POST:
            return redirect("/search/" + (str(request.POST.get('searchtext'))))
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
            mail_subject = 'Activate your blog account'
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
            return redirect("/search/" + (str(request.POST.get('searchtext'))))
    return render(request, 'faq.html')

def about(request):
    if request.method == 'POST':
        if 'searchtext' in request.POST:
            return redirect("/search/" + (str(request.POST.get('searchtext'))))
    return render(request, 'about.html')

def product(request):
    if request.method == 'POST':
        if 'searchtext' in request.POST:
            return redirect("/search/" + (str(request.POST.get('searchtext'))))
    return render(request, 'product.html')

def product2(request, item):
    if request.method == 'POST':
        if "addToCartButton" in request.POST:
            print("Adding to cart")
            if not request.session.exists(request.session.session_key):
                print("Creating session...")
                request.session.create()
            addToCart(request, item)
            return redirect('/winkelwagentje/')
        elif "addtowishlistButton" in request.POST:
            addToWishList(request, item)
            return redirect('/verlanglijst/')
        elif 'searchtext' in request.POST:
            return redirect("/search/" + (str(request.POST.get('searchtext'))))




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
    return render(request, 'product2.html', {
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

def search(request, query):
    if request.method == 'POST':
        if 'searchtext' in request.POST:
            return redirect("/search/" + (str(request.POST.get('searchtext'))))

    thequery = query
    return render(request, 'testing.html', {
        'query' : thequery,
    })

def about(request):
    if request.method == 'POST':
        if 'searchtext' in request.POST:
            return redirect("/search/" + (str(request.POST.get('searchtext'))))
    return render(request, 'about.html')

def logoutview(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    else:
        return redirect('/')


def loginview(request):
    if request.method == "POST":
        if 'searchtext' in request.POST:
            return redirect("/search/" + (str(request.POST.get('searchtext'))))
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return redirect('/login')
    else:
        return render(request, 'login.html', {'form': LogginginForm})

def registrationcomplete(request):
    if request.method == 'POST':
        if 'searchtext' in request.POST:
            return redirect("/search/" + (str(request.POST.get('searchtext'))))
    return render(request, 'completeregistration.html')

def activate(request, uidb64, token):
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
    return render(request, 'mailsend.html')

def results(request, query):

    #returnPage(request.GET.get('searchtext'))
    object = getResult2(query)
    print(object)
#    prodName = getProdName()
 #   prodPrice = getProdPrice()
  #  prodStock = getProdStock()
   # prodAuthor = getProdAuthor()
    return render(request, 'testing.html')

def shoppingcart(request):
    if request.method == 'POST':
        if 'removeFromCartButton' in request.POST:
            removeFromCart(request, int(request.POST.get('removeFromCartButton')))
            return redirect('/winkelwagentje/')
        elif "moveToWishListButton" in request.POST:
            addToWishList(request, int(request.POST.get('moveToWishListButton')))
            return redirect('/verlanglijst/')
        elif 'searchtext' in request.POST:
            return redirect("/search/" + (str(request.POST.get('searchtext'))))
    return render(request, 'shoppingcart.html')

def wishlist(request):
    if not request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        if 'removeFromWishListButton' in request.POST:
            removeFromWishList(request, int(request.POST.get('removeFromWishListButton')))
            return redirect('/verlanglijst/')
        elif 'searchtext' in request.POST:
            return redirect("/search/" + (str(request.POST.get('searchtext'))))
    return render(request, 'wishlist.html')


