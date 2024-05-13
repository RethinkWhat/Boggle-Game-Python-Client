from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QLabel, QApplication
from PyQt5.QtCore import Qt, QSize


class Ui_LobbyView(object):
    def setupUi(self, LobbyView):
        LobbyView.setObjectName("MainWindow")
        LobbyView.setEnabled(True)
        LobbyView.resize(1000, 600)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            LobbyView.sizePolicy().hasHeightForWidth()
        )
        LobbyView.setSizePolicy(sizePolicy)
        LobbyView.setMinimumSize(QtCore.QSize(1000, 600))
        LobbyView.setMaximumSize(QtCore.QSize(1000, 600))
        self.centralwidget = QtWidgets.QWidget(LobbyView)
        self.centralwidget.setObjectName("centralwidget")
        self.topWid = QtWidgets.QWidget(self.centralwidget)
        self.topWid.setStyleSheet("background-color: orange;")
        self.topWid.setGeometry(QtCore.QRect(0, 0, 1000, 50))
        self.topWid.setObjectName("topWid")

        self.home = QtWidgets.QPushButton(self.topWid)
        self.home.setGeometry(QtCore.QRect(780, 0, 50, 50))
        self.home.setObjectName("home")
        pixmap = QPixmap("../../res/lobby/home-white-solid.png")
        scaled_img = pixmap.scaled(self.home.size(), Qt.KeepAspectRatio)
        self.home.setIcon(QIcon(scaled_img))

        self.setting = QtWidgets.QPushButton(self.topWid)
        self.setting.setGeometry(QtCore.QRect(850, 0, 50, 50))
        self.setting.setObjectName("setting")
        pixmap = QPixmap("../../res/lobby/settings-white-solid.png")
        scaled_img = pixmap.scaled(self.setting.size(), Qt.KeepAspectRatio)
        self.setting.setIcon(QIcon(scaled_img))

        self.exit = QtWidgets.QPushButton(self.topWid)
        self.exit.setGeometry(QtCore.QRect(930, 0, 50, 50))
        self.exit.setObjectName("exit")
        pixmap = QPixmap("../../res/lobby/logout-white-solid.png")
        scaled_img = pixmap.scaled(self.exit.size(), Qt.KeepAspectRatio)
        self.exit.setIcon(QIcon(scaled_img))

        self.GameIcon = QtWidgets.QWidget(self.topWid)
        self.GameIcon.setGeometry(QtCore.QRect(0, 0, 121, 51))
        self.GameIcon.setObjectName("GameIcon")
        self.label = QLabel(self.GameIcon)
        self.label.setGeometry(QtCore.QRect(0, 0, 121, 51))

        # scaling image
        pixmap = QPixmap("../../res/lobby/logo-solid-white.png")
        scaled_img = pixmap.scaled(self.label.size(), Qt.KeepAspectRatio)
        self.label.setPixmap(scaled_img)

        self.Location = QtWidgets.QWidget(self.topWid)
        self.Location.setGeometry(QtCore.QRect(130, 0, 120, 51))
        self.Location.setObjectName("Location")
        self.bottomWid = QtWidgets.QWidget(self.centralwidget)
        self.bottomWid.setGeometry(QtCore.QRect(0, 50, 1000, 531))
        self.bottomWid.setObjectName("bottomWid")
        self.listWidget = QtWidgets.QListWidget(self.bottomWid)
        self.listWidget.setGeometry(QtCore.QRect(50, 20, 891, 431))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setStyleSheet("background-image: url('../../res/lobby/koyuki.jpg');")

        self.pushButton = QtWidgets.QPushButton(self.bottomWid)
        self.pushButton.setGeometry(QtCore.QRect(410, 460, 181, 41))
        self.pushButton.setStyleSheet(
            "background-color: #E6074A; border-radius: 10px; color: white;"
        )
        font = QtGui.QFont()
        font.setFamily("Barlow Semi Condensed ExtraBold")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.scrollArea = QtWidgets.QScrollArea(self.bottomWid)
        self.scrollArea.setGeometry(QtCore.QRect(909, 29, 21, 411))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 19, 409))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        LobbyView.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(LobbyView)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 20))
        self.menubar.setObjectName("menubar")
        LobbyView.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(LobbyView)
        self.statusbar.setObjectName("statusbar")
        LobbyView.setStatusBar(self.statusbar)

        self.retranslateUi(LobbyView)
        QtCore.QMetaObject.connectSlotsByName(LobbyView)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Lobby View", "Lobby View"))
        self.pushButton.setText(_translate("Lobby View", "EXIT LOBBY"))


class LobbyViewApp(QtWidgets.QMainWindow, Ui_LobbyView):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.exit_lobby)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollAreaWidgetContents.setMinimumHeight(500)

    def exit_lobby(self):
        QtWidgets.QApplication.quit()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    lobby_view = LobbyViewApp()
    lobby_view.show()
    sys.exit(app.exec_())
