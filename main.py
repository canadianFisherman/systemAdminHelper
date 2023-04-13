import sys
from datetime import datetime
import time
import os
import ipaddress
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QTextEdit, QPushButton, QGridLayout, QLineEdit, \
    QPlainTextEdit, QTreeWidgetItem, QDialog, QRadioButton
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent

from operations.parsing_ipconfig import devices
from operations.parsing_ping import parse_ping
from operations.parsing_tracert import parse_tracert
from operations.parsing_getmac import parse_getmac
from operations.parsing_nslookup import parse_nslookup
from operations.parsing_netstat import parse_netstat


# noinspection PyUnresolvedReferences
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('../SystemAdminHelper/windows/main.ui', self)

        self.setWindowIcon(QIcon('../SystemAdminHelper/windows/computer-support.png'))

        self.pb_ipconfig.clicked.connect(self.show_ipconfig)
        self.pb_ping.clicked.connect(self.show_pingDialog)
        self.pb_tracer.clicked.connect(self.show_tracertDialog)
        self.pb_getmac.clicked.connect(self.show_getmac)
        self.pb_nslookup.clicked.connect(self.show_nslookupDialog)
        self.pb_netstat.clicked.connect(self.show_netstat)
        self.pb_author.clicked.connect(self.show_author)

    def show_ipconfig(self):
        ipconfig.show()
        for k, v in devices.items():
            value = QTreeWidgetItem(ipconfig.treeWidget)
            value.setText(0, k.encode("windows-1251").decode("cp866"))

            for s in v:
                value1 = QTreeWidgetItem(value)
                value1.setText(0, s.encode("windows-1251").decode("cp866"))
                value.addChild(value1)
            with open(f'log/ipconfig {datetime.now().strftime("%H-%M, %m-%d-%Y")}.txt', 'a',
                      encoding='utf-8') as file:
                file.write(f'{k.encode("windows-1251").decode("cp866")}: {v}\n')

    def show_pingDialog(self):
        pingDialog.show()

    def show_tracertDialog(self):
        tracertDialog.show()

    def show_getmac(self):
        value = parse_getmac()
        getmac.plainTextEdit.setPlainText(value[0].encode("windows-1251").decode("cp866"))
        getmac.plainTextEdit_2.setPlainText(value[1].encode("windows-1251").decode("cp866"))

        getmac.show()
        with open(f'log/getmac {datetime.now().strftime("%H-%M, %m-%d-%Y")}.txt', 'w',
                  encoding='utf-8') as file:
            file.write(value[0].encode("windows-1251").decode("cp866") + '\n' + value[1].encode("windows-1251").decode(
                "cp866"))

    def show_nslookupDialog(self):
        nslookupDialog.show()

    def show_netstat(self):
        self.loadingNetstat = LoadingNetstat()
        self.loadingNetstat.show()

    def show_author(self):
        self.author = Author()
        self.author.show()


# noinspection PyUnresolvedReferences
class Ipconfig(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('../SystemAdminHelper/windows/ipconfig.ui', self)
        self.setWindowIcon(QIcon('../SystemAdminHelper/windows/computer-support.png'))


class ErrorDialog(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('../SystemAdminHelper/windows/errorDialog.ui', self)
        self.pushButton.clicked.connect(self.close_window)
        self.setWindowIcon(QIcon('../SystemAdminHelper/windows/computer-support.png'))

    def close_window(self):
        self.close()


# noinspection PyUnresolvedReferences
class PingDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.current_rb = ''

        loadUi('../SystemAdminHelper/windows/inputForPing.ui', self)
        self.setWindowIcon(QIcon('../SystemAdminHelper/windows/computer-support.png'))

        self.pb_OK.clicked.connect(self.run)

        self.rb_ip.toggled.connect(self.IP_clicked)

        self.rb_link.toggled.connect(self.link_clicked)

        self.rb_range.toggled.connect(self.range_clicked)

    def run(self):
        if self.current_rb == 'IP':
            if self.check_IP():
                self.loadingPing = LoadingPing()
                self.loadingPing.show()

            else:
                errorDialog.show()

        elif self.current_rb == 'Link':
            if self.check_link():
                values = self.check_link()
                ping.show()
                ping.plainTextEdit.setReadOnly(True)
                # ping.plainTextEdit.setPlainText('Загрузка')
                req = parse_ping(values[0], values[1], values[2])
                ping.plainTextEdit.setPlainText(req.encode("windows-1251").decode("cp866"))

                with open(f'log/ping {datetime.now().strftime("%H-%M, %m-%d-%Y")}.txt', 'w', encoding='utf-8') as file:
                    file.write(req.encode("windows-1251").decode("cp866"))

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
                    value += '\n'
                    value += parse_ping(ip, values[1], values[2])
                ping.plainTextEdit.setPlainText(value.encode("windows-1251").decode("cp866"))

                with open(f'log/ping {datetime.now().strftime("%H-%M, %m-%d-%Y")}.txt', 'w', encoding='utf-8') as file:
                    file.write(value.encode("windows-1251").decode("cp866"))
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
        pingDialog.le_ip.setPlaceholderText('Введите IP-адрес')

    def link_clicked(self):
        self.current_rb = 'Link'
        pingDialog.le_ip.setPlaceholderText('пример: google.com')

    def range_clicked(self):
        self.current_rb = 'Range'
        pingDialog.le_ip.setPlaceholderText('Введите два IP-адреса через пробел')


class Ping(QWidget):

    def __init__(self):
        super().__init__()
        loadUi('../SystemAdminHelper/windows/ping.ui', self)
        self.setWindowIcon(QIcon('../SystemAdminHelper/windows/computer-support.png'))

        self.plainTextEdit.setReadOnly(True)


class TracertDialog(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('../SystemAdminHelper/windows/inputForTracert.ui', self)
        self.setWindowIcon(QIcon('../SystemAdminHelper/windows/computer-support.png'))

        self.current_rb = ''

        self.pb_OK.clicked.connect(self.run)

        self.rb_ip.toggled.connect(self.IP_clicked)

        self.rb_link.toggled.connect(self.link_clicked)

        self.rb_range.toggled.connect(self.range_clicked)

    def run(self):
        if self.current_rb == 'IP':
            if self.check_IP():
                loading.show()

            else:
                errorDialog.show()

        elif self.current_rb == 'Link':
            if self.check_link():
                loading.show()

            else:
                errorDialog.show()

        elif self.current_rb == 'Range':
            if self.check_range():
                loading.show()
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
        pingDialog.le_ip.setPlaceholderText('Введите IP-адрес')

    def link_clicked(self):
        self.current_rb = 'Link'
        pingDialog.le_ip.setPlaceholderText('пример: dnevnik.ru')

    def range_clicked(self):
        self.current_rb = 'Range'
        pingDialog.le_ip.setPlaceholderText('Введите два IP-адреса через пробел')

    def open_loading(self):
        loading.show()


class Tracert(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('../SystemAdminHelper/windows/tracert.ui', self)
        self.setWindowIcon(QIcon('../SystemAdminHelper/windows/computer-support.png'))

        self.plainTextEdit.setReadOnly(True)


class Getmac(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('../SystemAdminHelper/windows/getmac.ui', self)
        self.setWindowIcon(QIcon('../SystemAdminHelper/windows/computer-support.png'))

        self.plainTextEdit.setReadOnly(True)


class NslookupInput(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('../SystemAdminHelper/windows/inputForNslookup.ui', self)
        self.setWindowIcon(QIcon('../SystemAdminHelper/windows/computer-support.png'))

        self.pb_OK.clicked.connect(self.run)

    def run(self):
        if self.check_domen():
            nslookup.show()
            value = parse_nslookup(self.le_domen.text())
            nslookup.plainTextEdit.setPlainText(value.encode("windows-1251").decode("cp866"))
            with open(f'log/nslookup {datetime.now().strftime("%H-%M, %m-%d-%Y")}.txt', 'w',
                      encoding='utf-8') as file:
                file.write(value.encode("windows-1251").decode("cp866"))
        else:
            errorDialog.show()

    def check_domen(self):
        if not self.le_domen.text().isnumeric():
            return True
        else:
            return True


class Nslookup(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('../SystemAdminHelper/windows/Nslookup.ui', self)
        self.setWindowIcon(QIcon('../SystemAdminHelper/windows/computer-support.png'))

        self.plainTextEdit.setReadOnly(True)


class Netstat(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('../SystemAdminHelper/windows/netstat.ui', self)
        self.setWindowIcon(QIcon('../SystemAdminHelper/windows/computer-support.png'))

        self.plainTextEdit.setReadOnly(True)


class Loading(QWidget):
    def __init__(self):
        super().__init__()
        self.tracert = Tracert()
        loadUi('../SystemAdminHelper/windows/Loading.ui', self)
        self.setWindowIcon(QIcon('../SystemAdminHelper/windows/computer-support.png'))

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Y:
            self.run()

        elif event.key() == Qt.Key.Key_N:
            self.close()

    def run(self):
        if tracertDialog.current_rb == 'IP':
            if self.check_IP():
                values = self.check_IP()

                req = parse_tracert(values[0], values[1], values[2])
                self.tracert.plainTextEdit.setPlainText(req.encode("windows-1251").decode("cp866"))

                with open(f'log/tracert {datetime.now().strftime("%H-%M, %m-%d-%Y")}.txt', 'w',
                          encoding='utf-8') as file:
                    file.write(req.encode("windows-1251").decode("cp866"))
                self.tracert.show()
                self.close()
            else:
                errorDialog.show()

        elif tracertDialog.current_rb == 'Link':
            if self.check_link():
                values = self.check_link()

                req = parse_tracert(values[0], values[1], values[2])
                self.tracert.plainTextEdit.setPlainText(req.encode("windows-1251").decode("cp866"))

                with open(f'log/tracert {datetime.now().strftime("%H-%M, %m-%d-%Y")}.txt', 'w',
                          encoding='utf-8') as file:
                    file.write(req.encode("windows-1251").decode("cp866"))
                self.tracert.show()
                self.close()
            else:
                errorDialog.show()

        elif tracertDialog.current_rb == 'Range':
            if self.check_range():
                values = self.check_range()
                value = ''
                for i in range(int(values[0][0].split('.')[-1]), int(values[0][1].split('.')[-1]) + 1):
                    ip = ''
                    for j in range(len(values[0][0].split('.')) - 1):
                        ip += values[0][0].split('.')[j] + '.'
                    ip += str(i)
                    value += '\n'
                    value += parse_tracert(ip, values[1], values[2])
                self.tracert.plainTextEdit.setPlainText(value.encode("windows-1251").decode("cp866"))
                with open(f'log/tracert {datetime.now().strftime("%H-%M, %m-%d-%Y")}.txt', 'w',
                          encoding='utf-8') as file:
                    file.write(value.encode("windows-1251").decode("cp866"))
                self.tracert.show()
                self.close()
            else:
                errorDialog.show()

    def check_IP(self):

        try:
            ipaddress.ip_address(tracertDialog.le_ip.text())
        except ValueError:
            return False
        else:
            ip_address = tracertDialog.le_ip.text()
            if tracertDialog.le_jumps.text() == '':
                jumps = '30'
            elif tracertDialog.le_jumps.text().isnumeric() and int(tracertDialog.le_jumps.text()) > 0:
                jumps = tracertDialog.le_jumps.text()
            else:
                return False

            if tracertDialog.le_timeout.text() == '':
                timeout = '4000'
            elif tracertDialog.le_timeout.text().isnumeric() and int(tracertDialog.le_timeout.text()) > 0:
                timeout = tracertDialog.le_timeout.text()
            else:
                return False
            return ip_address, jumps, timeout

    def check_link(self):
        if not tracertDialog.le_ip.text().isnumeric():
            ip_address = tracertDialog.le_ip.text()
        else:
            return False

        if tracertDialog.le_jumps.text() == '':
            jumps = '30'
        elif tracertDialog.le_jumps.text().isnumeric() and int(tracertDialog.le_jumps.text()) > 0:
            jumps = tracertDialog.le_jumps.text()
        else:
            return False

        if tracertDialog.le_timeout.text() == '':
            timeout = '4000'
        elif tracertDialog.le_timeout.text().isnumeric() and int(tracertDialog.le_timeout.text()) > 0:
            timeout = tracertDialog.le_timeout.text()
        else:
            return False
        return ip_address, jumps, timeout

    def check_range(self):
        try:
            ipaddress.ip_address(tracertDialog.le_ip.text().split()[0])
            ipaddress.ip_address(tracertDialog.le_ip.text().split()[1])
        except ValueError:
            return False
        else:
            ip_address = [tracertDialog.le_ip.text().split()[0], tracertDialog.le_ip.text().split()[1]]
            if tracertDialog.le_jumps.text() == '':
                jumps = '30'
            elif tracertDialog.le_jumps.text().isnumeric() and int(tracertDialog.le_jumps.text()) > 0:
                jumps = tracertDialog.le_jumps.text()
            else:
                return False

            if tracertDialog.le_timeout.text() == '':
                timeout = '4000'
            elif tracertDialog.le_timeout.text().isnumeric() and int(tracertDialog.le_timeout.text()) > 0:
                timeout = tracertDialog.le_timeout.text()
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


class LoadingPing(QWidget):

    def __init__(self):
        super().__init__()
        self.ping = Ping()
        loadUi('../SystemAdminHelper/windows/Loading.ui', self)
        self.setWindowIcon(QIcon('../SystemAdminHelper/windows/computer-support.png'))

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Y:
            self.run()

        elif event.key() == Qt.Key.Key_N:
            self.close()

    def run(self):
        if pingDialog.current_rb == 'IP':
            if self.check_IP():
                values = self.check_IP()
                req = parse_ping(values[0], values[1], values[2])
                self.ping.plainTextEdit.setPlainText(req.encode("cp866").decode("windows-1251"))

                with open(f'log/ping {datetime.now().strftime("%H-%M, %m-%d-%Y")}.txt', 'w', encoding='utf-8') as file:
                    file.write(req.encode("cp866").decode("windows-1251"))
                self.ping.show()
                self.close()
            else:
                errorDialog.show()

        elif self.current_rb == 'Link':
            if self.check_link():
                values = self.check_link()
                ping.show()
                ping.plainTextEdit.setReadOnly(True)
                # ping.plainTextEdit.setPlainText('Загрузка')
                req = parse_ping(values[0], values[1], values[2])
                ping.plainTextEdit.setPlainText(req.encode("cp866").decode("windows-1251"))

                with open(f'log/ping {datetime.now().strftime("%H-%M, %m-%d-%Y")}.txt', 'w', encoding='utf-8') as file:
                    file.write(req.encode("cp866").decode("windows-1251"))

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
                ping.plainTextEdit.setPlainText(value.encode("cp866").decode("windows-1251"))

                with open(f'log/ping {datetime.now().strftime("%H-%M, %m-%d-%Y")}.txt', 'w', encoding='utf-8') as file:
                    file.write(value.encode("cp866").decode("windows-1251"))
            else:
                errorDialog.show()

    def check_IP(self):

        try:
            ipaddress.ip_address(pingDialog.le_ip.text())
        except ValueError:
            return False
        else:
            ip_address = pingDialog.le_ip.text()
            if pingDialog.le_packets.text() == '':
                packets = '4'
            elif pingDialog.le_packets.text().isnumeric() and int(pingDialog.le_packets.text()) > 0:
                packets = pingDialog.le_packets.text()
            else:
                return False

            if pingDialog.le_timeout.text() == '':
                timeout = '4'
            elif pingDialog.le_timeout.text().isnumeric() and int(pingDialog.le_timeout.text()) > 0:
                timeout = pingDialog.le_timeout.text()
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


class LoadingNetstat(QWidget):

    def __init__(self):
        super().__init__()
        self.ping = Ping()
        loadUi('../SystemAdminHelper/windows/Loading.ui', self)
        self.setWindowIcon(QIcon('../SystemAdminHelper/windows/computer-support.png'))

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Y:
            self.run()

        elif event.key() == Qt.Key.Key_N:
            self.close()

    def run(self):
        value = parse_netstat()
        netstat.plainTextEdit.setPlainText(value[0].encode("windows-1251").decode("cp866"))
        netstat.plainTextEdit_2.setPlainText(value[1].encode("windows-1251").decode("cp866"))
        netstat.plainTextEdit_3.setPlainText(value[2].encode("windows-1251").decode("cp866"))
        netstat.plainTextEdit_4.setPlainText(value[3].encode("windows-1251").decode("cp866"))
        netstat.plainTextEdit.setReadOnly(True)
        netstat.plainTextEdit_2.setReadOnly(True)
        netstat.plainTextEdit_3.setReadOnly(True)
        netstat.plainTextEdit_4.setReadOnly(True)

        netstat.show()
        self.close()


class Author(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('../SystemAdminHelper/windows/author.ui', self)
        self.setWindowIcon(QIcon('../SystemAdminHelper/windows/computer-support.png'))
        self.pb_back.clicked.connect(self.back)

    def back(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    ipconfig = Ipconfig()
    mainWindow.show()
    pingDialog = PingDialog()
    errorDialog = ErrorDialog()
    ping = Ping()
    tracertDialog = TracertDialog()

    getmac = Getmac()
    nslookupDialog = NslookupInput()
    nslookup = Nslookup()
    netstat = Netstat()
    loading = Loading()
    try:
        sys.exit(app.exec())
    except SystemExit:
        print(os.path.dirname(sys.argv[0]))
        print('Закрытие приложения')
