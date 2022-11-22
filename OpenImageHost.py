from PySide2 import QtCore, QtGui, QtWidgets

class ImageHostConf():

    def __init__(self) -> None:
        pass

    def readConf(self):
        pass

    def writeConf(self):
        pass

    def updateConf(self):
        pass

    def getConf(self, conf: str):
        pass

class OpenImageHost(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(self.tr('Open图床'))
        self.sidelist=QtWidgets.QListWidget()
        self.sideBar()
        self.mainStack=QtWidgets.QStackedWidget()
        self.mainView()

        HBox=QtWidgets.QHBoxLayout()
        HBox.addWidget(self.sidelist)
        HBox.addWidget(self.mainStack)
        self.setLayout(HBox)

    def sideBar(self):
        pass
    
    def mainView(self):
        pass

if __name__ == '__main__':
    app = QtWidgets.QApplication()
    openImageHost = OpenImageHost()
    openImageHost.show()
    app.exec_()
