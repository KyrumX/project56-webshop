# make sure this is at the top if it isn't already
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.forms import ModelForm
from django.db.models import Max
from ..validators.formvalidators import *
from ..models import Customers, Address, Products
from ..database.AccountOps import getUserId, isUserBlocked

from django.forms.fields import DateField

#All forms are called in the views

# our new form
class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )

    #Hernoemen van de velden naar nederlands
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label = "Voor- en achternaam:"
        self.fields['contact_email'].label = "E-mailadres:"
        self.fields['content'].label = "Toelichting"


class LogginginForm(AuthenticationForm):
    username = forms.CharField(required=True, label="E-mail")
    password = forms.CharField(required=True, label="Wachtwoord", widget=forms.PasswordInput(render_value=False))

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.fields['password'].label = "Wachtwoord:"
        self.fields['password'].widget.attrs.update({'placeholder': '**********'})
        self.fields['username'].widget.attrs.update({'placeholder': 'deadpool@comicfire.com'})

    def confirm_login_allowed(self, user):
        if isUserBlocked(user.id):
            raise forms.ValidationError(
                self.error_messages['blocked'],
                code='blocked',
            )

    error_messages = {
        'invalid_login': (
            "De combinatie van e-mail en wachtwoord is niet correct. "
            "Let erop dat zowel e-mail als het wachtwoord hoofdletter gevoelig is."
        ),
        'blocked': (
            "Dit account is geblokkeerd. "
            "Als u denkt dat dit een fout is, neem dan contact op via de contact pagina."
        ),
    }

    # Geef een error wanneer inloggegevens niet overeen komen
    # def clean(self):
    #     print("Running...")
    #     username = self.cleaned_data['username']
    #     password = self.cleaned_data['password']
    #     try:
    #         User.objects.get(username=username, password=password)
    #     except User.DoesNotExist:
    #         raise forms.ValidationError("Het email en wachtwoord komen niet overeen")
    #     return self.cleaned_data

    # def clean_username(self):
    #     print("HELLOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    #     username = self.cleaned_data['username']
    #     print(isUserBlocked(getUserId(username)))
    #     if isUserBlocked(getUserId(username)):
    #         forms.ValidationError("ERROR")
    #     else:
    #         return self.cleaned_data

#Regestratie form, we geven een django UserCreationForm mee als attribuut die we dan kunnen aanpassen
class RegistrationForm(UserCreationForm):
    firstname = forms.CharField(required=True, label="Voornaam:")
    lastname = forms.CharField(required=True, label="Achternaam:")
    email = forms.EmailField(required=True, label="E-mail:")

    #Welke velden de form moet hebben
    class Meta:
        model = User
        fields = ("firstname", "lastname", "email", "password1", "password2")

    def clean_email(self):
        if User.objects.filter(username=self.cleaned_data['email']).exists():
            raise forms.ValidationError('Dit e-mailadres is al ingebruik, vul een ander e-mailadres in')
        return self.cleaned_data['email']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = "Wachtwoord:"
        self.fields['password2'].label = "Herhaling wachtwoord:"
        self.fields['password1'].help_text = "Je wachtwoord moet 8 karakters of langer zijn. Gebruik niet alleen cijfers."
        self.fields['password2'].help_text = "Herhaal het wachtwoord"
        self.error_messages = {
            'password_mismatch': ("Oeps! De twee opgegeven wachtwoorden kwamen niet overeen! Probeer het opnieuw!"),
        }

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        maxID = Customers.objects.all().aggregate(Max('customerID'))
        if maxID.get('customerID__max') == None:
            user.id = 1
        else:
            user.id = maxID.get('customerID__max') + 1

        user.first_name = self.cleaned_data['firstname']
        user.last_name = self.cleaned_data['lastname']
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']


        #Maak voor elke AUTH ook een customer aan met het zelfde ID
        customerEntry = Customers(customerID=user.id, email=user.email, name=user.first_name, surname=user.last_name,
                                  telephone='nvt', isRegistered=True)
        customerEntry.save()

        #Maak voor elke Customer ook een default address
        customerAddress = Address(customerID=Customers(customerID=user.id))
        customerAddress.save()


        if commit:
            user.save()

        return user


#Regestratie form voor producten, we geven een django ModelForm mee als attribuut die we dan kunnen aanpassen
class PRegistrationForm(ModelForm):
    prodName = forms.CharField(required=True, label="Titel:")
    prodPrice = forms.DecimalField(required=True, label="Prijs:")
    prodStock = forms.IntegerField(required=True, label="Quantiteit:")
    genre = forms.CharField(required=True, label='Genre:')
    type = forms.CharField(required=True, label='Type:')
    publisher = forms.CharField(required=True, label='Uitgever:')
    totalPages = forms.IntegerField(required=True, label='Bladzijden:')
    language = forms.CharField(required=False, label='Taal:')
    rating = forms.IntegerField(required=False, label='Score:')
    author = forms.CharField(required=True, label='Schrijver:')
    desc = forms.CharField(required=True, label='Beschrijving:')
    imageLink = forms.FileField(required=False, label='Foto:')
    pubDatum = forms.DateField(required=True, label='Uitgeefdatum:')

    class Meta:
        model = Products
        fields = ("prodName", "prodPrice", "prodStock")

    def save(self, commit=True):
        products = super(PRegistrationForm, self).save(commit=False)
        maxID = products.objects.all().aggregate(Max('prodNum'))
        if maxID.get('prodNum__max') == None:
            products.id = 1
        else:
            products.id = maxID.get('prodNum__max') + 1

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

        # Data wordt ingevoerd voor het product
        ProductsEntry = Products(prodNum=products.id, prodName=products.prodName, prodPrice=products.prodPrice,
                                    prodStock=products.prodStock)
        ProductsEntry.save()

        # Extra data wordt ingevoerd voor het product
        ProdData = ProductDetails(prodNum=products(prodNum=products.id), genre=products.genre,
                                                type=products.type, publisher=products.publisher,
                                                totalPages=products.totalPages, language=products.language,
                                                rating=products.rating, author=products.author, desc=products.desc,
                                                imageLink=products.imageLink, pubDatum=products.pubDatum)
        ProdData.save()

        if commit:
            products.save()

        return products

class CustomerDetails(forms.Form):
    customer_fname = forms.CharField(required=True, max_length=50)
    customer_lname = forms.CharField(required=True, max_length=50)
    customer_email = forms.EmailField(required=True, max_length=100)
    customer_phone = forms.CharField(required=False, max_length=12)
    customer_address = forms.CharField(required=True, max_length=100)
    customer_adressnum = forms.CharField(required=True, max_length=10)
    customer_city = forms.CharField(required=True, max_length=25)
    customer_postalcode = forms.CharField(required=True)

    #Nakijken of de postcode uit 4 cijfers en 2 leters bestaat
    def clean_customer_postalcode(self):
        CustomerpostalCodeIn = self.cleaned_data['customer_postalcode']
        postalcode_validator(CustomerpostalCodeIn)
        return self.cleaned_data['customer_postalcode']

    #Nakijken of het telefoonnummer bestaat uit 8 of 10 cijfers
    def clean_customer_phone(self):
        CustomertelephoneIn = self.cleaned_data['customer_phone']
        telephone_validator(CustomertelephoneIn)
        return self.cleaned_data['customer_phone']

    def clean_customer_city(self):
        CustomerCityIn = self.cleaned_data['customer_city']
        string_validator(CustomerCityIn)
        return self.cleaned_data['customer_city']

    def clean_customer_address(self):
        CustomerAddressIn = self.cleaned_data['customer_address']
        string_validator(CustomerAddressIn)
        return self.cleaned_data['customer_address']


    def __init__(self, *args, **kwargs):
        super(CustomerDetails, self).__init__(*args, **kwargs)
        self.fields['customer_fname'].label = "Voornaam:"
        self.fields['customer_lname'].label = "Achternaam:"
        self.fields['customer_email'].label = "E-mailadres:"
        self.fields['customer_phone'].label = "Telefoonnummer"
        self.fields['customer_address'].label = "Adres:"
        self.fields['customer_adressnum'].label = "Huisnummer en eventule toevoeging:"
        self.fields['customer_city'].label = "Stad:"
        self.fields['customer_postalcode'].label = "Postcode:"

		
class ReadOnlyText(forms.TextInput):
  input_type = 'text'

  def render(self, name, value, attrs=None):
     if value is None: 
         value = ''
     return value		

class CheckoutForm(forms.Form):

    card_name = forms.CharField(required=True)
    card_number = forms.IntegerField(required=True)
    card_edm = forms.IntegerField(required=True, max_value=12, min_value=1)
    card_edy = forms.IntegerField(required=True, max_value=2030, min_value=2017)
    card_CVC = forms.IntegerField(required=True)

    def __init__(self, *args, **kwargs):
        if 'label_suffix' not in kwargs:
            kwargs['label_suffix'] = ''
        super(CheckoutForm, self).__init__(*args, **kwargs)
        self.fields['card_name'].label = "Naam op de kaart:"
        self.fields['card_number'].label = "Kaartnummer:"
        #self.fields['card_number'].help_text = "De cijfers op de voorzijde van uw kaart."
        self.fields['card_edy'].label = ""
        self.fields['card_edm'].label = "Verval datum (mm-jj):"
        self.fields['card_CVC'].label = "CVC/CID:"
        self.fields['card_edy'].label = "-"

    #Nakijken van kaart gegevens
    def clean_card_number(self):
        card_numberIn = self.cleaned_data['card_number']
        creditcard_validator(card_numberIn, 16)
        return self.cleaned_data['card_number']

    def clean_card_CVC(self):
        card_cvcIn = self.cleaned_data['card_CVC']
        creditcard_validator(card_cvcIn, 3)
        return self.cleaned_data['card_CVC']



class AccountForm(forms.ModelForm):
    address = forms.CharField(required=True, max_length=100)
    number = forms.CharField(required=True, max_length=10)
    city = forms.CharField(required=True, max_length=25)
    postalcode = forms.CharField(required=True)


    def clean_postalcode(self):
        postalCodeIn = self.cleaned_data['postalcode']
        postalcode_validator(postalCodeIn)
        return self.cleaned_data['postalcode']

    def clean_city(self):
        cityIn = self.cleaned_data['city']
        string_validator(cityIn)
        return self.cleaned_data['city']

    def clean_address(self):
        addressIn = self.cleaned_data['address']
        string_validator(addressIn)
        return self.cleaned_data['address']

    class Meta:
        model = Address
        fields=(
            'address',
            'number',
            'city',
            'postalcode',
        )

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        self.fields['address'].label = "Adres:"
        self.fields['number'].label = "Huisnummer:"
        self.fields['city'].label = "Stad:"
        self.fields['postalcode'].label = "Postcode:"


class CustomerInfoForm(forms.Form):

    name = forms.CharField(required=True, max_length=50)
    surname = forms.CharField(required=True, max_length=50)
    telephone = forms.CharField(required=False)

    class Meta:
        model = Customers
        fields = (
            'name',
            'surname',
            'telephone',
        )

    def clean_telephone(self):
        telephoneIn = self.cleaned_data['telephone']
        telephone_validator(telephoneIn)
        return self.cleaned_data['telephone']


    def __init__(self, *args, **kwargs):
        super(CustomerInfoForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Voornaam:"
        self.fields['surname'].label = "Achternaam:"
        self.fields['telephone'].label = "Telefoonnummer:"


class PasswordForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(PasswordForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = "Oud wachtwoord:"
        self.fields['new_password1'].label = "Nieuw wachtwoord:"
        self.fields['new_password2'].label = "Herhaal nieuw wachtwoord:"
        self.fields[
            'new_password1'].help_text = "Je wachtwoord moet 8 karakters of langer zijn. Gebruik niet alleen cijfers."
        self.fields['new_password2'].help_text = "Herhaal het wachtwoord"
        self.error_messages = {
            'password_mismatch': ("Oeps! De twee opgegeven wachtwoorden kwamen niet overeen! Probeer het opnieuw!"),
        }