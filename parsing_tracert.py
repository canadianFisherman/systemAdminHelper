import os


def parse_tracert(ip, jumps, timeout):

    request = list(os.popen(f'tracert -h {jumps} -w {timeout} {ip}'))
    if len(request) == 1:
        value = 'Хост с таким именем не обнаружен!'
    elif request[2] != '\n':
        value = f'Определяем путь к {ip}\n'
        for i in range(4, request.index('Trace complete.\n')):
            value += request[i].lstrip(' ')
        value += f'Трассировка успешно выполнена.'
    else:
        for i in range(3, request.index('Trace complete.\n')):
            value += request[i].lstrip(' ')
        value += f'Трассировка успешно выполнена.'
    return value
