'''
   Copyright 2022 zoutao

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''
from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtWidgets import QListWidget, QStackedWidget
from PySide2.QtWidgets import QHBoxLayout

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

class OpenImageHost(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(self.tr('Open图床'))
        self.sidelist=QListWidget()
        self.sideBar()
        self.mainStack=QStackedWidget()
        self.mainView()

        HBox=QHBoxLayout()
        HBox.addWidget(self.sidelist)
        HBox.addWidget(self.mainStack)
        self.setLayout(HBox)

    def sideBar(self):
        pass
    
    def mainView(self):
        pass

if __name__ == '__main__':
    app = QApplication()
    openImageHost = OpenImageHost()
    openImageHost.show()
    app.exec_()
