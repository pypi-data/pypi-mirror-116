# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'data_merge_vertical.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from resources import pyqtsource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setWindowModality(Qt.ApplicationModal)
        Form.resize(800, 600)
        Form.setMinimumSize(QSize(0, 0))
        Form.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(Form)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.widget = QWidget(self.splitter)
        self.widget.setObjectName(u"widget")
        self.widget.setMaximumSize(QSize(300, 16777215))
        self.verticalLayout_10 = QVBoxLayout(self.widget)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.label_username_2 = QLabel(self.widget)
        self.label_username_2.setObjectName(u"label_username_2")

        self.verticalLayout_10.addWidget(self.label_username_2)

        self.listWidget_dataset = QListWidget(self.widget)
        self.listWidget_dataset.setObjectName(u"listWidget_dataset")
        self.listWidget_dataset.setAcceptDrops(True)

        self.verticalLayout_10.addWidget(self.listWidget_dataset)

        self.splitter.addWidget(self.widget)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout_8 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.pushButton_insert_start = QPushButton(self.layoutWidget)
        self.pushButton_insert_start.setObjectName(u"pushButton_insert_start")
        self.pushButton_insert_start.setMaximumSize(QSize(50, 16777215))
        icon = QIcon()
        icon.addFile(u":/pyqt/source/images/right.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_insert_start.setIcon(icon)

        self.horizontalLayout_6.addWidget(self.pushButton_insert_start)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_username_3 = QLabel(self.layoutWidget)
        self.label_username_3.setObjectName(u"label_username_3")

        self.verticalLayout_6.addWidget(self.label_username_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.listWidget_start = QListWidget(self.layoutWidget)
        self.listWidget_start.setObjectName(u"listWidget_start")
        self.listWidget_start.setAcceptDrops(True)

        self.verticalLayout_2.addWidget(self.listWidget_start)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.pushButton_start_add = QPushButton(self.layoutWidget)
        self.pushButton_start_add.setObjectName(u"pushButton_start_add")
        self.pushButton_start_add.setMaximumSize(QSize(50, 16777215))
        icon1 = QIcon()
        icon1.addFile(u":/pyqt/source/images/add.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_start_add.setIcon(icon1)

        self.verticalLayout_3.addWidget(self.pushButton_start_add)

        self.pushButton_start_up = QPushButton(self.layoutWidget)
        self.pushButton_start_up.setObjectName(u"pushButton_start_up")
        self.pushButton_start_up.setMaximumSize(QSize(50, 16777215))
        icon2 = QIcon()
        icon2.addFile(u":/pyqt/source/images/up1.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_start_up.setIcon(icon2)

        self.verticalLayout_3.addWidget(self.pushButton_start_up)

        self.pushButton_start_down = QPushButton(self.layoutWidget)
        self.pushButton_start_down.setObjectName(u"pushButton_start_down")
        self.pushButton_start_down.setMaximumSize(QSize(50, 16777215))
        icon3 = QIcon()
        icon3.addFile(u":/pyqt/source/images/down1.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_start_down.setIcon(icon3)

        self.verticalLayout_3.addWidget(self.pushButton_start_down)

        self.pushButton_start_del = QPushButton(self.layoutWidget)
        self.pushButton_start_del.setObjectName(u"pushButton_start_del")
        self.pushButton_start_del.setMaximumSize(QSize(50, 16777215))
        icon4 = QIcon()
        icon4.addFile(u":/pyqt/source/images/lc_delete.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_start_del.setIcon(icon4)

        self.verticalLayout_3.addWidget(self.pushButton_start_del)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_6.addLayout(self.verticalLayout_6)


        self.verticalLayout_8.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushButton_insert_append = QPushButton(self.layoutWidget)
        self.pushButton_insert_append.setObjectName(u"pushButton_insert_append")
        self.pushButton_insert_append.setMaximumSize(QSize(50, 16777215))
        self.pushButton_insert_append.setIcon(icon)

        self.horizontalLayout_5.addWidget(self.pushButton_insert_append)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_username_4 = QLabel(self.layoutWidget)
        self.label_username_4.setObjectName(u"label_username_4")

        self.verticalLayout_7.addWidget(self.label_username_4)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.listWidget_append = QListWidget(self.layoutWidget)
        self.listWidget_append.setObjectName(u"listWidget_append")
        self.listWidget_append.setAcceptDrops(True)

        self.verticalLayout_4.addWidget(self.listWidget_append)


        self.horizontalLayout_4.addLayout(self.verticalLayout_4)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.pushButton_append_add = QPushButton(self.layoutWidget)
        self.pushButton_append_add.setObjectName(u"pushButton_append_add")
        self.pushButton_append_add.setMaximumSize(QSize(50, 16777215))
        self.pushButton_append_add.setIcon(icon1)

        self.verticalLayout_5.addWidget(self.pushButton_append_add)

        self.pushButton_append_up = QPushButton(self.layoutWidget)
        self.pushButton_append_up.setObjectName(u"pushButton_append_up")
        self.pushButton_append_up.setMaximumSize(QSize(50, 16777215))
        self.pushButton_append_up.setIcon(icon2)

        self.verticalLayout_5.addWidget(self.pushButton_append_up)

        self.pushButton_append_down = QPushButton(self.layoutWidget)
        self.pushButton_append_down.setObjectName(u"pushButton_append_down")
        self.pushButton_append_down.setMaximumSize(QSize(50, 16777215))
        self.pushButton_append_down.setIcon(icon3)

        self.verticalLayout_5.addWidget(self.pushButton_append_down)

        self.pushButton_append_del = QPushButton(self.layoutWidget)
        self.pushButton_append_del.setObjectName(u"pushButton_append_del")
        self.pushButton_append_del.setMaximumSize(QSize(50, 16777215))
        self.pushButton_append_del.setIcon(icon4)

        self.verticalLayout_5.addWidget(self.pushButton_append_del)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)


        self.horizontalLayout_4.addLayout(self.verticalLayout_5)


        self.verticalLayout_7.addLayout(self.horizontalLayout_4)


        self.horizontalLayout_5.addLayout(self.verticalLayout_7)


        self.verticalLayout_8.addLayout(self.horizontalLayout_5)

        self.splitter.addWidget(self.layoutWidget)

        self.verticalLayout.addWidget(self.splitter)

        self.widget_2 = QWidget(Form)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMinimumSize(QSize(0, 50))
        self.widget_2.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_code = QPushButton(self.widget_2)
        self.pushButton_code.setObjectName(u"pushButton_code")

        self.horizontalLayout.addWidget(self.pushButton_code)

        self.pushButton_help = QPushButton(self.widget_2)
        self.pushButton_help.setObjectName(u"pushButton_help")
        icon5 = QIcon()
        icon5.addFile(u":/pyqt/source/images/lc_helpindex.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_help.setIcon(icon5)

        self.horizontalLayout.addWidget(self.pushButton_help)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton_ok = QPushButton(self.widget_2)
        self.pushButton_ok.setObjectName(u"pushButton_ok")

        self.horizontalLayout.addWidget(self.pushButton_ok)

        self.pushButton_save = QPushButton(self.widget_2)
        self.pushButton_save.setObjectName(u"pushButton_save")

        self.horizontalLayout.addWidget(self.pushButton_save)

        self.pushButton_cancel = QPushButton(self.widget_2)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")

        self.horizontalLayout.addWidget(self.pushButton_cancel)


        self.verticalLayout.addWidget(self.widget_2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u6570\u636e\u5408\u5e76-\u7eb5\u5411\u5408\u5e76", None))
        self.label_username_2.setText(QCoreApplication.translate("Form", u"\u53ef\u9009\u6570\u636e\u96c6\uff1a", None))
        self.pushButton_insert_start.setText("")
        self.label_username_3.setText(QCoreApplication.translate("Form", u"\u8d77\u59cb\u6570\u636e\u96c6:", None))
        self.pushButton_start_add.setText("")
        self.pushButton_start_up.setText("")
        self.pushButton_start_down.setText("")
        self.pushButton_start_del.setText("")
        self.pushButton_insert_append.setText("")
        self.label_username_4.setText(QCoreApplication.translate("Form", u"\u7528\u6765\u7eb5\u5411\u5408\u5e76\u7684\u6570\u636e\u96c6:", None))
        self.pushButton_append_add.setText("")
        self.pushButton_append_up.setText("")
        self.pushButton_append_down.setText("")
        self.pushButton_append_del.setText("")
        self.pushButton_code.setText(QCoreApplication.translate("Form", u"\u4ee3\u7801", None))
        self.pushButton_help.setText("")
        self.pushButton_ok.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
        self.pushButton_save.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88", None))
    # retranslateUi

