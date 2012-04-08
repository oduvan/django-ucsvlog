def json_dump_line(line):
    return '"'+unicode(line).replace('\\','\\\\').replace('\n','\\n').replace('"','\\"')+'"'


def readable_dict(dd):
    if not dd:
        return '{}'
    ret = ''
    for kd,vd in dd.items():
        ret += '\n'+json_dump_line(kd) + ':' + json_dump_line(vd)+','
    return '{'+ret[:-1]+'\n}'

def readable_list(ll):
    return '[' + ','.join(map(json_dump_line,ll)) + ']'