import datetime
import webbrowser
import numpy as np
import pandas as pd

# 导入PyQt5模块
from PySide2.QtCore import QSize, Qt, Signal
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QHBoxLayout, QWidget, QSpacerItem, QToolButton, QSizePolicy, QWizard, QMessageBox, \
    QFileDialog, QFrame, QDesktopWidget, QDialog, QTableWidgetItem, QInputDialog, QAbstractItemView, QLineEdit, \
    QApplication

# 导入数据相关操作模块
from packages.pm_preprocess.ui.data_row_filter import Ui_Form as DataRowFilter_Ui_Form  # # 数据筛选

class DataFilterForm(QDialog, DataRowFilter_Ui_Form):
    """
    打开"数据-行筛选"窗口
    """
    signal_data_change = Signal(str, dict)  # 自定义信号，用于修改数据 变量名，数据集

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()

        # 变量初始化
        self.current_dataset = pd.DataFrame()
        self.current_dataset_name = ''
        self.current_dataset_columns = []
        self.data_type = []
        self.filter_dataset = pd.DataFrame()  # 执行筛选后的数据集

        # 绑定事件
        self.comboBox_random.currentIndexChanged.connect(self.filter_random_label)  # 按比例随机抽样时，显示%，否则隐藏%
        self.lineEdit_col_find.textChanged.connect(self.filter_column_partter)
        self.pushButton_ok.clicked.connect(self.dataset_update)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_help.clicked.connect(self.get_help)

        # 动态刷新查询结果
        self.comboBox_random.currentIndexChanged.connect(self.exec_filter)
        self.comboBox_replace.currentIndexChanged.connect(self.exec_filter)
        self.radioButton_random.toggled.connect(self.exec_filter)
        self.radioButton_simple.toggled.connect(self.exec_filter)
        self.spinBox_end.valueChanged.connect(self.exec_filter)
        self.spinBox_start.valueChanged.connect(self.exec_filter)
        self.spinBox_random_state.valueChanged.connect(self.exec_filter)
        self.spinBox_random.valueChanged.connect(self.exec_filter)
        self.radioButton_column.toggled.connect(self.exec_filter)
        self.radioButton_dtype.toggled.connect(self.exec_filter)
        self.comboBox_columns.currentTextChanged.connect(self.exec_filter)
        self.comboBox_col_condition.currentTextChanged.connect(self.exec_filter)
        self.lineEdit_col_find.textChanged.connect(self.exec_filter)
        self.comboBox_dtype.currentIndexChanged.connect(self.exec_filter)

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            reply = QMessageBox.question(self, '确认退出？', '是否退出当前窗口？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.close()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))

    def get_help(self):
        """
        打开帮助页面
        """
        try:
            webbrowser.get('chrome').open_new_tab("http://www.pyminer.com")
        except Exception as e:
            webbrowser.open_new_tab("http://www.pyminer.com")

    def dataset_init(self):
        self.filter_dataset = self.current_dataset.copy().head(100)
        self.tableWidget_dataset.setColumnCount(len(self.filter_dataset.columns))
        self.tableWidget_dataset.setRowCount(len(self.filter_dataset.index))
        self.tableWidget_dataset.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_dataset.setHorizontalHeaderLabels(self.filter_dataset.columns.values.tolist())

        for i in range(len(self.filter_dataset.index)):
            for j in range(len(self.filter_dataset.columns)):
                self.tableWidget_dataset.setItem(i, j, QTableWidgetItem(str(self.filter_dataset.iat[i, j])))

        for x in range(self.tableWidget_dataset.columnCount()):
            headItem = self.tableWidget_dataset.horizontalHeaderItem(x)  # 获得水平方向表头的Item对象

            headItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def data_preview(self, dataset):
        # 获取当前数据集
        data = dataset.head(100)
        self.tableWidget_dataset.setColumnCount(len(data.columns))
        self.tableWidget_dataset.setRowCount(len(data.index))
        self.tableWidget_dataset.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_dataset.setHorizontalHeaderLabels(data.columns.values.tolist())

        for i in range(len(data.index)):
            for j in range(len(data.columns)):
                self.tableWidget_dataset.setItem(i, j, QTableWidgetItem(str(data.iat[i, j])))

        for x in range(self.tableWidget_dataset.columnCount()):
            headItem = self.tableWidget_dataset.horizontalHeaderItem(x)  # 获得水平方向表头的Item对象

            headItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def filter_simple(self):
        dataset = self.current_dataset.copy()
        # 简单过滤
        int_start = int(self.spinBox_start.value())
        int_end = int(self.spinBox_end.value())
        if 1 <= int_start <= dataset.shape[1]:
            if int_end >= 1 and int_end >= int_start:
                print(dataset.shape)
                self.filter_dataset = dataset.iloc[int_start - 1:int_end]
                self.data_preview(self.filter_dataset)
            else:
                QMessageBox.warning(self, '注意', '输入的结束位置无效', QMessageBox.Yes)
        else:
            QMessageBox.warning(self, '注意', '输入的开始位置无效', QMessageBox.Yes)

    def filter_random_label(self):
        if self.comboBox_random.currentText() == "按比例随机抽样":
            self.label_random.setHidden(False)
        elif self.comboBox_random.currentText() == "按行数随机抽样":
            self.label_random.setHidden(True)

    def filter_random(self):
        # 随机抽样
        dataset = self.current_dataset.copy()
        if self.comboBox_replace.currentText() == "有放回抽样":
            random_replace = True
        else:
            random_replace = False

        random_random_state = int(self.spinBox_random_state.value())
        if self.comboBox_random.currentText() == "按比例随机抽样":
            # 抽取行的比例
            random_func = float(self.spinBox_random.value()) / 100

            self.filter_dataset = dataset.sample(n=None,
                                                 frac=random_func,
                                                 replace=random_replace,
                                                 random_state=random_random_state)
        else:
            # 要抽取的行数
            random_func = int(self.lineEdit_random.text())
            self.filter_dataset = dataset.sample(n=random_func,
                                                 frac=None,
                                                 replace=random_replace,
                                                 random_state=random_random_state)

        self.data_preview(self.filter_dataset)  # 刷新预览数据

    def filter_column_partter(self):
        content = self.lineEdit_col_find.text()
        if content.isdigit():
            self.comboBox_col_condition.clear()
            self.comboBox_col_condition.addItems(['模糊匹配', 'in', 'not in', '=', '>', '>=', '<', '<='])
        else:
            self.comboBox_col_condition.clear()
            self.comboBox_col_condition.addItems(['模糊匹配', 'in', 'not in'])

    def filter_column(self):
        # 根据列筛选
        data = self.current_dataset.copy()
        col = self.comboBox_columns.currentText()
        content = self.lineEdit_col_find.text()
        if self.comboBox_columns.currentText() != "变量列表":
            if content.isdigit():  # 判断列的筛选条件是否为数值
                if self.comboBox_col_condition.currentText() == "=":
                    self.filter_dataset = data[data[col] == float(content)]
                elif self.comboBox_col_condition.currentText() == ">":
                    self.filter_dataset = data[data[col] > float(content)]
                elif self.comboBox_col_condition.currentText() == ">=":
                    self.filter_dataset = data[data[col] >= float(content)]
                elif self.comboBox_col_condition.currentText() == "<":
                    self.filter_dataset = data[data[col] < float(content)]
                elif self.comboBox_col_condition.currentText() == "<=":
                    self.filter_dataset = data[data[col] <= float(content)]
            else:
                content = content.lower()
                if self.comboBox_col_condition.currentText() == "模糊匹配":
                    self.filter_dataset = data[data[col].map(str.lower).str.contains(content)]
                elif self.comboBox_col_condition.currentText() == "in":
                    self.filter_dataset = data[data[col].isin(content.split(','))]
                elif self.comboBox_col_condition.currentText() == "not in":
                    self.filter_dataset = data[~data[col].isin(content.split(','))]
        self.data_preview(self.filter_dataset)

    def filter_dtype(self):
        data = self.current_dataset.copy()
        dtype = self.comboBox_dtype.currentText()  # 当前要筛选的数据类型
        if dtype == "全部":
            self.data_preview(data)
            return
        self.filter_dataset = data.select_dtypes(include=dtype)
        self.data_preview(self.filter_dataset)

    def filter_default(self):
        self.filter_dataset = self.current_dataset.copy()
        self.data_preview(self.filter_dataset)

    def exec_filter(self):
        if self.radioButton_simple.isChecked():
            self.filter_simple()
        elif self.radioButton_random.isChecked():
            self.filter_random()
        elif self.radioButton_column.isChecked():
            self.filter_column()
        elif self.radioButton_dtype.isChecked():
            self.filter_dtype()
        else:
            self.filter_default()


    def dataset_update(self):
        self.exec_filter()
        reply = QMessageBox.information(self, "注意", "是否保存当前筛选结果到工作区间并覆盖原数据", QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
        if reply == QMessageBox.Yes:
            if len(self.filter_dataset) > 0:
                self.signal_data_change.emit(self.current_dataset_name,self.filter_dataset.to_dict())
        else:
            default_name = self.current_dataset_name.split('.')[0] + '_new'
            dataset_name, ok = QInputDialog.getText(self, "另存为", "新变量名称:", QLineEdit.Normal, default_name)
            if ok and (len(dataset_name) != 0):
                self.signal_data_change.emit(dataset_name, self.filter_dataset.to_dict())

