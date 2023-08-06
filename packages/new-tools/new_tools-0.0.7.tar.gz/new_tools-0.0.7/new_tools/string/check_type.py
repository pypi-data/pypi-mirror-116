def check_bool(string=str()):
    if string == True or string.capitalize() == "True" or string.lower() == "true":
        return True
    else:
        return False