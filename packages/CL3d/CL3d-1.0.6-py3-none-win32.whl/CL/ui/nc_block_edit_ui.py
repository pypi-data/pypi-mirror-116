# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nc_block_edit_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(350, 438)
        Dialog.setMinimumSize(QtCore.QSize(350, 219))
        Dialog.setMaximumSize(QtCore.QSize(350, 1000))
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_info = QtWidgets.QLabel(Dialog)
        self.label_info.setMinimumSize(QtCore.QSize(0, 40))
        self.label_info.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_info.setFont(font)
        self.label_info.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_info.setStyleSheet("")
        self.label_info.setAlignment(QtCore.Qt.AlignCenter)
        self.label_info.setObjectName("label_info")
        self.verticalLayout.addWidget(self.label_info)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setMinimumSize(QtCore.QSize(328, 120))
        self.groupBox.setMaximumSize(QtCore.QSize(328, 99999))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.doubleSpinBox_x = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_x.setDecimals(6)
        self.doubleSpinBox_x.setMinimum(-999999.0)
        self.doubleSpinBox_x.setMaximum(999999.0)
        self.doubleSpinBox_x.setSingleStep(1.0)
        self.doubleSpinBox_x.setObjectName("doubleSpinBox_x")
        self.gridLayout.addWidget(self.doubleSpinBox_x, 0, 1, 1, 1)
        self.doubleSpinBox_y = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_y.setDecimals(6)
        self.doubleSpinBox_y.setMinimum(-999999.0)
        self.doubleSpinBox_y.setMaximum(999999.0)
        self.doubleSpinBox_y.setStepType(QtWidgets.QAbstractSpinBox.DefaultStepType)
        self.doubleSpinBox_y.setObjectName("doubleSpinBox_y")
        self.gridLayout.addWidget(self.doubleSpinBox_y, 1, 1, 1, 1)
        self.label_z_5 = QtWidgets.QLabel(self.groupBox)
        self.label_z_5.setStyleSheet("")
        self.label_z_5.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.label_z_5.setObjectName("label_z_5")
        self.gridLayout.addWidget(self.label_z_5, 6, 0, 1, 1)
        self.label_z_3 = QtWidgets.QLabel(self.groupBox)
        self.label_z_3.setStyleSheet("")
        self.label_z_3.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.label_z_3.setObjectName("label_z_3")
        self.gridLayout.addWidget(self.label_z_3, 4, 0, 1, 1)
        self.label_z_4 = QtWidgets.QLabel(self.groupBox)
        self.label_z_4.setStyleSheet("")
        self.label_z_4.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.label_z_4.setObjectName("label_z_4")
        self.gridLayout.addWidget(self.label_z_4, 5, 0, 1, 1)
        self.label_y = QtWidgets.QLabel(self.groupBox)
        self.label_y.setStyleSheet("")
        self.label_y.setObjectName("label_y")
        self.gridLayout.addWidget(self.label_y, 1, 0, 1, 1)
        self.label_z = QtWidgets.QLabel(self.groupBox)
        self.label_z.setStyleSheet("")
        self.label_z.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.label_z.setObjectName("label_z")
        self.gridLayout.addWidget(self.label_z, 2, 0, 1, 1)
        self.label_x = QtWidgets.QLabel(self.groupBox)
        self.label_x.setStyleSheet("")
        self.label_x.setObjectName("label_x")
        self.gridLayout.addWidget(self.label_x, 0, 0, 1, 1)
        self.doubleSpinBox_z = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_z.setDecimals(6)
        self.doubleSpinBox_z.setMinimum(-999999.0)
        self.doubleSpinBox_z.setMaximum(999999.0)
        self.doubleSpinBox_z.setObjectName("doubleSpinBox_z")
        self.gridLayout.addWidget(self.doubleSpinBox_z, 2, 1, 1, 1)
        self.doubleSpinBox_i = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_i.setDecimals(6)
        self.doubleSpinBox_i.setMinimum(-999999.0)
        self.doubleSpinBox_i.setMaximum(999999.0)
        self.doubleSpinBox_i.setObjectName("doubleSpinBox_i")
        self.gridLayout.addWidget(self.doubleSpinBox_i, 3, 1, 1, 1)
        self.doubleSpinBox_j = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_j.setDecimals(6)
        self.doubleSpinBox_j.setMinimum(-999999.0)
        self.doubleSpinBox_j.setMaximum(999999.0)
        self.doubleSpinBox_j.setObjectName("doubleSpinBox_j")
        self.gridLayout.addWidget(self.doubleSpinBox_j, 4, 1, 1, 1)
        self.doubleSpinBox_a = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_a.setDecimals(6)
        self.doubleSpinBox_a.setMinimum(-999999.0)
        self.doubleSpinBox_a.setMaximum(999999.0)
        self.doubleSpinBox_a.setObjectName("doubleSpinBox_a")
        self.gridLayout.addWidget(self.doubleSpinBox_a, 6, 1, 1, 1)
        self.doubleSpinBox_k = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_k.setDecimals(6)
        self.doubleSpinBox_k.setMinimum(-999999.0)
        self.doubleSpinBox_k.setMaximum(999999.0)
        self.doubleSpinBox_k.setObjectName("doubleSpinBox_k")
        self.gridLayout.addWidget(self.doubleSpinBox_k, 5, 1, 1, 1)
        self.label_z_2 = QtWidgets.QLabel(self.groupBox)
        self.label_z_2.setStyleSheet("")
        self.label_z_2.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.label_z_2.setObjectName("label_z_2")
        self.gridLayout.addWidget(self.label_z_2, 3, 0, 1, 1)
        self.doubleSpinBox_c = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_c.setDecimals(6)
        self.doubleSpinBox_c.setMinimum(-999999.0)
        self.doubleSpinBox_c.setMaximum(999999.0)
        self.doubleSpinBox_c.setObjectName("doubleSpinBox_c")
        self.gridLayout.addWidget(self.doubleSpinBox_c, 7, 1, 1, 1)
        self.label_z_6 = QtWidgets.QLabel(self.groupBox)
        self.label_z_6.setStyleSheet("")
        self.label_z_6.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.label_z_6.setObjectName("label_z_6")
        self.gridLayout.addWidget(self.label_z_6, 7, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_ok = QtWidgets.QPushButton(self.frame)
        self.pushButton_ok.setAutoDefault(False)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.horizontalLayout.addWidget(self.pushButton_ok)
        self.pushButton_reset = QtWidgets.QPushButton(self.frame)
        self.pushButton_reset.setAutoDefault(False)
        self.pushButton_reset.setObjectName("pushButton_reset")
        self.horizontalLayout.addWidget(self.pushButton_reset)
        self.pushButton_app = QtWidgets.QPushButton(self.frame)
        self.pushButton_app.setAutoDefault(False)
        self.pushButton_app.setObjectName("pushButton_app")
        self.horizontalLayout.addWidget(self.pushButton_app)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "单边编辑"))
        self.label_info.setText(_translate("Dialog", "请选择单条边"))
        self.groupBox.setTitle(_translate("Dialog", "位置坐标"))
        self.label_z_5.setText(_translate("Dialog", "A"))
        self.label_z_3.setText(_translate("Dialog", "J(绿)"))
        self.label_z_4.setText(_translate("Dialog", "K(蓝)"))
        self.label_y.setText(_translate("Dialog", "Y(绿)"))
        self.label_z.setText(_translate("Dialog", "Z(蓝)"))
        self.label_x.setText(_translate("Dialog", "X(红)"))
        self.label_z_2.setText(_translate("Dialog", "I(红)"))
        self.label_z_6.setText(_translate("Dialog", "C"))
        self.pushButton_ok.setText(_translate("Dialog", "确定"))
        self.pushButton_reset.setText(_translate("Dialog", "重置"))
        self.pushButton_app.setText(_translate("Dialog", "应用"))
