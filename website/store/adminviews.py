import datetime
from django.db.models import Sum, Avg
from django.shortcuts import render, redirect
from graphos.renderers import gchart
from graphos.sources.simple import SimpleDataSource
from graphos.sources.model import ModelDataSource
from store.collections.adminforms import AdminRegistrationForm, ProductsRegistrationForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import OrderDetails, Dates, UserVisits

#Admin index - comicfire.com/admin/
from django.views import View

from store.database.adminGetData import ifUserExists
from django.contrib.auth import login, logout, update_session_auth_hash
from .collections.tools import *
from .collections.forms import *
from .database.AccountOps import *
from .collections.posts import *
from django.contrib.auth import authenticate

def admin(request):
    args = {}
    if request.method == "POST":
        print(request.POST)
        if 'loginbutton' in request.POST:
            form = LogginginForm(request.POST)
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

def createuser(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin/')
    else:
        form = AdminRegistrationForm()
    return render(request, 'admin/createuser.html', {'form' :  form})

#Class based view instead of Function based view
class EditUser(View):
    def get(self, request, userid):
        AddressData = Address.objects.get(customerID=userid)
        UserData = Customers.objects.get(customerID=userid)
        Data = {'address' : AddressData.address, 'number' : AddressData.number, 'city' : AddressData.city, 'postalcode' : AddressData.postalcode, 'name': UserData.name, 'surname': UserData.surname, 'telephone': UserData.telephone}
        user_form = EditUserForm(initial=Data)
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
            print(user_form)
            if user_form.is_valid():
                editUser(request, userid)
                return redirect('/admin/searchusers/')
            return render(request, 'admin/edituser.html', {'userid': userid, 'user_form': user_form})

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

        return render(request, 'admin/productdataselection.html', {})

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
        return render(request, 'admin/productdataselection.html', {
            'warning' : "De combinatie van jaar en maand is niet geldig. Selecteer er één uit de onderstaande lijst."
        })

class Visits(View):
    def get(self, request, from_month=1, to_month=2, from_year=2017, to_year=2018):
        now = datetime.datetime.now()
        thisyear = now.year
        thismonth = now.month
		
        daysinamonth = {1 : 31, 2 : 28, 3 : 31, 4 : 30, 5 : 31, 6 : 30, 7 : 31, 8 : 31, 9 : 30, 10 : 31, 11 : 30, 12 : 31}
		
        #if from_year < 2018:
         #   from_year = 2018
        #elif to_year > now.year or to_year >= now.year and to_month > now.month:
         #   to_year = now.year
         #   to_month = now.month

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
            print("incoming")
            print(e.date)

            data = [
                ['Visits', 'Aantal'],
                ['01-01-2018', cnt],
                ['01-02-2018', cnt2],
            ]


            data_source = SimpleDataSource(thevisits)
            chart = gchart.LineChart(data_source, options={'title': "Visits"})
			
            month_tostr = { 1 : "Januari", 2 : "Februari", 3 : "Maart", 4 : "April", 5 : "Mei", 6 : "Juni", 7 : "Juli", 8 : "Augustus", 9: "September", 10 : "Oktober", 11 : "November", 12 : "December"}

            return render(request, 'admin/visits.html', {
                'chart' : chart,
                'year' : now.year,
                'month' : month_tostr[now.month],
            })
        return render(request, 'admin/productdataselection.html', {
            'warning' : "De combinatie van jaar en maand is niet geldig. Selecteer er één uit de onderstaande lijst."
        })