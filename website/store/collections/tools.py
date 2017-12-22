def RepresentInt(object):
    try:
        int(object)
        return True
    except ValueError:
        return False

def TransBool(bool):
    if bool == True:
        return "Ja"
    return "Nee"