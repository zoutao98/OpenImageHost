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
import base64
import datetime
import functools
import json
import os
import pathlib
import threading
import time
from PySide2.QtCore import QTimer, QByteArray, QBuffer, QIODevice, Signal
from PySide2.QtGui import Qt, QImage, QStandardItemModel, QStandardItem, QPixmap, QMovie
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QSizePolicy
from PySide2.QtWidgets import QStackedWidget, QTreeView
from PySide2.QtWidgets import QHBoxLayout, QFormLayout, QLineEdit
from PySide2.QtWidgets import QToolBar, QPushButton

import icon

class NoticeWidget(QLabel):
    _parent = None

    def __init__(self, parent, text):
        super().__init__()
        self._parent = parent
        self.setParent(parent)
        self.setText(text)
        self.setAlignment(Qt.AlignCenter)
        self.setVisible(True)
        self.setStyleSheet("color: white;background-color:rgba(80, 80, 80, 255);border-radius:7px;")
        self.installEventFilter(self)
        self.changeSize()
        self.timer = QTimer()

        self.timer.start(1000)
        self.timer.timeout.connect(self.handleTimeOut)
    
    def changeSize(self):
        if self._parent:
            w = self._parent.width() * 0.5
            self.setFixedSize(w, 30)
            self.move((self._parent.width() - self.width()) >> 1, (self._parent.height() - self.height()) >> 1)
    
    def handleTimeOut(self):
        self.timer.stop()
        self.deleteLater()
    
    def eventFilter(self, watched, event):
        if event.type() == event.Paint:
            self.changeSize()
        return super().eventFilter(watched, event)

class Conf():
    _instance_lock = threading.Lock()

    confPath = 'conf'
    confFile = 'conf/conf.json'
    repo = 'github.repo'
    token = 'github.token'
    fork = 'github.fork'
    proxy = 'github.proxy'

    def __init__(self) -> None:
        pass
    
    @property
    def conf(self):
        return self._conf

    @conf.setter
    def conf(self, value):
        self._conf = value
        self.updateConf()

    def readConf(self):
        if not hasattr(self, '_conf'):
            self._conf = {}
        if not os.path.exists(self.confPath):
            os.makedirs(self.confPath)
        try:
            with open(self.confFile, 'r') as f:
                jsonStr = f.read()
                self._conf = json.loads(jsonStr)
        except:
            with open(self.confFile, 'w') as f:
                json.dump(self._conf, f)

    def writeConf(self):
        pass

    def updateConf(self):
        with self._instance_lock:
            with open(self.confFile, 'w') as f:
                json.dump(self._conf, f)

    def getConf(self, confstr: str):
        try:
            self.conf[confstr]
        except:
            self.conf[confstr] = ''
            self.conf = self.conf
        return self.conf[confstr]
    
    def setConf(self, confstr, value):
        self.conf[confstr] = value
        self.conf = self.conf
        return self.conf[confstr]
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = object.__new__(cls)
                    cls.readConf(cls)
        return cls._instance

class PhotosConf():
    _instance_lock = threading.Lock()
    pcf = 'app.json'
    
    sha = ''
    def __init__(self, *widget) -> None:
        pass

    @property
    def conf(self):
        return self._conf
    
    @conf.setter
    def conf(self, value):
        self._conf = value

    def readConf(self):
        if not hasattr(self, '_conf'):
            self._conf = {}
        def getPhotosConf():
            repo = Conf().getConf(Conf.repo)
            fork = Conf().getConf(Conf.fork)
            token = Conf().getConf(Conf.token)
            if repo == '' or fork == '' or token == '':
                return
            import githubfile
            # self._photo.photosTip.emit('??????')
            resp = githubfile.getFile(token, repo, self.pcf)
            if resp.status_code == 200 or resp.status_code == 201:
                respjson = json.loads(resp.text)
                self.sha = respjson['sha']
                content = respjson['content']
                getconf = base64.b64decode(content).decode('utf-8')
                self.conf = (json.loads(getconf))
                self._photo.photosTip.emit('??????????????????')
                self._photo.updatePhotos.emit()
            else:
                respjson = json.loads(resp.text)
                self._photo.photosTip.emit(f'{resp.status_code}:{respjson["message"]}')
        task = threading.Thread(target=getPhotosConf)
        task.daemon = True
        task.start()

    def append(self, data):
        try:
            self.conf['photos']
            self.conf['photos'].append(data)
        except:
            self.conf['photos'] = []
            self.conf['photos'].append(data)
        def updateConf():
            repo = Conf().getConf(Conf.repo)
            fork = Conf().getConf(Conf.fork)
            token = Conf().getConf(Conf.token)
            if repo == '' or fork == '' or token == '':
                self._photo.photosTip.emit('????????????GitHub??????')
                return
            import githubfile
            resp = githubfile.updateFile(token, repo, self.pcf, base64.b64encode(json.dumps(self.conf).encode('utf-8')).decode('utf-8'), self.sha)
            if resp.status_code == 200 or resp.status_code == 201:
                respJson = json.loads(resp.text)
                self.sha = respJson['content']['sha']
                self._photo.updatePhotos.emit()
        task = threading.Thread(target=updateConf)
        task.daemon = True
        task.start()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = object.__new__(cls)
                    cls._photo = args[0]
                    cls.readConf(cls)
        return cls._instance

class SettingWidget(QWidget):

    def __init__(self) -> None:
        super().__init__()
        layout=QFormLayout()

        self.repo = QLineEdit(placeholderText='user/repo', text=Conf().getConf(Conf.repo))
        layout.addRow(self.tr('??????'), self.repo)

        self.fork = QLineEdit(placeholderText='fork', text=Conf().getConf(Conf.fork))
        layout.addRow(self.tr('??????'), self.fork)

        self.token = QLineEdit(placeholderText='token', text=Conf().getConf(Conf.token))
        layout.addRow(self.tr('Token'), self.token)

        self.proxy = QLineEdit(placeholderText='proxy', text=Conf().getConf(Conf.proxy))
        layout.addRow(self.tr('??????'),self.proxy)

        okButton = QPushButton(self.tr('??????'))
        okButton.clicked.connect(self.validateForm)
        layout.addRow(okButton)
        self.setLayout(layout)
    
    def validateForm(self):
        text = self.repo.text()
        if text == '':
            NoticeWidget(self.nativeParentWidget(), self.tr('??????????????????'))
            return
        if len(text.split('/')) != 2:
            NoticeWidget(self.nativeParentWidget(), self.tr('??????????????????'))
            return
        Conf().setConf(Conf().repo, text)

        text = self.fork.text()
        if text == '':
            NoticeWidget(self.nativeParentWidget(), self.tr('???????????????'))
            return
        Conf().setConf(Conf().fork, text)

        text = self.token.text()
        if text == '':
            NoticeWidget(self.nativeParentWidget(), self.tr('?????????Token'))
            return
        Conf().setConf(Conf().token, text)

        text = self.proxy.text()
        Conf().setConf(Conf().proxy, text)


class UploadWidget(QWidget):

    def __init__(self) -> None:
        super().__init__()
        layout=QFormLayout()
        uploadButton = QPushButton(self.tr('????????????'))
        uploadButton.setObjectName('uploadButton')
        shearButton = QPushButton(self.tr('???????????????'))
        shearButton.setObjectName('shearButton')
        layout.addRow(uploadButton)
        layout.addRow(shearButton)
        self.uploadPath = QLineEdit(placeholderText='path',)
        layout.addRow(self.tr('?????????'),self.uploadPath)
        self.setLayout(layout)

        uploadButton.clicked.connect(self.upload)
        shearButton.clicked.connect(self.shear)
    
    def upload(self):
        repo = Conf().getConf(Conf.repo)
        fork = Conf().getConf(Conf.fork)
        token = Conf().getConf(Conf.token)
        if repo == '' or fork == '' or token == '':
            NoticeWidget(self.nativeParentWidget(), self.tr('????????????GitHub??????'))
            return
        file = QFileDialog.getOpenFileName(self.nativeParentWidget(), self.tr('????????????'), filter=self.tr('Image Files (*)'))
        if file[0]:
            import githubfile
            filePath = file[0]
            content = githubfile.getContent(filePath)
            filePath = pathlib.Path(filePath)
            fileName = filePath.name
            uploadPath = self.uploadPath.text()
            if uploadPath != '':
                fileName = f'{uploadPath}/{fileName}'
            resp = githubfile.uploadFile(token, repo, fileName, content)
            if resp.status_code == 200 or resp.status_code == 201:
                respJson = json.loads(resp.text)
                rawUrl = respJson['content']['download_url']
                markdownExample = f'![]({rawUrl})'
                
                fastgitRawUrl = f'https://raw.fastgit.org/{repo}/{fork}/{fileName}'
                markdownExample = f'![]({fastgitRawUrl})'
                QApplication.clipboard().setText(markdownExample)
                NoticeWidget(self.nativeParentWidget(), self.tr('?????????????????????'))
                PhotosConf().append({
                    'filename': fileName,
                    'raw': rawUrl,
                    'fast': fastgitRawUrl,
                    'sha': respJson['content']['sha']
                })

    def shear(self):
        clipboard = QApplication.clipboard()
        clipdata = clipboard.mimeData()
        if clipdata.hasImage():
            img: QImage = clipdata.imageData()
            ba = QByteArray()
            buffer = QBuffer(ba)
            buffer.open(QIODevice.WriteOnly)
            img.save(buffer, 'PNG')
            content = ba.toBase64().data().decode('utf-8')
            fileName = f'{datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")}.PNG'
            uploadPath = self.uploadPath.text()
            if uploadPath != '':
                fileName = f'{uploadPath}/{fileName}'
            repo = Conf().getConf(Conf.repo)
            fork = Conf().getConf(Conf.fork)
            token = Conf().getConf(Conf.token)
            if repo == '' or fork == '' or token == '':
                NoticeWidget(self.nativeParentWidget(), self.tr('????????????GitHub??????'))
                return
            import githubfile
            resp = githubfile.uploadFile(token, repo, fileName, content)
            if resp.status_code == 200 or resp.status_code == 201:
                respJson = json.loads(resp.text)
                rawUrl = respJson['content']['download_url']
                markdownExample = f'![]({rawUrl})'
                
                fastgitRawUrl = f'https://raw.fastgit.org/{repo}/{fork}/{fileName}'
                markdownExample = f'![]({fastgitRawUrl})'
                QApplication.clipboard().setText(markdownExample)
                NoticeWidget(self.nativeParentWidget(), self.tr('?????????????????????'))
                PhotosConf().append({
                    'filename': fileName,
                    'raw': rawUrl,
                    'fast': fastgitRawUrl,
                    'sha': respJson['content']['sha']
                })
        else:
            NoticeWidget(self.nativeParentWidget(), self.tr('???????????????????????????'))

class ImageWidget(QWidget):

    loading = Signal()

    def __init__(self, photo) -> None:
        super().__init__()
        self.photo = photo
        layout = QFormLayout()
        self.label= QLabel()
        self.label.setFixedSize(64, 64)

        opt = QToolBar()
        markdown = QPushButton("Markdown")
        opt.addWidget(markdown)
        def markdownClip():
            fastgitRawUrl = self.photo['fast']
            markdownExample = f'![]({fastgitRawUrl})'
            QApplication.clipboard().setText(markdownExample)
            NoticeWidget(self.nativeParentWidget(), self.tr('?????????????????????'))
        markdown.clicked.connect(markdownClip)
        layout.addRow(self.label, opt)
        self.setLayout(layout)
        self.movie = QMovie(':/icon/loading.gif')
        self.label.setMovie(self.movie)
        self.movie.start()

        task = threading.Thread(target=self.getPhoto)
        task.daemon = True
        task.start()
        self.loading.connect(self.loadingStop)

    def loadingStop(self):
        self.movie.stop()
        self.label.repaint()

    
    def getPhoto(self):
        import requests
        resp = requests.get(self.photo['fast'])
        if resp.status_code == 200:
            photo = QPixmap()
            #photo.loadFromData(req.content, "JPG")
            photo.loadFromData(resp.content)
            photo = photo.scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label.setPixmap(photo)
            self.loading.emit()


class PhotosWidget(QWidget):

    photosTip = Signal(str)
    updatePhotos = Signal()
    photos = []

    def __init__(self) -> None:
        super().__init__()
        PhotosConf(self)
        self.photosTip.connect(self.tips)
        self.updatePhotos.connect(self.updatePhoto)

        self.formLayout = QFormLayout()
        self.setLayout(self.formLayout)

    def tips(self, strings):
        NoticeWidget(self.nativeParentWidget(), self.tr(strings))

    def updatePhoto(self):
        try:
            PhotosConf().conf['photos']
            for photo in PhotosConf().conf['photos']:
                if photo not in self.photos:
                    imageWidget = ImageWidget(photo)
                    self.formLayout.addRow(imageWidget)
                    self.photos.append(photo)
                    self.repaint()
        except:
            return


class OpenImageHost(QWidget):
    
    sideBarMenus = ['??????', '??????', '??????']

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(self.tr('Open??????'))

        self.mainStack=QStackedWidget()
        self.sideBar=QToolBar()
        
        self.mainViewInit()
        self.sideBarInit()

        HBox=QHBoxLayout()
        HBox.addWidget(self.sideBar)
        HBox.addWidget(self.mainStack)
        self.setLayout(HBox)

    def sideBarInit(self):
        self.sideBar.setOrientation(Qt.Vertical)
        for sideBarMenu in self.sideBarMenus:
            if(sideBarMenu == '??????'):
                stackWidget = UploadWidget()
            elif(sideBarMenu == '??????'):
                stackWidget = SettingWidget()
            elif(sideBarMenu == '??????'):
                stackWidget = PhotosWidget()
            else:
                continue

            self.mainStack.addWidget(stackWidget)

            pushButton = QPushButton(self.tr(sideBarMenu))
            pushButton.clicked.connect(functools.partial(self.mainStack.setCurrentWidget, stackWidget))
            self.sideBar.addWidget(pushButton)
    
    def mainViewInit(self):
        pass

if __name__ == '__main__':
    Conf()
    app = QApplication()
    
    openImageHost = OpenImageHost()
    openImageHost.show()
    app.exec_()
