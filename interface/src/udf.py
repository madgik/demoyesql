import re
def regexprmatch(*args):
    a=re.search(args[0], str(args[1]),re.UNICODE)
    if a!=None:
        return True
    else:
        return False
        