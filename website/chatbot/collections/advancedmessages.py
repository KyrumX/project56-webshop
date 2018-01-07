from django.utils.timezone import localtime, now

from store.models import Orders, Customers


def hasOrderPlaced(id):
    return Orders.objects.filter(customerID=Customers(id)).exists()

def getLastOrderData(id):
    return Orders.objects.filter(customerID=Customers(id)).order_by('-orderDate').first()

def split(date):
    return date.split("-")

def getDay(date):
    splitted = split(date)
    return splitted[2]

def getYear(date):
    splitted = split(date)
    return splitted[0]

def getMonth(date):
    month = int(split(date)[1])
    if month == 1:
        return "januari"
    elif month == 2:
        return "februari"
    elif month == 3:
        return "maart"
    elif month == 4:
        return "april"
    elif month == 5:
        return "mei"
    elif month == 6:
        return "juni"
    elif month == 7:
        return "juli"
    elif month == 8:
        return "augustus"
    elif month == 9:
        return "september"
    elif month == 10:
        return "oktober"
    elif month == 11:
        return "november"
    else:
        return "december"

def sendableDay(day):
    if day == 'Saturday' or day == 'Sunday':
        return False
    return True

def sendableTime(hour):
    hour = int(hour)
    if hour >= 0 and hour <= 15:
        return True
    else:
        return False

def generate_order_question(order):
    message = "Gaat uw vraag over de bestelling geplaatst op "
    message += str(getDay(str(order.orderDate))) + " " + str(getMonth(str(order.orderDate))) + ", " + str(getYear(str(order.orderDate)))
    message += " met ordernummer "
    message += str(order.orderNum)
    message += "?"
    return message

def generate_order_overview(order):
    message = "Uw bestelling met nummer "
    message += str(order.orderNum)
    message += " geplaatst op "
    message += str(getDay(str(order.orderDate))) + " " + str(getMonth(str(order.orderDate))) + ", " + str(
        getYear(str(order.orderDate)))
    message += " heeft als status "
    status = str(order.orderStatus)
    if status == "Processed" or status == "Verwerkt":
        message += "'Verwerkt'. Dit betekent dat wij uw bestelling en betaling in goede orde hebben ontvangen."
        date = localtime(now())
        canSendDay = sendableDay(date.strftime("%A"))
        canSendTime = sendableTime(date.time().hour)
        if canSendDay and canSendTime:
            message += " Naar verwachting wordt uw bestelling vandaag nog bij onze pakketbezorger aangeboden. Wordt het pakket niet vandaag verzonden? Dan wordt dit waarschijnlijk op de volgende werkdag gedaan."
        else:
            message += "Uw bestelling wordt de eerst volgende werkdag bij onze pakketbezorger aangeboden."
        return message
    else:
        message += "'Wordt verwerkt'. Dit betekent dat wij bezig zijn met het verwerken van uw bestelling. Wanneer de " \
                   "status verandert naar 'Verwerkt' zal de bestelling zo snel mogelijk worden geleverd. Neem voor " \
                   "vragen contact op met onze klantenservice via ons contactform."