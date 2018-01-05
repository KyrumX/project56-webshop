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
    punctuation = ["{", "}", "[", "]", "(", ")"]
    for p in punctuation:
        message = message.replace(p, "")
    return message

def removeMiscellaneous(message):
    punctuation = ["~", "@", "#", "$", "%", "^", "&", "*", "-", "_", "+", "=", ";", ":", "'", "<", ">", "/", "|", "`", "lt", "gt"]
    for p in punctuation:
        message = message.replace(p, "")
    return message