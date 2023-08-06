import os
import sys

from PySide2.QtCore import QSettings, QTranslator
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QWidget, QMessageBox, QApplication, QFileDialog, QStyleFactory

from features.ui.base.Preferences import Ui_Form
from utils import *


class Preferences(QWidget, Ui_Form):
    def __init__(self):
        super(Preferences, self).__init__()
        self.setupUi(self)

        self.pushButton_ok.clicked.connect(self.save_settings)
        self.toolButton_workspace.clicked.connect(self.change_workspace_path)
        self.toolButton_output.clicked.connect(self.change_output_path)
        self.comboBox_language.currentIndexChanged.connect(self.change_lang)
        self.comboBox_theme.currentIndexChanged.connect(self.change_theme)

        # load settings
        self.settings = QSettings("config.ini", QSettings.IniFormat)
        self.theme = self.settings.value("MAIN/THEME")
        self.language = self.settings.value("MAIN/LANGUAGE")
        self.path_workspace = self.settings.value("MAIN/PATH_WORKDIR")
        self.path_output = self.settings.value("MAIN/PATH_OUTPUT")
        self.path_interpreter = self.settings.value("MAIN/INTERPRETER")
        self.if_display_startpage = self.settings.value("MAIN/STARTPAGE")

        self.comboBox_theme.setCurrentText(self.theme)
        self.lineEdit_worksapce.setText(self.path_workspace)
        self.lineEdit_output.setText(self.path_output)

        # 设置语言
        if self.language == "zh_CN":
            self.comboBox_language.setCurrentText("简体中文")
        elif self.language == "en":
            self.comboBox_language.setCurrentText("English")

        # 设置显示快速启动页
        if self.if_display_startpage == "True":
            self.checkBox_startpage.setChecked(True)
        else:
            self.checkBox_startpage.setChecked(False)

        # 设置解释器路径
        if self.path_interpreter:
            print(self.path_interpreter)
        else:
            self.path_interpreter = sys.executable
            print(self.path_interpreter)

        # 设置工作目录
        if self.path_workspace:
            self.lineEdit_worksapce.setText(self.path_workspace)
        else:
            self.path_workspace = os.path.join(get_documents_dir(), 'PyMiner Workspace')
            self.lineEdit_worksapce.setText(self.path_workspace)

        # 设置输出目录
        if self.path_output:
            self.lineEdit_output.setText(self.path_workspace)
        else:
            self.path_output = os.path.join(get_documents_dir(), 'PyMiner Workspace', 'output')
            self.lineEdit_output.setText(self.path_output)

    def change_fontsize(self):
        font = QFont()
        font.setPointSize(int(self.spinBox.value()))
        self.plainTextEdit.setFont(font)

    def save_settings(self):

        self.theme = self.comboBox_theme.currentText()
        self.path_workspace = self.lineEdit_worksapce.text()
        self.path_output = self.lineEdit_output.text()
        self.interpreter="d:/pyminer/python.exe"

        # 保存 语言设置

        if self.comboBox_language.currentText() == "简体中文":
            self.language = "zh_CN"
        else:
            self.language = "en"

        # 保存 是否显示‘快速启动页’
        if self.checkBox_startpage.isChecked():
            self.if_display_startpage = "True"
        else:
            self.if_display_startpage = "False"

        self.settings.setValue("MAIN/THEME", self.theme)
        self.settings.setValue("MAIN/LANGUAGE", self.language)
        self.settings.setValue("MAIN/PATH_WORKSPACE", self.path_workspace)
        self.settings.setValue("MAIN/PATH_OUTPUT", self.path_output)
        self.settings.setValue("MAIN/INTERPRETER", self.interpreter)
        self.settings.setValue("MAIN/STARTPAGE", self.if_display_startpage)

        # if self.comboBox.currentText()=='简体中文':
        #     self.language ='zh_CN'
        # else:
        #     self.language = 'English'
        # self.settings.setValue("General/Language", self.language)
        QMessageBox.information(self, "提示", "设置内容已保存，重启后生效！")

    def change_workspace_path(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select a directory as workspace", os.path.expanduser('~'))
        self.lineEdit_worksapce.setText(dir_path)

    def change_output_path(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select a directory as output location",
                                                    os.path.expanduser('~'))
        self.lineEdit_output.setText(dir_path)

    def change_lang(self):
        if self.comboBox.currentText() == 'English':
            trans = QTranslator()
            trans.load('English.qm')
            app.installTranslator(trans)
            self.retranslateUi(self)

        else:
            trans = QTranslator()
            trans.load('zh_CN.qm')
            app.installTranslator(trans)
            self.retranslateUi(self)

    def change_theme(self):
        if self.comboBox_theme.currentText()=="Fusion":
            QApplication.setStyle(QStyleFactory.create("Fusion"))
        else:
            QApplication.setStyle(QStyleFactory.create("windowsvista"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Preferences()
    form.show()
    sys.exit(app.exec_())
