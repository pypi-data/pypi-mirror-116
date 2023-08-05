# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'geo_edit_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(350, 520)
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
        self.groupBox.setMaximumSize(QtCore.QSize(328, 120))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label_x = QtWidgets.QLabel(self.groupBox)
        self.label_x.setStyleSheet("")
        self.label_x.setObjectName("label_x")
        self.gridLayout.addWidget(self.label_x, 0, 0, 1, 1)
        self.label_y = QtWidgets.QLabel(self.groupBox)
        self.label_y.setStyleSheet("")
        self.label_y.setObjectName("label_y")
        self.gridLayout.addWidget(self.label_y, 1, 0, 1, 1)
        self.doubleSpinBox_x = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_x.setDecimals(6)
        self.doubleSpinBox_x.setMinimum(-999999.0)
        self.doubleSpinBox_x.setMaximum(999999.0)
        self.doubleSpinBox_x.setSingleStep(1.0)
        self.doubleSpinBox_x.setObjectName("doubleSpinBox_x")
        self.gridLayout.addWidget(self.doubleSpinBox_x, 0, 1, 1, 1)
        self.label_z = QtWidgets.QLabel(self.groupBox)
        self.label_z.setStyleSheet("")
        self.label_z.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.label_z.setObjectName("label_z")
        self.gridLayout.addWidget(self.label_z, 2, 0, 1, 1)
        self.doubleSpinBox_y = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_y.setDecimals(6)
        self.doubleSpinBox_y.setMinimum(-999999.0)
        self.doubleSpinBox_y.setMaximum(999999.0)
        self.doubleSpinBox_y.setStepType(QtWidgets.QAbstractSpinBox.DefaultStepType)
        self.doubleSpinBox_y.setObjectName("doubleSpinBox_y")
        self.gridLayout.addWidget(self.doubleSpinBox_y, 1, 1, 1, 1)
        self.doubleSpinBox_z = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_z.setDecimals(6)
        self.doubleSpinBox_z.setMinimum(-999999.0)
        self.doubleSpinBox_z.setMaximum(999999.0)
        self.doubleSpinBox_z.setObjectName("doubleSpinBox_z")
        self.gridLayout.addWidget(self.doubleSpinBox_z, 2, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.pushButton_coord = QtWidgets.QPushButton(Dialog)
        self.pushButton_coord.setAutoDefault(False)
        self.pushButton_coord.setObjectName("pushButton_coord")
        self.verticalLayout.addWidget(self.pushButton_coord)
        self.groupBox_geoinfo = QtWidgets.QGroupBox(Dialog)
        self.groupBox_geoinfo.setMinimumSize(QtCore.QSize(328, 200))
        self.groupBox_geoinfo.setMaximumSize(QtCore.QSize(328, 200))
        self.groupBox_geoinfo.setObjectName("groupBox_geoinfo")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_geoinfo)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_5 = QtWidgets.QLabel(self.groupBox_geoinfo)
        self.label_5.setStyleSheet("")
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)
        self.doubleSpinBox_angle = QtWidgets.QDoubleSpinBox(self.groupBox_geoinfo)
        self.doubleSpinBox_angle.setDecimals(6)
        self.doubleSpinBox_angle.setMinimum(-360.0)
        self.doubleSpinBox_angle.setMaximum(360.0)
        self.doubleSpinBox_angle.setObjectName("doubleSpinBox_angle")
        self.gridLayout_2.addWidget(self.doubleSpinBox_angle, 3, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox_geoinfo)
        self.label_4.setStyleSheet("")
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.doubleSpinBox_w = QtWidgets.QDoubleSpinBox(self.groupBox_geoinfo)
        self.doubleSpinBox_w.setDecimals(6)
        self.doubleSpinBox_w.setMinimum(0.01)
        self.doubleSpinBox_w.setMaximum(999999.0)
        self.doubleSpinBox_w.setObjectName("doubleSpinBox_w")
        self.gridLayout_2.addWidget(self.doubleSpinBox_w, 2, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox_geoinfo)
        self.label_6.setStyleSheet("")
        self.label_6.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 2, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox_geoinfo)
        self.label_7.setStyleSheet("")
        self.label_7.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 3, 0, 1, 1)
        self.doubleSpinBox_r = QtWidgets.QDoubleSpinBox(self.groupBox_geoinfo)
        self.doubleSpinBox_r.setDecimals(6)
        self.doubleSpinBox_r.setMinimum(0.0)
        self.doubleSpinBox_r.setMaximum(999999.0)
        self.doubleSpinBox_r.setSingleStep(1.0)
        self.doubleSpinBox_r.setObjectName("doubleSpinBox_r")
        self.gridLayout_2.addWidget(self.doubleSpinBox_r, 0, 1, 1, 1)
        self.doubleSpinBox_len = QtWidgets.QDoubleSpinBox(self.groupBox_geoinfo)
        self.doubleSpinBox_len.setDecimals(6)
        self.doubleSpinBox_len.setMinimum(0.01)
        self.doubleSpinBox_len.setMaximum(999999.0)
        self.doubleSpinBox_len.setStepType(QtWidgets.QAbstractSpinBox.DefaultStepType)
        self.doubleSpinBox_len.setObjectName("doubleSpinBox_len")
        self.gridLayout_2.addWidget(self.doubleSpinBox_len, 1, 1, 1, 1)
        self.doubleSpinBox_microLink = QtWidgets.QDoubleSpinBox(self.groupBox_geoinfo)
        self.doubleSpinBox_microLink.setDecimals(6)
        self.doubleSpinBox_microLink.setMinimum(-360.0)
        self.doubleSpinBox_microLink.setMaximum(360.0)
        self.doubleSpinBox_microLink.setObjectName("doubleSpinBox_microLink")
        self.gridLayout_2.addWidget(self.doubleSpinBox_microLink, 5, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox_geoinfo)
        self.label_8.setStyleSheet("")
        self.label_8.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 5, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_geoinfo)
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
        Dialog.setWindowTitle(_translate("Dialog", "标准孔编辑"))
        self.label_info.setText(_translate("Dialog", "请选择标准孔"))
        self.groupBox.setTitle(_translate("Dialog", "位置坐标"))
        self.label_x.setText(_translate("Dialog", "X"))
        self.label_y.setText(_translate("Dialog", "Y"))
        self.label_z.setText(_translate("Dialog", "Z"))
        self.pushButton_coord.setText(_translate("Dialog", "绝对坐标系"))
        self.groupBox_geoinfo.setTitle(_translate("Dialog", "几何属性"))
        self.label_5.setText(_translate("Dialog", "长度"))
        self.label_4.setText(_translate("Dialog", "半径"))
        self.label_6.setText(_translate("Dialog", "宽度"))
        self.label_7.setText(_translate("Dialog", "旋转角度"))
        self.label_8.setText(_translate("Dialog", "过切"))
        self.pushButton_ok.setText(_translate("Dialog", "确定"))
        self.pushButton_reset.setText(_translate("Dialog", "重置"))
        self.pushButton_app.setText(_translate("Dialog", "应用"))
