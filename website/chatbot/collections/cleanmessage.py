def clean(message):
    cleaned_string = message.lower()
    cleaned_string = removePunctuation(cleaned_string)
    return cleaned_string

def removePunctuation(message):
    message = removePoint(message)
    message = removeQuestionmarks(message)
    message = removeBrackets(message)
    message = removeComma(message)
    message = removeExclamation(message)
    message = removeMiscellaneous(message)
    return message

def removeQuestionmarks(message):
    return message.replace("?", "")

def removePoint(message):
    return message.replace(".", "")

def removeExclamation(message):
    return message.replace("!", "")

def removeComma(message):
    return message.replace(",", "")

def removeBrackets(message):
    message = message.replace("{", "")
    message = message.replace("}", "")
    message = message.replace("[", "")
    message = message.replace("]", "")
    message = message.replace("(", "")
    message = message.replace(")", "")
    return message

def removeMiscellaneous(message):
    message = message.replace("~", "")
    message = message.replace("@", "")
    message = message.replace("#", "")
    message = message.replace("$", "")
    message = message.replace("%", "")
    message = message.replace("^", "")
    message = message.replace("&", "")
    message = message.replace("*", "")
    message = message.replace("-", "")
    message = message.replace("_", "")
    message = message.replace("+", "")
    message = message.replace("=", "")
    message = message.replace(";", "")
    message = message.replace(":", "")
    message = message.replace("'", "")
    message = message.replace("<", "")
    message = message.replace(">", "")
    message = message.replace("/", "")
    message = message.replace("|", "")
    message = message.replace("`", "")
    return message