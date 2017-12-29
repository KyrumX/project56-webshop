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
    for string in INTERNATIONAL_CATEGORIES:
        if string in usermessage:
            return [INTERNATIONAL_QUESTION, "11"]

    for string in DELIVERY_CATEGORIES:
        if string in usermessage:
            return [DELIVERY_QUESTION, "1"]

    for string in STATUS_CATEGORIES:
        if string in usermessage:
            return [STATUS_QUESTION, "2"]

    for string in RETURN_CATEGORIES:
        if string in usermessage:
            return [RETURN_QUESTION, "3"]

    for string in PAYMENT_CATEGORIES:
        if string in usermessage:
            return [PAYMENT_QUESTION, "4"]

    for string in PRODUCT_CATEGORIES:
        if string in usermessage:
            return [PRODUCT_QUESTION, "99"]
    return [NOT_FOUND, "0"]

def get_question_response(usermessage, case):
    for string in POSITIVE_ANSWERS:
        if string in usermessage:
            return get_positive_response(usermessage, case)
    if case == 11:
        return [DELIVERY_QUESTION, "1"]
    elif case == -1:
        return [THANKS_RESPONSE, "0"]
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