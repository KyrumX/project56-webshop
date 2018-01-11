import datetime

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.db.models import Sum
from django.views import View
from graphos.renderers import gchart
from graphos.sources.simple import SimpleDataSource

from store.collections.adminforms import AdminRegistrationForm, ProductsRegistrationForm
from store.collections.adminforms import EditProductForm, EditUserForm
from store.collections.forms import LogginginForm
from .collections.posts import *
from .database.AccountOps import *
from .database.ProductOps import editProduct, deleteProduct
from .models import Dates
from .models import OrderDetails
from .models import ProductDetails, Products


def admin(request):
    args = {}
    if request.method == "POST":
        print(request.POST)
        if 'loginbutton' in request.POST:
            form = LogginginForm(request.POST)
            if form.is_valid():
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/admin')
    else:
        form = LogginginForm()
    args['form'] = form
    return render(request, 'admin/admin.html', args)

#De searchusers functie -> zoekt users aan de hand van ID of naam
def searchusers(request):
    if request.method == 'GET':
        if 'query' in request.GET:
            return searchusersresults(request)
    return render(request, 'admin/searchuser.html')

#De result pagina van de searchusers functie
def searchusersresults(request):
    getUserPar = request.GET['query']
    return render(request, 'admin/searchuser.html', {
        'query' : getUserPar,
    })

#Wat hierboven staat maar dan voor producten
def searchproducts(request):
    if request.method == 'GET':
        if 'query' in request.GET:
            return searchproductresults(request)
    return render(request, 'admin/searchproducts.html')

def searchproductresults(request):
    getProductPar = request.GET['query']
    return render(request, 'admin/searchproducts.html', {
        'query' : getProductPar,
    })

def createuser(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'admin/usercreated.html', {})
    else:
        form = AdminRegistrationForm()
    return render(request, 'admin/createuser.html', {'form' :  form})

#Class based view instead of Function based view
class EditUser(View):
    def get(self, request, userid):
        AddressData = Address.objects.get(customerID=userid)
        UserData = Customers.objects.get(customerID=userid)
        Data = {'address' : AddressData.address, 'number' : AddressData.number, 'city' : AddressData.city, 'postalcode' : AddressData.postalcode, 'name': UserData.name, 'surname': UserData.surname, 'telephone': UserData.telephone, 'isBlocked' : UserData.isBlocked}
        user_form = EditUserForm(initial=Data)
        if request.user.id == int(userid):
            user_form.fields['isBlocked'].disabled = True
        return render(request, 'admin/edituser.html', {
            'userid': userid,
            'user_form': user_form,
        })

    def post(self, request, userid):
        if 'deleteuser' in request.POST:
            deleteUser(request)
            return render(request, 'admin/userdeleted.html', {
                'userid': userid,
            })
        if 'edituser' in request.POST:
            user_form = EditUserForm(request.POST)
            if user_form.is_valid():
                editUser(request, userid)
                return redirect('/admin/searchusers/')
            return render(request, 'admin/edituser.html', {'userid': userid, 'user_form': user_form})


class EditProduct(View):
    def get(self, request, item):
        item = int(item)
        ProductsData = Products.objects.get(prodNum=item)
        ProductDetData = ProductDetails.objects.get(prodNum=Products(item))
        Data = {'prodName': ProductsData.prodName, 'prodStock': ProductsData.prodStock, 'prodPrice': ProductsData.prodPrice,
                'genre': ProductDetData.genre, 'type': ProductDetData.type, 'publisher': ProductDetData.publisher,
                'totalPages': ProductDetData.totalPages, 'language': ProductDetData.language,  'rating': ProductDetData.rating,
                'author': ProductDetData.author,  'desc': ProductDetData.desc, 'imageLink': ProductDetData.imageLink, 'pubDatum': ProductDetData.pubDatum }
        product_form = EditProductForm(initial=Data)
        return render(request, 'admin/editproduct.html', {
            'item': item,
            'product_form': product_form,
        })

    def post(self, request, item):
        if 'deleteproduct' in request.POST:
            deleteProduct(request)
            return render(request, 'admin/productdeleted.html', {
                'item': item,
            })
        if 'editproduct' in request.POST:
            product_form = EditProductForm(request.POST)
            print(product_form)
            if product_form.is_valid():
                editProduct(request, item)
                return render(request, 'admin/productedited.html', {
                'item': item})
            return render(request, 'admin/editproduct.html', {'item': item, 'product_form': product_form})

def createproduct(request):
    if request.method == 'POST':
        form = ProductsRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin/')
    else:
        form = ProductsRegistrationForm()
    return render(request, 'admin/createproduct.html', {'form' :  form})

class ProductGraphSelection(View):
    def get(self, request):

        return render(request, 'admin/dataselection.html', {})

class ProductGraphMonth(View):
    def get(self, request, year, month):
        if Orders.objects.filter(orderDate__year__icontains=int(year), orderDate__month=int(month)).exists():
            ordersInPeriod = Orders.objects.filter(orderDate__year__icontains=int(year), orderDate__month=int(month))
            orders = OrderDetails.objects.all().filter(orderNum__in=ordersInPeriod) \
                .values('productNum') \
                .annotate(amount=Sum('amount')) \
                .order_by('-amount')[:10]

            dataR = []

            for e in orders:
                dataR.append([str(e['productNum']), e['amount']])

            data = [
                ['Product', 'Aantal'],
            ]

            for e in dataR:
                data.append(e)
                print(e)
                print("HIIII")

            for e in data:
                print(e)

            data_source = SimpleDataSource(data)
            chart = gchart.BarChart(data_source, options={'title': "Producten / Aantal verkocht"})

            return render(request, 'admin/productdatamonth.html', {
                'chart' : chart,
                'year' : int(year),
                'month' : int(month),
            })
        return render(request, 'admin/dataselection.html', {
            'warning' : "De combinatie van jaar en maand is niet geldig. Selecteer er één uit de onderstaande lijst."
        })

class Visits(View):
    def get(self, request, from_month=1, to_month=2, from_year=2017, to_year=2018):
        now = datetime.datetime.now()
        thisyear = now.year
        thismonth = now.month
		
        daysinamonth = {1 : 31, 2 : 28, 3 : 31, 4 : 30, 5 : 31, 6 : 30, 7 : 31, 8 : 31, 9 : 30, 10 : 31, 11 : 30, 12 : 31}
		
        chart = None
        month_tostr = None

        thevisits = [['Visits', 'Totaal']]
	
        if Dates.objects.filter(date__year__icontains=thisyear, date__month__icontains=thismonth).exists():
            for i in range(1, daysinamonth[thismonth]):
                if i > now.day:
                    dateobject = Dates.objects.filter(date__year__icontains=thisyear, date__month__icontains=thismonth, date__day__icontains=i)
                    thevisits.append(["{0}-{1}-{2}".format(i, thismonth, thisyear), None])
                else:
                    dateobject = Dates.objects.filter(date__year__icontains=thisyear, date__month__icontains=thismonth, date__day__icontains=i)
                    thevisits.append(["{0}-{1}-{2}".format(i, thismonth, thisyear), dateobject.count()])
		
        thevisits.append(["01-02-2018", None])

        firstmonth = Dates.objects.filter(date__year__icontains=2018, date__month=1)

        secondmonth = Dates.objects.filter(date__year__icontains=2018, date__month=2)
        print("secondmonth: ", secondmonth)

        datelist = []

        cnt = 0
        for e in firstmonth:
            cnt += 1
            datelist.append(e.date)

        cnt2 = 0
        for e in secondmonth:
            cnt2 += 1


            data_source = SimpleDataSource(thevisits)
            chart = gchart.LineChart(data_source, options={'title': "Visits"})
			
            month_tostr = { 1 : "januari", 2 : "februari", 3 : "maart", 4 : "april", 5 : "mei", 6 : "juni", 7 : "juli", 8 : "augustus", 9: "september", 10 : "oktober", 11 : "november", 12 : "december"}


        return render(request, 'admin/visits.html', {
            'chart': chart,
            'year': now.year,
            'month': month_tostr[now.month],
        })

