from os import popen


def parse_getmac():
    request = list(popen('getmac'))
    value1 = f'Физический адрес:\n\n'
    value2 = f'Название устройства:\n\n'
    for i in range(3, len(request)):
        value1 += request[i].split()[0] + ';' '\n'
        if len(request[i].split()) == 2:
            value2 += request[i].split()[1] + ';' '\n'
        else:
            value2 += request[i].split()[1] + ' ' + request[i].split()[2] + ';' '\n'
    return value1, value2

