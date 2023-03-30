import sys
import ipaddress
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QTextEdit, QPushButton, QGridLayout, QLineEdit, \
    QPlainTextEdit, QTreeWidgetItem, QDialog, QRadioButton
from PyQt6.uic import loadUi
from parsing_ipconfig import devices
from parsing_ping import parse


# noinspection PyUnresolvedReferences
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('../SystemAdminHelper/windows/main.ui', self)
        self.pb_ipconfig.clicked.connect(self.show_ipconfig)
        self.pb_ping.clicked.connect(self.show_pingDialog)

    def show_ipconfig(self):
        ipconfig.show()

    def show_pingDialog(self):
        pingDialog.show()


# noinspection PyUnresolvedReferences
class Ipconfig(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('../SystemAdminHelper/windows/ipconfig.ui', self)

        for k, v in devices.items():
            value = QTreeWidgetItem(self.treeWidget)
            value.setText(0, k)

            for s in v:
                value1 = QTreeWidgetItem(value)
                value1.setText(0, s)
                value.addChild(value1)


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
                print(parse(values[0], values[1], values[2]))

            else:
                errorDialog.show()

        elif self.current_rb == 'Link':
            if self.check_link():
                values = self.check_link()
                print(parse(values[0], values[1], values[2]))
            else:
                errorDialog.show()

        elif self.current_rb == 'Range':
            if self.check_range():
                values = self.check_range()
                for i in range(int(values[0][0].split('.')[-1]), int(values[0][1].split('.')[-1]) + 1):
                    ip = ''
                    for j in range(len(values[0][0].split('.')) - 1):
                        ip += values[0][0].split('.')[j] + '.'
                    ip += str(i)
                    print(parse(ip, values[1], values[2]))
            else:
                errorDialog.show()

    # if self.onClicked_Link()

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

    def link_clicked(self):
        self.current_rb = 'Link'

    def range_clicked(self):
        self.current_rb = 'Range'



class Ping(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('../SystemAdminHelper/windows/ping.ui', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    ipconfig = Ipconfig()
    mainWindow.show()
    pingDialog = PingDialog()
    errorDialog = ErrorDialog()
    ping = Ping()
    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Закрытие приложения')
