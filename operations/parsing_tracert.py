import os


def parse_tracert(ip, jumps, timeout):

    request = list(os.popen(f'tracert -h {jumps} -w {timeout} {ip}'))
    value = ''
    if len(request) == 1:
        value = 'Хост с таким именем не обнаружен!'.encode("cp866").decode("windows-1251")
    else:
        value += f'Определяем путь к {ip}\n'.encode("cp866").decode("windows-1251")
        index_of_enter = request.index('\n', 1, len(request))
        index_of_enter_next = request.index('\n', request.index('\n', 1, len(request)) + 1, len(request))
        for i in range(index_of_enter + 1, index_of_enter_next):
            value += request[i].lstrip(' ')
        value += f'Трассировка успешно выполнена.'.encode("cp866").decode("windows-1251")

    return value