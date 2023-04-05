import sys
from datetime import datetime
import time
import os
import ipaddress
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QTextEdit, QPushButton, QGridLayout, QLineEdit, \
    QPlainTextEdit, QTreeWidgetItem, QDialog, QRadioButton
from PyQt6.uic import loadUi
from operations.parsing_ipconfig import devices
from operations.parsing_ping import parse_ping
from operations.parsing_tracert import parse_tracert
from operations.parsing_getmac import parse_getmac


# noinspection PyUnresolvedReferences
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('../SystemAdminHelper/windows/main.ui', self)
        self.pb_ipconfig.clicked.connect(self.show_ipconfig)
        self.pb_ping.clicked.connect(self.show_pingDialog)
        self.pb_tracer.clicked.connect(self.show_tracertDialog)
        self.pb_getmac.clicked.connect(self.show_getmac)

    def show_ipconfig(self):
        ipconfig.show()
        for k, v in devices.items():
            value = QTreeWidgetItem(ipconfig.treeWidget)
            value.setText(0, k.encode("windows-1251").decode("cp866"))

            for s in v:
                value1 = QTreeWidgetItem(value)
                value1.setText(0, s)
                value.addChild(value1)
            with open(f'log/ipconfig {datetime.now().strftime("%H-%M, %m-%d-%Y")}.txt', 'a',
                      encoding='utf-8') as file:
                file.write(f'{k.encode("windows-1251").decode("cp866")}: {v}\n')

    def show_pingDialog(self):
        pingDialog.show()

    def show_tracertDialog(self):
        tracertDialog.show()

    def show_getmac(self):
        getmac.show()
        with open(f'log/getmac {datetime.now().strftime("%H-%M, %m-%d-%Y")}.txt', 'w',
                  encoding='utf-8') as file:
            file.write(getmac.value[0] + '\n' + getmac.value[1])

# noinspection PyUnresolvedReferences
class Ipconfig(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('../SystemAdminHelper/windows/ipconfig.ui', self)




class ErrorDialog(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('../SystemAdminHelper/windows/errorDialog.ui', self)
        self.pushButton.clicked.connect(self.close_window)

    def close_window(self):
        self.close()


# noinspection PyUnresolvedReferences
class PingDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.current_rb = ''

        loadUi('../SystemAdminHelper/windows/inputForPing.ui', self)
        self.pb_OK.clicked.connect(self.run)

        self.rb_ip.toggled.connect(self.IP_clicked)

        self.rb_link.toggled.connect(self.link_clicked)

        self.rb_range.toggled.connect(self.range_clicked)

    def run(self):
        if self.current_rb == 'IP':
            if self.check_IP():
                values = self.check_IP()
                ping.show()
                ping.plainTextEdit.setReadOnly(True)
                # ping.plainTextEdit.setPlainText('Загрузка')
                req = parse_ping(values[0], values[1], values[2])
                ping.plainTextEdit.setPlainText(req)

                with open(f'log/ping {datetime.now().strftime("%H-%M, %m-%d-%Y")}.txt', 'w', encoding='utf-8') as file:
                    file.write(req)

            else:
                errorDialog.show()

        elif self.current_rb == 'Link':
            if self.check_link():
                values = self.check_link()
                ping.show()
                ping.plainTextEdit.setReadOnly(True)
                # ping.plainTextEdit.setPlainText('Загрузка')
                req = parse_ping(values[0], values[1], values[2])
                ping.plainTextEdit.setPlainText(req)

                with open(f'log/ping {datetime.now().strftime("%H-%M, %m-%d-%Y")}.txt', 'w', encoding='utf-8') as file:
                    file.write(req)

            else:
                errorDialog.show()

        elif self.current_rb == 'Range':
            if self.check_range():
                values = self.check_range()
                value = ''
                for i in range(int(values[0][0].split('.')[-1]), int(values[0][1].split('.')[-1]) + 1):
                    ip = ''
                    for j in range(len(values[0][0].split('.')) - 1):
                        ip += values[0][0].split('.')[j] + '.'
                    ip += str(i)
                    ping.show()
                    ping.plainTextEdit.setReadOnly(True)
                    # ping.plainTextEdit.setPlainText('Загрузка')
                    value += '\n'
                    value += parse_ping(ip, values[1], values[2])
                ping.plainTextEdit.setPlainText(value)

                with open(f'log/ping {datetime.now().strftime("%H-%M, %m-%d-%Y")}.txt', 'w', encoding='utf-8') as file:
                    file.write(value)
            else:
                errorDialog.show()

    def check_IP(self):

        try:
            ipaddress.ip_address(self.le_ip.text())
        except ValueError:
            return False
        else:
            ip_address = self.le_ip.text()
            if self.le_packets.text() == '':
                packets = '4'
            elif self.le_packets.text().isnumeric() and int(self.le_packets.text()) > 0:
                packets = self.le_packets.text()
            else:
                return False

            if self.le_timeout.text() == '':
                timeout = '4'
            elif self.le_timeout.text().isnumeric() and int(self.le_timeout.text()) > 0:
                timeout = self.le_timeout.text()
            else:
                return False
            return ip_address, packets, timeout

    def check_link(self):
        if not self.le_ip.text().isnumeric():
            ip_address = self.le_ip.text()
        else:
            return False

        if self.le_packets.text() == '':
            packets = '4'
        elif self.le_packets.text().isnumeric() and int(self.le_packets.text()) > 0:
            packets = self.le_packets.text()
        else:
            return False

        if self.le_timeout.text() == '':
            timeout = '4'
        elif self.le_timeout.text().isnumeric() and int(self.le_timeout.text()) > 0:
            timeout = self.le_timeout.text()
        else:
            return False
        return ip_address, packets, timeout

    def check_range(self):
        try:
            ipaddress.ip_address(self.le_ip.text().split()[0])
            ipaddress.ip_address(self.le_ip.text().split()[1])
        except ValueError:
            return False
        else:
            ip_address = [self.le_ip.text().split()[0], self.le_ip.text().split()[1]]
            if self.le_packets.text() == '':
                packets = '4'
            elif self.le_packets.text().isnumeric() and int(self.le_packets.text()) > 0:
                packets = self.le_packets.text()
            else:
                return False

            if self.le_timeout.text() == '':
                timeout = '4'
            elif self.le_timeout.text().isnumeric() and int(self.le_timeout.text()) > 0:
                timeout = self.le_timeout.text()
            else:
                return False
            return ip_address, packets, timeout

    def IP_clicked(self):
        self.current_rb = 'IP'
        pingDialog.le_ip.setPlaceholderText('')

    def link_clicked(self):
        self.current_rb = 'Link'
        pingDialog.le_ip.setPlaceholderText('')

    def range_clicked(self):
        self.current_rb = 'Range'
        pingDialog.le_ip.setPlaceholderText('Введите два IP-адреса через пробел')


class Ping(QWidget):

    def __init__(self):
        super().__init__()
        loadUi('../SystemAdminHelper/windows/ping.ui', self)


class TracertDialog(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('../SystemAdminHelper/windows/inputForTracert.ui', self)
        self.current_rb = ''

        self.pb_OK.clicked.connect(self.run)

        self.rb_ip.toggled.connect(self.IP_clicked)

        self.rb_link.toggled.connect(self.link_clicked)

        self.rb_range.toggled.connect(self.range_clicked)

    def run(self):
        if self.current_rb == 'IP':
            if self.check_IP():
                values = self.check_IP()
                tracert.show()
                tracert.plainTextEdit.setPlainText('Загрузка')
                # time.sleep(5000)
                req = parse_tracert(values[0], values[1], values[2])
                ping.plainTextEdit.setPlainText(req)

                with open(f'log/tracert {datetime.now().strftime("%H-%M, %m-%d-%Y")}.txt', 'w',
                          encoding='utf-8') as file:
                    file.write(req)

            else:
                errorDialog.show()

        elif self.current_rb == 'Link':
            if self.check_link():
                values = self.check_link()
                tracert.show()
                tracert.plainTextEdit.setReadOnly(True)
                # ping.plainTextEdit.setPlainText('Загрузка')
                req = parse_tracert(values[0], values[1], values[2])
                ping.plainTextEdit.setPlainText(req)

                with open(f'log/tracert {datetime.now().strftime("%H-%M, %m-%d-%Y")}.txt', 'w',
                          encoding='utf-8') as file:
                    file.write(req)
            else:
                errorDialog.show()

        elif self.current_rb == 'Range':
            if self.check_range():
                values = self.check_range()
                value = ''
                for i in range(int(values[0][0].split('.')[-1]), int(values[0][1].split('.')[-1]) + 1):
                    ip = ''
                    for j in range(len(values[0][0].split('.')) - 1):
                        ip += values[0][0].split('.')[j] + '.'
                    ip += str(i)
                    tracert.show()
                    tracert.plainTextEdit.setReadOnly(True)
                    value += '\n'
                    value += parse_tracert(ip, values[1], values[2])
                tracert.plainTextEdit.setPlainText(value)
                with open(f'log/tracert {datetime.now().strftime("%H-%M, %m-%d-%Y")}.txt', 'w',
                          encoding='utf-8') as file:
                    file.write(value)
            else:
                errorDialog.show()

    def check_IP(self):

        try:
            ipaddress.ip_address(self.le_ip.text())
        except ValueError:
            return False
        else:
            ip_address = self.le_ip.text()
            if self.le_jumps.text() == '':
                jumps = '30'
            elif self.le_jumps.text().isnumeric() and int(self.le_jumps.text()) > 0:
                jumps = self.le_jumps.text()
            else:
                return False

            if self.le_timeout.text() == '':
                timeout = '4000'
            elif self.le_timeout.text().isnumeric() and int(self.le_timeout.text()) > 0:
                timeout = self.le_timeout.text()
            else:
                return False
            return ip_address, jumps, timeout

    def check_link(self):
        if not self.le_ip.text().isnumeric():
            ip_address = self.le_ip.text()
        else:
            return False

        if self.le_jumps.text() == '':
            jumps = '30'
        elif self.le_jumps.text().isnumeric() and int(self.le_jumps.text()) > 0:
            jumps = self.le_jumps.text()
        else:
            return False

        if self.le_timeout.text() == '':
            timeout = '4000'
        elif self.le_timeout.text().isnumeric() and int(self.le_timeout.text()) > 0:
            timeout = self.le_timeout.text()
        else:
            return False
        return ip_address, jumps, timeout

    def check_range(self):
        try:
            ipaddress.ip_address(self.le_ip.text().split()[0])
            ipaddress.ip_address(self.le_ip.text().split()[1])
        except ValueError:
            return False
        else:
            ip_address = [self.le_ip.text().split()[0], self.le_ip.text().split()[1]]
            if self.le_jumps.text() == '':
                jumps = '30'
            elif self.le_jumps.text().isnumeric() and int(self.le_jumps.text()) > 0:
                jumps = self.le_jumps.text()
            else:
                return False

            if self.le_timeout.text() == '':
                timeout = '4000'
            elif self.le_timeout.text().isnumeric() and int(self.le_timeout.text()) > 0:
                timeout = self.le_timeout.text()
            else:
                return False
            return ip_address, jumps, timeout

    def IP_clicked(self):
        self.current_rb = 'IP'
        pingDialog.le_ip.setPlaceholderText('')

    def link_clicked(self):
        self.current_rb = 'Link'
        pingDialog.le_ip.setPlaceholderText('')

    def range_clicked(self):
        self.current_rb = 'Range'
        pingDialog.le_ip.setPlaceholderText('Введите два IP-адреса через пробел')


class Tracert(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('../SystemAdminHelper/windows/tracert.ui', self)


class Getmac(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('../SystemAdminHelper/windows/getmac.ui', self)
        self.plainTextEdit.setReadOnly(True)
        self.value = parse_getmac()
        self.plainTextEdit.setPlainText(self.value[0])
        self.plainTextEdit_2.setPlainText(self.value[1])



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    ipconfig = Ipconfig()
    mainWindow.show()
    pingDialog = PingDialog()
    errorDialog = ErrorDialog()
    ping = Ping()
    tracertDialog = TracertDialog()
    tracert = Tracert()
    getmac = Getmac()
    try:
        sys.exit(app.exec())
    except SystemExit:
        print(os.path.dirname(sys.argv[0]))
        print('Закрытие приложения')
