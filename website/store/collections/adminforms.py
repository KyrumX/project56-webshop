from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models import Max
from ..validators.formvalidators import *

from store.models import Customers, Address, Products, ProductDetails


class AdminRegistrationForm(UserCreationForm):
    firstname = forms.CharField(required=True, label="Voornaam:", min_length=2)
    lastname = forms.CharField(required=True, label="Achternaam:", min_length=2)
    email = forms.EmailField(required=True, label="E-mail:")
    isstaff = forms.BooleanField(required=False, label='Is medewerker:')


    class Meta:
        model = User
        fields = ("firstname", "lastname", "email", "password1", "password2")

    def clean_email(self):
        usernameEmail = self.cleaned_data['email']
        if User.objects.filter(username=usernameEmail).exists():
            raise forms.ValidationError('Dit e-mailadres is al ingebruik, vul een ander e-mailadres in')
        return self.cleaned_data['email']

    def __init__(self, *args, **kwargs):
        super(AdminRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = "Wachtwoord:"
        self.fields['password2'].label = "Herhaling wachtwoord:"
        self.fields[
            'password1'].help_text = "Je wachtwoord moet 8 karakters of langer zijn. Gebruik niet alleen cijfers."
        self.fields['password2'].help_text = "Herhaal het wachtwoord"
        self.error_messages = {
            'password_mismatch': ("Oeps! De twee opgegeven wachtwoorden kwamen niet overeen! Probeer het opnieuw!")
        }

    def save(self, commit=True):
        user = super(AdminRegistrationForm, self).save(commit=False)
        maxID = Customers.objects.all().aggregate(Max('customerID'))
        if maxID.get('customerID__max') == None:
            user.id = 1
        else:
            user.id = maxID.get('customerID__max') + 1

        user.first_name = self.cleaned_data['firstname']
        user.last_name = self.cleaned_data['lastname']
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        user.is_staff = self.cleaned_data['isstaff']

        #Every new User in the Auth table also requires a Customer entity
        newEntryCustomer = Customers(customerID=user.id, email=user.email, name=user.first_name, surname=user.last_name, telephone='nvt', isRegistered=True)
        newEntryCustomer.save()

        #Every Customer requires an Address entity
        newEntryAddress = Address(customerID=Customers(customerID=user.id))
        newEntryAddress.save()

        if commit:
            user.save()

        return user


class ProductsRegistrationForm(ModelForm):
    prodName = forms.CharField(required=True, label="Titel:", max_length=200, min_length=8)
    prodPrice = forms.DecimalField(required=True, label="Prijs:", min_value=1)
    prodStock = forms.IntegerField(required=True, label="Quantiteit:", min_value=1)
    genre = forms.CharField(required=True, label='Genre:', max_length=50, min_length=3)
    type = forms.CharField(required=True, label='Type:', max_length=50, min_length=3)
    publisher = forms.CharField(required=True, label='Uitgever:', max_length=50, min_length=7)
    totalPages = forms.IntegerField(required=True, label='Bladzijden:', min_value=1)
    language = forms.CharField(required=True, label='Taal:', max_length=25, min_length=3)
    rating = forms.IntegerField(required=False, label='Score:', min_value=1, max_value=5)
    author = forms.CharField(required=True, label='Schrijver:', max_length=50, min_length=7)
    desc = forms.CharField(required=True, label='Beschrijving:', min_length=12)
    imageLink = forms.CharField(required=False, label='Foto link:', max_length=300, min_length=8)
    pubDatum = forms.DateField(required=True, label='Uitgeefdatum (Y-M-D):')

    class Meta:
        model = Products
        fields = ("prodName", "prodPrice", "prodStock")

    def clean_prodName(self):
        pass

    def clean_language(self):
        LanguageIn = self.cleaned_data['language']
        language_validator(LanguageIn)
        return self.cleaned_data['language']

    def clean_type(self):
        TypeIn = self.cleaned_data['type']
        typeAndGenre_validator(TypeIn)
        return self.cleaned_data['type']

    def clean_genre(self):
        GenreIn = self.cleaned_data['genre']
        typeAndGenre_validator(GenreIn)
        return self.cleaned_data['genre']

    def save(self, commit=True):
        products = super(ProductsRegistrationForm, self).save(commit=False)
        maxID = Products.objects.all().aggregate(Max('prodNum'))
        if maxID.get('prodNum__max') == None:
            products.id = 1
        else:
            products.id = maxID.get('prodNum__max') + 1

        products.prodName = self.cleaned_data['prodName']
        products.prodPrice = self.cleaned_data['prodPrice']
        products.prodStock = self.cleaned_data['prodStock']
        products.genre = string_validator(self.cleaned_data['genre'])
        products.type = string_validator(self.cleaned_data['type'])
        products.publisher = self.cleaned_data['publisher']
        products.totalPages = self.cleaned_data['totalPages']
        products.language = string_validator(self.cleaned_data['language'])
        products.rating = self.cleaned_data['rating']
        products.author = string_validator(self.cleaned_data['author'])
        products.desc = self.cleaned_data['desc']
        products.imageLink = self.cleaned_data['imageLink']
        products.pubDatum = self.cleaned_data['pubDatum']

        # Data wordt ingevoerd voor het product
        newEntryProducts = Products(prodNum=products.id, prodName=products.prodName, prodPrice=products.prodPrice, prodStock=products.prodStock)
        newEntryProducts.save()

        # Extra data wordt ingevoerd voor het product
        newEntryProductDetails = ProductDetails(prodNum=newEntryProducts, genre=products.genre, type=products.type, publisher=products.publisher, totalPages=products.totalPages, language=products.language, rating=products.rating, author=products.author, desc=products.desc, imageLink=products.imageLink, pubDatum=products.pubDatum)
        newEntryProductDetails.save()

        return products

class EditProductForm(forms.Form):
    prodName = forms.CharField(required=True, label="Titel:", max_length=200)
    prodPrice = forms.DecimalField(required=True, label="Prijs:", min_value=1)
    prodStock = forms.IntegerField(required=True, label="Quantiteit:", min_value=1)
    genre = forms.CharField(required=True, label='Genre:', max_length=50)
    type = forms.CharField(required=True, label='Type:', max_length=50)
    publisher = forms.CharField(required=True, label='Uitgever:', max_length=50)
    totalPages = forms.IntegerField(required=True, label='Bladzijden:', min_value=1)
    language = forms.CharField(required=False, label='Taal:', max_length=25)
    rating = forms.IntegerField(required=False, label='Score:', min_value=1, max_value=5)
    author = forms.CharField(required=True, label='Schrijver:', max_length=50)
    desc = forms.CharField(required=True, label='Beschrijving:')
    imageLink = forms.CharField(required=False, label='Foto link:', max_length=300)
    pubDatum = forms.DateField(required=True, label='Uitgeefdatum (Y-M-D):')

    class Meta:
        model = Products


    def save(self, commit=True):
        products = super(EditProductForm, self).save(commit=False)
        products.prodName = self.cleaned_data['prodName']
        products.prodPrice = self.cleaned_data['prodPrice']
        products.prodStock = self.cleaned_data['prodStock']
        products.genre = self.cleaned_data['genre']
        products.type = self.cleaned_data['type']
        products.publisher = self.cleaned_data['publisher']
        products.totalPages = self.cleaned_data['totalPages']
        products.language = self.cleaned_data['language']
        products.rating = self.cleaned_data['rating']
        products.author = self.cleaned_data['author']
        products.desc = self.cleaned_data['desc']
        products.imageLink = self.cleaned_data['imageLink']
        products.pubDatum = self.cleaned_data['pubDatum']
