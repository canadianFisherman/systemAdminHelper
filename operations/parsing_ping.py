import os
import langdetect


def parse_ping(ip, packets, timeout):
    request = list(os.popen(f'ping {ip} -n {packets} -w {timeout}'))

    if langdetect.detect(request[1]) == 'en':

        if len(request[-1].split()) == 9:

            value = f'Проверка подключения к {ip}\nПакетов отправлено: {request[-3].split()[3].rstrip(",")}\n' \
                    f'Пакетов получено: {request[-3].split()[6].rstrip(",")}\nПакетов потеряно: {request[-3].strip().split()[9]}' \
                    f'\n' \
                    f'Приблизительное время приёма-передачи в мс:\n' \
                    f'Минимальное = {request[-1].split()[2]} Максимальное = {request[-1].split()[5]} Среднее = ' \
                    f'{request[-1].split()[-1]}'

        elif len(request[-1].split()) == 12:
            value = f'Проверка подключения к {ip}\nПакетов отправлено: {request[-1].split()[3].rstrip(",")}\n' \
                    f'Пакетов получено: {request[-1].split()[6].rstrip(",")}\nПакетов потеряно: {request[-1].strip().split()[9]}'

        else:
            value = f'Хоста с таким именем не существует!'

        return value + '\n'

    elif langdetect.detect(request[1]) == 'ru':
        if len(request[-1].split()) == 11:
            value = f'Проверка подключения к {ip}\nПакетов отправлено: {request[-5].split()[3].rstrip(",")}\n' \
                    f'Пакетов получено: {request[-5].split()[6].rstrip(",")}\nПакетов потеряно: {request[-5].strip().split()[9]}' \
                    f'\n' \
                    f'Приблизительное время приёма-передачи в мс:\n' \
                    f'Минимальное = {request[-1].split()[2]} Максимальное = {request[-1].split()[5]} Среднее = ' \
                    f'{request[-1].split()[-1]}'

        elif len(request[-1].split()) == 2:
            value = f'Проверка подключения к {ip}\nПакетов отправлено: {request[-2].split()[3].rstrip(",")}\n' \
                    f'Пакетов получено: {request[-2].split()[6].rstrip(",")}\nПакетов потеряно: {request[-2].strip().split()[9]}'
        else:
            value = f'Хоста с таким именем не существует!'

        return value + '\n'