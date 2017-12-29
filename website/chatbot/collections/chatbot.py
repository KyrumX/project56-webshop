import operator

from .botmessages import *
from .botcategories import *

def get_type_input(usermessage, case):
    case = int(case)
    usermessage = usermessage.lower()
    if case == 0:
        return get_question_category(usermessage, case)
    else:
        return get_question_response(usermessage, case)

def get_question_category(usermessage, case):
    categories = {
        'international' : 0,
        'delivery' : 0,
        'status' : 0,
        'return' : 0,
        'payment' : 0,
        'contact' : 0,
        'product' : 0,

    }

    for string in INTERNATIONAL_CATEGORIES:
        if string in usermessage:
            categories['international'] += 2
            #return [INTERNATIONAL_QUESTION, "11"]

    for string in DELIVERY_CATEGORIES:
        if string in usermessage:
            categories['delivery'] += 2
            #return [DELIVERY_QUESTION, "1"]

    for string in STATUS_CATEGORIES:
        if string in usermessage:
            categories['status'] += 2
            #return [STATUS_QUESTION, "2"]

    for string in RETURN_CATEGORIES:
        if string in usermessage:
            categories['return'] += 2
            #return [RETURN_QUESTION, "3"]

    for string in PAYMENT_CATEGORIES:
        if string in usermessage:
            categories['payment'] += 2
            #return [PAYMENT_QUESTION, "4"]

    for string in CONTACT_CATEGORIES:
        if string in usermessage:
            categories['contact'] += 2
            #return [CONTACT_RESPONSE, "0"]

    for string in PRODUCT_CATEGORIES:
        if string in usermessage:
            categories['product'] += 1
            #return [PRODUCT_QUESTION, "99"]

    return select_category(categories, usermessage, case)

def select_category(categories, usermessage, case):
    selected_category = max(categories.keys(), key=(lambda k: categories[k]))
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
    elif selected_category == 'contact':
        return [CONTACT_RESPONSE, "0"]
    elif selected_category == 'product':
        return [PRODUCT_QUESTION, "99"]
    else:
        return [NOT_FOUND, "0"]

def get_question_response(usermessage, case):
    for string in POSITIVE_ANSWERS:
        if string in usermessage:
            return get_positive_response(usermessage, case)
    if case == 11:
        return [DELIVERY_QUESTION, "1"]
    elif case == -1:
        for string in NEGATIVE_ANSWERS:
            if string in usermessage:
                return [DELIVERY_QUESTION, "1"]
            else:
                return get_question_category(usermessage, case)
    else:
        return [DEFAULT_AFTER, "0"]

def get_positive_response(usermessage, case):
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