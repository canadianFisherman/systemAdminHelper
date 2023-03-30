import sys
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QTextEdit, QPushButton, QGridLayout, QLineEdit, \
    QPlainTextEdit, QTreeWidgetItem, QDialog
from PyQt6.uic import loadUi
from parsing_ipconfig import devices
from parsing_ping import parse


# noinspection PyUnresolvedReferences
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('../SysAdminHelper/windows/main.ui', self)
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
        loadUi('../SysAdminHelper/windows/ipconfig.ui', self)

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
        loadUi('../SysAdminHelper/windows/errorDialog.ui', self)
        self.pushButton.clicked.connect(self.close_window)

    def close_window(self):
        self.close()


# noinspection PyUnresolvedReferences
class PingDialog(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('../SysAdminHelper/windows/inputForPing.ui', self)
        self.pb_OK.clicked.connect(self.run)

    def run(self):
        if self.le_ip.text() == '':
            errorDialog.show()
        else:
            ip = self.le_ip.text()
            if self.le_packets.text().isnumeric() and self.le_timeout.text().isnumeric():
                packets = self.le_packets.text()
                timeout = self.le_timeout.text()
                ping.show()
                ping.label.setText(parse(ip=ip, packets=packets, timeout=timeout))

            elif self.le_packets.text().isalpha() or self.le_timeout.text().isalpha():
                errorDialog.show()
            elif not self.le_packets.text().isalnum() or not self.le_timeout.text().isalnum():
                if not self.le_packets.text().isalnum():
                    packets = "4"
                else:
                    packets = self.le_packets.text()
                if not self.le_timeout.text().isalnum():
                    timeout = '4'
                else:
                    timeout = self.le_timeout.text()
                ping.show()
                ping.label.setText(parse(ip=ip, packets=packets, timeout=timeout))


class Ping(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('../SysAdminHelper/windows/ping.ui', self)


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
