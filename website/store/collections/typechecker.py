def is_type_float(object):
    try:
        float(object)
    except ValueError:
        return False
    return True