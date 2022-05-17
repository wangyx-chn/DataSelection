import sys
import time
import os.path as osp
import json
from PyQt5.QtWidgets import QDesktopWidget,QMessageBox,QApplication,QMainWindow,QWidget,QFileDialog
from PyQt5.QtGui import QPixmap, QPainter, QIcon
from PyQt5.QtCore import QSize
from Ui_Main import Ui_MainWindow
from imgviewer import ImageViewer

source = ['arcgis','bing','google']

class MainForm(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MainForm,self).__init__()
        self.setupUi(self)
        self.AutoCenter()
        self.SetIcon()
        self.connectSignal()
        self.setWindowIcon(QIcon('./winicon.png'))
        self.setWindowTitle('DataSelect')
        self.imgview = ImageViewer()
        self.gridLayout_2.addWidget(self.imgview, 0, 0, 2, 1)

    def connectSignal(self):
        self.start_btn.clicked.connect(self.StartSelect)
        self.last_btn.clicked.connect(self.LastPic)
        self.next_btn.clicked.connect(self.NextPic)
        self.view_btn.clicked.connect(self.ChangeView)
        self.full_ava_btn.clicked.connect(self.Record)
        self.part_ava_btn.clicked.connect(self.Record)
        self.not_ava_btn.clicked.connect(self.Record)
        self.actionopenfile.triggered.connect(self.OpenFile)
        self.actionopenfolder.triggered.connect(self.ChooseFolder)
        
    
    def SetIcon(self):
        lasticon = QIcon('./left.png')
        nexticon = QIcon('./right.png')
        self.last_btn.setIcon(lasticon)
        self.next_btn.setIcon(nexticon)

    def AutoCenter(self):
        screen = QDesktopWidget().screenGeometry()
        init_size = QSize(screen.width()*2//3,screen.height()*2//3)
        self.resize(init_size)
        self.move((screen.width()-init_size.width())//2,
        (screen.height()-init_size.height())//2)

    def OpenFile(self):
        file,_ = QFileDialog.getOpenFileName(self,"OpenFile")
        self.Log(f"Open : {file}")
        self.imgview.setImage(file)

    def Log(self,text:str):
        time_str = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        text = time_str + " " + text
        self.LogBrowser.append(text)

    def ChooseFolder(self):
        self.dir = QFileDialog.getExistingDirectory(self,"选取文件夹","C:/Users/wangyx/Desktop")
        self.start_btn.setEnabled(True)
        self.Log('Open folder:'+self.dir)

    def StartSelect(self):
        self.Log("Start Selecting ...")
        jsonfile = osp.join(self.dir,'big_image.json')
        self.jsonfile = jsonfile
        if osp.exists(jsonfile):
            with open(jsonfile,'r+') as f:
                content = f.read()
                if content != '':
                    self.labels = json.loads(content)
                    self.picIndex = len(self.labels)+1
                else:
                    self.Log(".json file is empty")
                    self.labels = {}
                    self.picIndex = 1
                
        else:
            self.Log(f"create a .json file {jsonfile}")
            f = open(jsonfile,'w')
            f.close()
            self.labels = {}
            self.picIndex = 1

        self.viewIndex = 0
        self.show_img()
        self.view_btn.setEnabled(True)
        self.last_btn.setEnabled(True)
        self.next_btn.setEnabled(True)
        self.view_btn.setEnabled(True)
        self.full_ava_btn.setEnabled(True)
        self.part_ava_btn.setEnabled(True)
        self.not_ava_btn.setEnabled(True)
        self.start_btn.setEnabled(False)


    def NextPic(self):
        if self.picIndex<923:
            self.picIndex+=1
            self.show_img()
        else:
            QMessageBox.warning(self,"提示","当前已经是最后一张图像")

    def LastPic(self):
        if self.picIndex>1:
            self.picIndex-=1
            self.show_img()
        else:
            QMessageBox.warning(self,"提示","当前已经是第一张图像")
    
    def ChangeView(self):
        self.viewIndex = (self.viewIndex+1)%3
        self.show_img()

    def show_img(self):
        self.Log(f"Current Pic : {self.picIndex} View : {source[self.viewIndex]}")
        img_file = osp.join(self.dir,f'{self.picIndex}_{source[self.viewIndex]}.jpg')
        img = QPixmap(img_file)
        self.imgbox.setPixmap(img)

    def Record(self):
        img_type = self.sender().objectName()
        if img_type=='full_ava_btn':
            self.labels[self.picIndex]='F'
            self.Log(f"Pic {self.picIndex} is marked as F : [[ Fully Available ]]")
        elif img_type=='part_ava_btn':
            self.labels[self.picIndex]='P'
            self.Log(f"Pic {self.picIndex} is marked as P : [[ Partly Available ]]")
        else:
            self.labels[self.picIndex]='N'
            self.Log(f"Pic {self.picIndex} is marked as N : [[ Not Available ]]")
        self.NextPic()

    def closeEvent(self, event) -> None:
        if hasattr(self,'jsonfile'):
            with open(self.jsonfile,'w') as f:
                json.dump(self.labels,f,indent=4)
        event.accept()

if __name__=='__main__':
    App = QApplication(sys.argv)
    win = MainForm()
    win.show()
    sys.exit(App.exec_())