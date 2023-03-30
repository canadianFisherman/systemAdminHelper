import os
request = list(os.popen('ipconfig'))
devices = {}

for i in range(len(request) - 1):
    try:
        if request[i][-2] == ':':
            name = str(request[i]).rstrip(':\n')
            details = []
            j = i + 2

            while j < len(request) and request[j] != '\n':
                details.append(str(request[j]).rstrip('\n'))
                j += 1
            devices.update({name: details})

    except IndexError:
        pass


