import os


def parse_nslookup(domen):
    request = list(os.popen(f'Nslookup {domen}'))
    if len(request) == 3:
        return 'Домен не найден'.encode("cp866").decode("windows-1251")
    else:
        value = f'Данные о машине:\n' \
                f'Сервер: {request[0][request[0].index(":") + 3:]}\n' \
                f'Адрес: {request[1][request[1].index(":") + 3:]}\n' \
                f'Данные о домене:\n' \
                f'Название: {domen}\n'.encode("cp866").decode("windows-1251")
        addresses = f'{request[4][request[4].index(":"):]}\n'
        for i in range(5, len(request)):
            addresses += request[i] + '\n'
        value += f'Адреса: {addresses}'.encode("cp866").decode("windows-1251")
        return value
