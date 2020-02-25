
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui

class Ui_slideways(object):
    def setupUi(self, slideways):
        """Initialise un fenêtre avec tous les bouttons et Widget"""
        self.xligne1 = 400
        self.xligne2 = 400
        self.xligne3 = 400
        self.xligne4 = 400
        slideways.setObjectName("slideways")
        slideways.resize(1200, 600)
        slideways.setMinimumSize(QSize(1200, 600))
        slideways.setMaximumSize(QSize(1200, 600))
        slideways.setContextMenuPolicy(Qt.NoContextMenu)
        icon = QIcon()
        icon.addPixmap(QPixmap("icon.png"), QIcon.Normal, QIcon.Off)
        slideways.setWindowIcon(icon)
        slideways.setTabShape(QTabWidget.Rounded)
        self.centralwidget = QWidget(slideways)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QFrame(self.centralwidget)
        self.frame.setGeometry(QRect(0, 0, 1200, 500))
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Plain)
        self.frame.setLineWidth(0)
        self.frame.setObjectName("frame")

        self.text_button = QPushButton("Current Game : Human vs Human", self)
        self.text_button.setGeometry(QRect(450, 525, 300, 50))
        self.text_button.setStyleSheet('QPushButton {background-color: #8CC6EA; color: #FFFFFF;}')
        self.text_button.setEnabled(False)
        

        self.A4 = QPushButton(self.frame)
        self.A4.setGeometry(QRect(self.xligne1, 50, 100, 100))
        self.A4.setStyleSheet('QPushButton {background-color: #D7D7D7; color: #D7D7D7;}')
        self.A4.setObjectName("A4")

        self.B4 = QPushButton(self.frame)
        self.B4.setGeometry(QRect(self.xligne1+100, 50, 100, 100))
        self.B4.setStyleSheet('QPushButton {background-color: #D7D7D7; color: #D7D7D7;}')
        self.B4.setObjectName("B4")

        self.C4 = QPushButton(self.frame)
        self.C4.setGeometry(QRect(self.xligne1+200, 50, 100, 100)) 
        self.C4.setStyleSheet('QPushButton {background-color: #D7D7D7; color: #D7D7D7;}')
        self.C4.setObjectName("C4")

        self.D4 = QPushButton(self.frame)
        self.D4.setGeometry(QRect(self.xligne1+300, 50, 100, 100))
        self.D4.setStyleSheet('QPushButton {background-color: #D7D7D7; color: #D7D7D7;}')
        self.D4.setObjectName("D4")

        self.A3 = QPushButton(self.frame)
        self.A3.setGeometry(QRect(self.xligne2, 150, 100, 100))
        self.A3.setStyleSheet('QPushButton {background-color: #D7D7D7; color: #D7D7D7;}')
        self.A3.setObjectName("A3")

        self.B3 = QPushButton(self.frame)
        self.B3.setGeometry(QRect(self.xligne2+100, 150, 100, 100))
        self.B3.setStyleSheet('QPushButton {background-color: #D7D7D7; color: #D7D7D7;}')
        self.B3.setObjectName("B3")

        self.C3 = QPushButton(self.frame)
        self.C3.setGeometry(QRect(self.xligne2+200, 150, 100, 100)) 
        self.C3.setStyleSheet('QPushButton {background-color: #D7D7D7; color: #D7D7D7;}')
        self.C3.setObjectName("C3")

        self.D3 = QPushButton(self.frame)
        self.D3.setGeometry(QRect(self.xligne2+300, 150, 100, 100))
        self.D3.setStyleSheet('QPushButton {background-color: #D7D7D7; color: #D7D7D7;}')
        self.D3.setObjectName("D3")

        self.A2 = QPushButton(self.frame)
        self.A2.setGeometry(QRect(self.xligne3, 250, 100, 100))
        self.A2.setStyleSheet('QPushButton {background-color: #D7D7D7; color: #D7D7D7;}') 
        self.A2.setObjectName("A2")
    
        self.B2 = QPushButton(self.frame)
        self.B2.setGeometry(QRect(self.xligne3+100, 250, 100, 100)) 
        self.B2.setStyleSheet('QPushButton {background-color: #D7D7D7; color: #D7D7D7;}')
        self.B2.setObjectName("B2")

        self.C2 = QPushButton(self.frame)
        self.C2.setGeometry(QRect(self.xligne3+200, 250, 100, 100)) 
        self.C2.setStyleSheet('QPushButton {background-color: #D7D7D7; color: #D7D7D7;}')
        self.C2.setObjectName("C2")

        self.D2 = QPushButton(self.frame)
        self.D2.setGeometry(QRect(self.xligne3+300, 250, 100, 100)) 
        self.D2.setStyleSheet('QPushButton {background-color: #D7D7D7; color: #D7D7D7;}')
        self.D2.setObjectName("D2")

        self.A1 = QPushButton(self.frame)
        self.A1.setGeometry(QRect(self.xligne4, 350, 100, 100))
        self.A1.setStyleSheet('QPushButton {background-color: #D7D7D7; color: #D7D7D7;}')
        self.A4.setObjectName("A1")

        self.B1 = QPushButton(self.frame)
        self.B1.setGeometry(QRect(self.xligne4+100, 350, 100, 100)) 
        self.B1.setStyleSheet('QPushButton {background-color: #D7D7D7; color: #D7D7D7;}')
        self.B1.setObjectName("B1")

        self.C1 = QPushButton(self.frame)
        self.C1.setGeometry(QRect(self.xligne4+200, 350, 100, 100)) 
        self.C1.setStyleSheet('QPushButton {background-color: #D7D7D7; color: #D7D7D7;}')
        self.C1.setObjectName("C1")

        self.D1 = QPushButton(self.frame)
        self.D1.setGeometry(QRect(self.xligne4+300, 350, 100, 100))
        self.D1.setStyleSheet('QPushButton {background-color: #D7D7D7; color: #D7D7D7;}')
        self.D1.setObjectName("D1")

        self.plusligne1 = QPushButton(">", self.frame)
        self.plusligne1.setGeometry(QRect(1100, 50, 50, 100))

        self.plusligne2 = QPushButton(">", self.frame)
        self.plusligne2.setGeometry(QRect(1100, 150, 50, 100))

        self.plusligne3 = QPushButton(">", self.frame)
        self.plusligne3.setGeometry(QRect(1100, 250, 50, 100))

        self.plusligne4 = QPushButton(">", self.frame)
        self.plusligne4.setGeometry(QRect(1100, 350, 50, 100))

        self.moinsligne1 = QPushButton("<", self.frame)
        self.moinsligne1.setGeometry(QRect(50, 50, 50, 100))

        self.moinsligne2 = QPushButton("<", self.frame)
        self.moinsligne2.setGeometry(QRect(50, 150, 50, 100))

        self.moinsligne3 = QPushButton("<", self.frame)
        self.moinsligne3.setGeometry(QRect(50, 250, 50, 100))

        self.moinsligne4 = QPushButton("<", self.frame)
        self.moinsligne4.setGeometry(QRect(50, 350, 50, 100))


        slideways.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(slideways)
        self.menubar.setGeometry(QRect(0, 0, 627, 50))
        self.menubar.setObjectName("menubar")
        self.menuNew = QMenu(self.menubar)
        self.menuNew.setObjectName("menuNew")
        slideways.setMenuBar(self.menubar)
        self.toolBar = QToolBar(slideways)
        self.toolBar.setMovable(False)
        self.toolBar.setFloatable(False)
        self.toolBar.setObjectName("toolBar")
        slideways.addToolBar(Qt.TopToolBarArea, self.toolBar)
        self.actionNew_Game = QAction(slideways)
        self.actionNew_Game.setObjectName("actionNew_Game")
        self.action_Exit = QAction(slideways)
        self.action_Exit.setObjectName("action_Exit")
        self.action_Player = QAction(slideways)
        self.action_Player.setObjectName("action_Player")
        self.action_IA = QAction(slideways)
        self.action_IA.setObjectName("action_IA")
        self.action_IAvsIA = QAction(slideways)
        self.action_IAvsIA.setObjectName("action_IAvsIA")
        self.menuNew.addAction(self.actionNew_Game)
        self.menuNew.addAction(self.action_Player)
        self.menuNew.addAction(self.action_IA)
        self.menuNew.addAction(self.action_IAvsIA)
        self.menuNew.addSeparator()
        self.menuNew.addSeparator()
        self.menuNew.addAction(self.action_Exit)
        self.menubar.addAction(self.menuNew.menuAction())
        self.toolBar.addAction(self.actionNew_Game)
        self.toolBar.addAction(self.action_Player)
        self.toolBar.addAction(self.action_IA)
        self.toolBar.addAction(self.action_IAvsIA)
        self.label_timer = QLabel("  IA Speed : ")
        self.toolBar.addWidget(self.label_timer)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setGeometry(0, 0, 200, 20)
        self.toolBar.addWidget(self.slider)
        self.label_ms = QLabel("100ms")
        self.toolBar.addWidget(self.label_ms)

        self.retranslateUi(slideways)
        QMetaObject.connectSlotsByName(slideways)

    def retranslateUi(self, slideways):
        _translate = QCoreApplication.translate
        slideways.setWindowTitle(_translate("slideways", "Slideways"))
        self.menuNew.setTitle(_translate("slideways", "&Menu"))
        self.toolBar.setWindowTitle(_translate("slideways", "toolBar"))
        self.action_Player.setText(_translate("Slideways", "Human vs Human"))
        self.action_IA.setText(_translate("Slideways", "Human vs IA"))
        self.action_IAvsIA.setText(_translate("Slideways", "IA vs IA"))
        self.actionNew_Game.setText(_translate("slideways", "New Game"))
        self.action_Exit.setText(_translate("slideways", "Exit"))

