from .botmessages import *
from .botcategories import *

def get_type_input(usermessage, case):
    case = int(case)
    if case == 0:
        return get_question_category(usermessage)
    else:
        return get_question_response(usermessage, case)

def get_question_category(usermessage):
    for string in DELIVERY_CATEGORIES:
        if string in usermessage:
            return [DELIVERY_QUESTION, "1"]
    for string in STATUS_CATEGORIES:
        if string in usermessage:
            return [STATUS_QUESTION, "2"]


    for string in PRODUCT_CATEGORIES:
        if string in usermessage:
            return [PRODUCT_QUESTION, "99"]
    return [NOT_FOUND, "0"]

def get_question_response(usermessage, case):
    for string in POSITIVE_ANSWERS:
        if string in usermessage:
            return get_positive_response(usermessage, case)
    else:
        return [DEFAULT_AFTER, "0"]

def get_positive_response(usermessage, case):
    if case == 1:
        return [DELIVERY_RESPONSE, "0"]
    elif case == 2:
        return [STATUS_RESPONSE, "0"]
    elif case == 99:
        return [PRODUCT_RESPONSE, "0"]
