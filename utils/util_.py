import json
def __str2db_format(self, data):
    '''Convert string data to database format.
    If data is None it returns the 'Null' text,
    otherwise it returns the text surrounded by quotes ensuring internal quotes are escaped.
    '''
    if data==None:
        return 'Null'
    out=str(data)
    if "'" not in out:
        return "'" + out + "'"
    elif '"' not in out:
        return '"' + out + '"'
    else:
        return json.dumps(out)