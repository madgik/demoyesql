import settings as msettings
from bottle import route, run, static_file, request

from bottle import redirect




def executequery(query, bindings=None):
    def latinnum(x):
        x = int(x)
        lx = ""
        while x > 25:
            lx += chr(ord('A') + int(x / 25))
            x %= 25
        lx += chr(ord('A') + x)
        return lx

    query = query.rstrip(';\n\s ')

    try:
        origvars = msettings.madis.functions.variables
        c = msettings.Connection.cursor().execute(query, localbindings=bindings)
        return c
    except Exception as e:
        raise

    # Schema from query's description
    try:
        schema = c.getdescription()
    except:
        c.close()
        msettings.madis.functions.variables = origvars
        self.finish()
        return

    colnames = []
    coltypes = []

    for cname, ctype in schema:
        if ctype == None:
            colnames += [cname]
            coltypes += [ctype]
            continue
        ctypehead3 = ctype.lower()[0:3]
        if ctypehead3 in ('int', 'rea', 'flo', 'dou', 'num'):
            ctype = 'number'
        else:
            ctype = 'string'
        colnames += [cname]
        coltypes += [ctype]

    try:
        firstrow = next(c)
    except StopIteration:
        c.close()
        msettings.madis.functions.variables = origvars
        self.finish()
        return
    except Exception as e:
        c.close()
        msettings.madis.functions.variables = origvars
        self.finish(str(e))
        return

    # Merge with guessed schema from query's first row
    for cname, ctype, i in zip(colnames, coltypes, range(len(colnames))):
        if ctype == None:
            frtype = type(firstrow[i])
            if frtype in (int, float):
                coltypes[i] = 'number'
            else:
                coltypes[i] = 'string'

    # Write responce's header
    response = {"cols": []}
    for name, ctype, num in zip(colnames, coltypes, range(len(colnames))):
        id = latinnum(num)
        response["cols"] += [{"id": id, "label": name, "type": ctype}]

    # Write header
    self.write(json.dumps(response, separators=(',', ':'), sort_keys=True, ensure_ascii=False)[0:-1] + ',"rows":[')

    # Write first line
    response = json.dumps({"c": [{"v": x} for x in firstrow]}, separators=(',', ':'), sort_keys=True,
                          ensure_ascii=False)
    self.write(response)

    self.executequeryrow(c, msettings.madis.functions.variables)
    msettings.madis.functions.variables = origvars









def renderTable(tuples, elapsed_time = 0, lenres = 0):
    printResult = """<style type='text/css'> h1 {color:red;} h2 {color:blue;} p {color:green;} </style>
    <table border = '1' frame = 'above'>"""

    header = '<tr><th>' + '</th><th>'.join([str(x) for x in tuples[0]]) + '</th></tr>'
    data = '<tr>' + '</tr><tr>'.join(
        ['<td>' + '</td><td>'.join([str(y) for y in row]) + '</td>' for row in tuples[1:]]) + '</tr>'

    printResult += header + data + "</table>"
    if elapsed_time != 0:
        printResult += "Query executed in "+ str(elapsed_time) + " seconds and returns "+ str(lenres) + " rows"
    return printResult


import time

@route('/classify')
def classify():
    try:
        start_time = time.time()
        sql = request.query.pubid
        c = executequery(query=sql)
        schema = list(c.getdescription())
        li = list(c)
        lenres = len(li)
        table = [tuple(i[0] for i in schema)]+li
        elapsed_time = time.time() - start_time
        print("time: ", elapsed_time)
        return "<html><body>" + renderTable(table, elapsed_time, lenres) + "</body></html>"
    except Exception as e:
        return "<html><body>" + str(e) + "</body></html>"

    return "<html><body>" + renderTable(table) + "</body></html>"

import os

@route('/classify_plain_sql', method='GET')
def classify_plain_sql():
    upload = request.files.get('topn')

    name, ext = os.path.splitext(upload.filename)
    f = open("udfs.py", "a")
    f.write("\n\n")
    f.write(upload.filename)
    f.close()

    msettings.Connection.createscalarfunction(opname, fobject)
    return "<html><body>" + renderTable(table) + "</body></html>"


@route('/upload', method='POST')
def do_login():
    try:
        import importlib
        from importlib import import_module
        upload     = request.files.get('upload')
        name, ext = os.path.splitext(upload.filename)
        if ext not in ('.py'):
            return 'Upload only .py files'
        f = open(upload.filename,'w')
        raw = upload.file.read()
        f.write(raw.decode())
        f.close()

        module = import_module(name)
        importlib.reload(module)
        from inspect import getmembers, isfunction
        funcs = getmembers(module, isfunction)
        for method in funcs:
            msettings.Connection.createscalarfunction(method[0], method[1])

        return static_file("forms2.html", 'web')
    except Exception as e:
        return "<html><body>" + str(e) + "</body></html>"


@route('/updateweight')
def updateweight():
    class1 = request.query.class1
    subclass = request.query.subclass
    term = request.query.term
    weight = request.query.weight
    table = app.updateweight(class1, subclass, term, weight)
    return "<html><body>" + renderTable(table) + "</body></html>"


@route('/selectTopNauthors')
def selectTopNauthorsWEB():
    class1 = request.query.class1
    n = request.query.n
    table = app.selectTopNauthors(class1, n)
    return "<html><body>" + renderTable(table) + "</body></html>"


@route('/findSimilarArticles')
def findSimilarArticlesWEB():
    aid = request.query.articleId
    topn = request.query.n
    table = app.findSimilarArticles(aid, topn)
    return "<html><body>" + renderTable(table) + "</body></html>"


@route('/moo')
def index():
    import gzip
    import base64
    return gzip.zlib.decompress(base64.decodestring(
        '''eNqNVNtu2zgQfc9XaFWgIa27c0ETalxgiz70oUWx7WIfAkOgJcpkoBsoKpbR5N87lJysnd0ChSBx\nNHNmeOZCptLU1SqVgher1ChTidXfvXDqdsDvZjCmbdJo1qe1MNzJJde9MOAOpgzeuas0mn03bbF3\naq63qtmpwkhwY/fwL4XaSmMVqzTnzQPvHVWAm7vOAXl9idhn1OU7i4tm4Crtc606szp74NrZOOAU\nbT7UojGh3ZBN6vxYvRXmYyWs2P+5/863X3gtyPkc7ZzexevZh6NPbsEf2saI0ZDzZXFO2dlJ+DCv\nFMr/WJbsLI2eubyQ2gFSZxKQM8vDOZsdSodcJBs6uFuzrJi+GpIrVsMfCctGuI5ZtgcZLdkWUNFb\ndQfl0ORGtQ2hP6aEIRt9AdmebQIYmYZdlGlWwGduZFhWbavJJtKUjQkUC83G5SuLl1BUKyCbYExo\nhOIChu6u8JJ1YNc1Ux7Mwv2/oPsFZMUMsivaPDgIIIN7poUZdOOIILlO1eOj8JLr1f375DZ+YlvR\nHOcwdGE39JJMrDRvirYmdLGMY4o1mU1JHHunZtTQJ1ZiBgpiptJMe0vk6VEMTrBFBnD+PmHX9AOv\nyNFuqiRZTw/sYjYG0HcFyypvWvH1IA7j+IqNaUBsJenbtwQp9lKVhlAfKT2L01b+CEiUh6Wqqm9m\nXwlw9XbDSexPT3hBXRs1vXzPcVIE13+J3EzWnS/p7ex4ojsN9uYmv3FRtRF4SL5iDYgF1O2D+N5a\nF/p/ReBhpRoLGD2bwkL52D+1tp4Hw85/YT0F/EV4+ZvhpR2CVxvIow2yvQfbha1wR2xBeSW0Ie63\nvNXi1nG9o4nMqsg2FyuN444ka4Rn+2B2XyxPy3PmvinL+L/14ToneCqyvZ8kc/BeNWTEyHRxhXW+\nOU7/yb+4QIoVYCttr+CCvZzwtpluuaLdncwsHlAc5NeooXuFSZ6OboQ0steFvQvtbfoTFh22jg==\n'''))


@route('/:path')
def callback(path):
    return static_file(path, 'web')


@route('/')
def callback():
    return static_file("index.html", 'web')



run(host='localhost', port=8080)
