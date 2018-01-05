import operator

from chatbot.collections.advancedmessages import hasOrderPlaced, generate_order_question, getLastOrderData, \
    generate_order_overview
from chatbot.collections.cleanmessage import clean
from .botmessages import *
from .botcategories import *

def get_type_input(usermessage, case, request):
    case = int(case)
    cleaned_message = clean(usermessage)
    if case == 0:
        return get_question_category(cleaned_message, case, request)
    else:
        return get_question_response(cleaned_message, case, request)

def get_question_category(usermessage, case, request):
    categories = {
        'international' : 0,
        'delivery' : 0,
        'status' : 0,
        'return' : 0,
        'payment' : 0,
        'contact' : 0,
        'product' : 0,
        'order' : 0,
    }

    for string in INTERNATIONAL_CATEGORIES:
        if string in usermessage:
            categories['international'] += 2

    for string in DELIVERY_CATEGORIES:
        if string in usermessage:
            categories['delivery'] += 2

    for string in STATUS_CATEGORIES:
        if string in usermessage:
            categories['status'] += 2

    for string in RETURN_CATEGORIES:
        if string in usermessage:
            categories['return'] += 2

    for string in PAYMENT_CATEGORIES:
        if string in usermessage:
            categories['payment'] += 2

    for string in CONTACT_CATEGORIES:
        if string in usermessage:
            categories['contact'] += 2

    for string in ORDER_CATEGORIES:
        if string in usermessage:
            categories['order'] += 2

    for string in PRODUCT_CATEGORIES:
        if string in usermessage:
            categories['product'] += 1

    return select_category(categories, usermessage, case, request)

def select_category(categories, usermessage, case, request):
    selected_category = max(categories.keys(), key=(lambda k: categories[k]))
    print(selected_category)
    if categories[selected_category] == 0:
        return [NOT_FOUND, "0"]
    elif selected_category == 'international':
        return [INTERNATIONAL_QUESTION, "11"]
    elif selected_category == 'delivery':
        return [DELIVERY_QUESTION, "1"]
    elif selected_category == 'status':
        return [STATUS_QUESTION, "2"]
    elif selected_category == 'return':
        return [RETURN_QUESTION, "3"]
    elif selected_category == 'payment':
        return [PAYMENT_QUESTION, "4"]
    elif selected_category == 'order':
        return [FIRST_ORDER_RESPONSE, "200"]
    elif selected_category == 'contact':
        return [CONTACT_RESPONSE, "0"]
    elif selected_category == 'product':
        return [PRODUCT_QUESTION, "99"]
    else:
        return [NOT_FOUND, "0"]

def get_question_response(usermessage, case, request):
    for string in POSITIVE_ANSWERS:
        if string in usermessage:
            return get_positive_response(usermessage, case, request)
    if case == 11:
        return [DELIVERY_QUESTION, "1"]
    elif case == -1:
        for string in NEGATIVE_ANSWERS:
            if string in usermessage:
                return [THANKS_RESPONSE, "1"]
            else:
                return get_question_category(usermessage, case, request)
    else:
        return [DEFAULT_AFTER, "0"]

def get_positive_response(usermessage, case, request):
    if case == 1:
        return [DELIVERY_RESPONSE + DEFAULT, "-1"]
    elif case  == -1:
        return [DEFAULT_BEFORE, "0"]
    elif case == 2:
        return [STATUS_RESPONSE + DEFAULT, "-1"]
    elif case == 3:
        return [RETURN_RESPONSE + DEFAULT, "-1"]
    elif case == 4:
        return [PAYMENT_RESPONSE + DEFAULT, "-1"]
    elif case == 99:
        return [PRODUCT_RESPONSE + DEFAULT, "-1"]
    elif case == 11:
        return [INTERNATIONAL_RESPONSE, "111"]
    elif case == 200:
        if request.user.is_authenticated and not hasOrderPlaced(request.user.id):
            return [NO_ORDER_RESPONSE + DEFAULT, "-1"]
        elif not request.user.is_authenticated:
            return [NOT_LOGGED_IN + STATUS_QUESTION, "2"]
        order = getLastOrderData(request.user.id)
        message = generate_order_question(order)
        return [message, "201"]
    elif case == 201:
        order = getLastOrderData(request.user.id)
        message = generate_order_overview(order)
        return [message + DEFAULT, "-1"]