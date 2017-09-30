# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\GitRepos\OdsBfiStaging\GuiBuilder\OdsBfiStaging\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

import os
from PyQt5 import QtCore, QtGui, QtWidgets

from Ui_LoginDialog import Ui_LoginDialog
from Ui_CorrectionDialog import Ui_CorrectionDialog
from OdsTableReplacer import OdsTableReplacer
from LoadCreator import LoadCreator


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(785, 625)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("database-refresh.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox = QtWidgets.QGroupBox(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_2.addWidget(self.label_7)
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_2.addWidget(self.label_8)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lineEdit_LoginBfi = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_LoginBfi.setEnabled(False)
        self.lineEdit_LoginBfi.setObjectName("lineEdit_LoginBfi")
        self.verticalLayout_3.addWidget(self.lineEdit_LoginBfi)
        self.lineEdit_LoginOdsBfi = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_LoginOdsBfi.setEnabled(False)
        self.lineEdit_LoginOdsBfi.setObjectName("lineEdit_LoginOdsBfi")
        self.verticalLayout_3.addWidget(self.lineEdit_LoginOdsBfi)
        self.lineEdit_OutputPath = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_OutputPath.setEnabled(False)
        self.lineEdit_OutputPath.setObjectName("lineEdit_OutputPath")
        self.verticalLayout_3.addWidget(self.lineEdit_OutputPath)
        self.lineEdit_SchemaOds = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_SchemaOds.setObjectName("lineEdit_SchemaOds")
        self.verticalLayout_3.addWidget(self.lineEdit_SchemaOds)
        self.lineEdit_SchemaChk = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_SchemaChk.setObjectName("lineEdit_SchemaChk")
        self.verticalLayout_3.addWidget(self.lineEdit_SchemaChk)
        self.lineEdit_Staging = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_Staging.setObjectName("lineEdit_Staging")
        self.verticalLayout_3.addWidget(self.lineEdit_Staging)
        self.comboBox_Template = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_Template.setObjectName("comboBox_Template")
        self.verticalLayout_3.addWidget(self.comboBox_Template)
        self.comboBox_Execute = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_Execute.setObjectName("comboBox_Execute")
        self.verticalLayout_3.addWidget(self.comboBox_Execute)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_ConnectBfi = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_ConnectBfi.setObjectName("pushButton_ConnectBfi")
        self.verticalLayout.addWidget(self.pushButton_ConnectBfi)
        self.pushButton_ConnectOdsBfi = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_ConnectOdsBfi.setObjectName("pushButton_ConnectOdsBfi")
        self.verticalLayout.addWidget(self.pushButton_ConnectOdsBfi)
        self.pushButton_Browse = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_Browse.setObjectName("pushButton_Browse")
        self.verticalLayout.addWidget(self.pushButton_Browse)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.pushButton_Execute = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_Execute.setObjectName("pushButton_Execute")
        self.verticalLayout.addWidget(self.pushButton_Execute)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_4.addWidget(self.groupBox)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_6.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_6.setSpacing(6)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.textEdit_Info = QtWidgets.QTextEdit(self.groupBox_3)
        self.textEdit_Info.setEnabled(False)
        self.textEdit_Info.setObjectName("textEdit_Info")
        self.horizontalLayout_6.addWidget(self.textEdit_Info)
        self.verticalLayout_4.addWidget(self.groupBox_3)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 785, 21))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ODS BFI Staging Builder"))
        self.groupBox.setTitle(_translate("MainWindow", "Globale Einstellungen"))
        self.label_2.setText(_translate("MainWindow", "Login BFI:"))
        self.label_3.setText(_translate("MainWindow", "Login ODS - BFI:"))
        self.label_4.setText(_translate("MainWindow", "Script Output Pfad:"))
        self.label_5.setText(_translate("MainWindow", "Schemaname ODS:"))
        self.label_6.setText(_translate("MainWindow", "Schemaname CHK:"))
        self.label_7.setText(_translate("MainWindow", "Staging Name:"))
        self.label_8.setText(_translate("MainWindow", "Kunden Template Verzeichnis:"))
        self.label.setText(_translate("MainWindow", "Akionen Ausführen:"))
        self.pushButton_ConnectBfi.setText(_translate("MainWindow", "Connect"))
        self.pushButton_ConnectOdsBfi.setText(_translate("MainWindow", "Connect"))
        self.pushButton_Browse.setText(_translate("MainWindow", "Browse"))
        self.pushButton_Execute.setText(_translate("MainWindow", "Execute"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Info Log"))

    ##################################################################################################################

    def connect_user_signals(self):
        self.pushButton_ConnectBfi.clicked.connect(self.__connectBfi)
        self.pushButton_ConnectOdsBfi.clicked.connect(self.__connectOdsBfi)
        self.pushButton_Browse.clicked.connect(self.__browseScript)
        self.pushButton_Execute.clicked.connect(self.__execute)

        self.comboBox_Template.currentIndexChanged.connect(self.__cbo_template_changed)
        self.comboBox_Execute.currentIndexChanged.connect(self.__cbo_action_changed)

        self.lineEdit_SchemaChk.textChanged.connect(self.__update_parameters)
        self.lineEdit_SchemaOds.textChanged.connect(self.__update_parameters)
        self.lineEdit_Staging.textChanged.connect(self.__update_parameters)

    def init_user_data(self, globalOdsBfiStaging):
        self.globalOdsBfiStaging = globalOdsBfiStaging
        # cbo template abfuellen
        for index, text, user_data in self.globalOdsBfiStaging.getCbo_kunde_subdirectory_auswahl():
            self.comboBox_Template.addItem(text, userData=[index, user_data])
            if self.globalOdsBfiStaging.getTemplate_kunde_subdirectory() == user_data:
                self.comboBox_Template.setCurrentIndex(index)
        # cbo action abfuellen
        for index, text, user_data in self.globalOdsBfiStaging.getCbo_action_auswahl():
            self.comboBox_Execute.addItem(text, userData=[index, user_data])
        self.pushButton_Execute.setToolTip(self.globalOdsBfiStaging.getCbo_action_auswahl()[0][2])

        if self.globalOdsBfiStaging.getLogin_bfi().testConnection(printInfo=False):
            self.lineEdit_LoginBfi.setText(self.globalOdsBfiStaging.getLogin_bfi().getDisplayConnectionString())
        if self.globalOdsBfiStaging.getLogin_ods_bfi_staging().testConnection(printInfo=False):
            self.lineEdit_LoginOdsBfi.setText(
                self.globalOdsBfiStaging.getLogin_ods_bfi_staging().getDisplayConnectionString())

        self.lineEdit_OutputPath.setText(self.globalOdsBfiStaging.getOutput_path())
        self.lineEdit_SchemaChk.setText(self.globalOdsBfiStaging.getSchema_chk())
        self.lineEdit_Staging.setText(self.globalOdsBfiStaging.getSchema_staging())
        self.lineEdit_SchemaOds.setText(self.globalOdsBfiStaging.getSchema_ods())
        self.textEdit_Info.setText("")

    def write_debug_info(self, debug_info):
        self.textEdit_Info.append(debug_info)

    def __connectBfi(self):
        loginShow = True
        self.statusBar.showMessage("BFI Datenbank Verbindung setzen.", 10000)
        while loginShow:
            LoginDialog = QtWidgets.QDialog()
            LoginDialog.setWindowModality(QtCore.Qt.ApplicationModal)
            ui = Ui_LoginDialog()
            ui.setupUi(LoginDialog)
            result = LoginDialog.exec_()
            if result == QtWidgets.QDialog.Accepted:
                self.statusBar.showMessage("BFI Datenbank Verbindung testen...", 10000)
                self.globalOdsBfiStaging.getLogin_bfi().setUserName(userName=ui.lineEdit_Username.text())
                self.globalOdsBfiStaging.getLogin_bfi().setPassword(passWord=ui.lineEdit_Password.text())
                self.globalOdsBfiStaging.getLogin_bfi().setConnection(connection=ui.lineEdit_Connection.text())
                if self.globalOdsBfiStaging.getLogin_bfi().testConnection(printInfo=False):
                    self.lineEdit_LoginBfi.setText(self.globalOdsBfiStaging.getLogin_bfi().getDisplayConnectionString())
                    self.statusBar.showMessage("BFI Datenbank Verbindung OK.", 10000)
                    loginShow = False
                else:
                    self.statusBar.showMessage("BFI Datenbank Verbindung fehlgeschlagen, Dialog wird neu angezeigt.",
                                               10000)


            elif result == QtWidgets.QDialog.Rejected:
                loginShow = False

            LoginDialog.destroy()

    def __connectOdsBfi(self):
        loginShow = True
        self.statusBar.showMessage("ODS - BFI Datenbank Verbindung setzen.", 10000)
        while loginShow:
            LoginDialog = QtWidgets.QDialog()
            LoginDialog.setWindowModality(QtCore.Qt.ApplicationModal)
            ui = Ui_LoginDialog()
            ui.setupUi(LoginDialog)
            result = LoginDialog.exec_()
            if result == QtWidgets.QDialog.Accepted:
                self.statusBar.showMessage("ODS - BFI Datenbank Verbindung testen...", 10000)
                self.globalOdsBfiStaging.getLogin_ods_bfi_staging().setUserName(userName=ui.lineEdit_Username.text())
                self.globalOdsBfiStaging.getLogin_ods_bfi_staging().setPassword(passWord=ui.lineEdit_Password.text())
                self.globalOdsBfiStaging.getLogin_ods_bfi_staging().setConnection(
                    connection=ui.lineEdit_Connection.text())
                if self.globalOdsBfiStaging.getLogin_ods_bfi_staging().testConnection(printInfo=False):
                    self.lineEdit_LoginOdsBfi.setText(
                        self.globalOdsBfiStaging.getLogin_ods_bfi_staging().getDisplayConnectionString())
                    self.statusBar.showMessage("ODS - BFI Datenbank Verbindung OK.", 10000)
                    loginShow = False
                else:
                    self.statusBar.showMessage(
                        "ODS - BFI Datenbank Verbindung fehlgeschlagen, Dialog wird neu angezeigt.", 10000)


            elif result == QtWidgets.QDialog.Rejected:
                loginShow = False

            LoginDialog.destroy()

    def __browseScript(self):
        self.statusBar.showMessage("Script Output Pfad setzen.", 10000)
        initPath = os.getcwd()
        if len(self.globalOdsBfiStaging.getOutput_path()) > 0:
            initPath = self.globalOdsBfiStaging.getOutput_path()
        folder = QtWidgets.QFileDialog.getExistingDirectory(directory=initPath)
        if len(folder) > 0:
            self.lineEdit_OutputPath.setText(folder)
        else:
            self.lineEdit_OutputPath.setText("")
        self.globalOdsBfiStaging.setOutput_path(self.lineEdit_OutputPath.text())

    def __execute(self):
        print("__execute")
        self.textEdit_Info.clear()
        if self.comboBox_Execute.currentIndex() == 0:
            self.statusBar.showMessage("ODS Tabellen Initial ersetzen.")
            worker = OdsTableReplacer()
            worker.setup(bfi_login=self.globalOdsBfiStaging.getLogin_bfi(),
                         staging_login=self.globalOdsBfiStaging.getLogin_ods_bfi_staging(),
                         schema_ods=self.globalOdsBfiStaging.getSchema_ods(),
                         schema_bfi_stating=self.globalOdsBfiStaging.getLogin_ods_bfi_staging().getUserName(),
                         schema_bfi=self.globalOdsBfiStaging.getLogin_bfi().getUserName(),
                         schema_staging=self.globalOdsBfiStaging.getSchema_staging(),
                         template_kunde_subdirectory=self.globalOdsBfiStaging.getTemplate_kunde_subdirectory(),
                         output_path=self.globalOdsBfiStaging.getOutput_path(),
                         wirte2console=False,
                         do_initialize=True,
                         log_box=self.textEdit_Info
                         )
            worker.replace_tables()
            self.statusBar.showMessage("ODS Tabellen Initial ersetzen beendet.", 10000)
        elif self.comboBox_Execute.currentIndex() == 1:
            self.statusBar.showMessage("ODS Tabellen Incremental ersetzen.")
            worker = OdsTableReplacer()
            worker.setup(bfi_login=self.globalOdsBfiStaging.getLogin_bfi(),
                         staging_login=self.globalOdsBfiStaging.getLogin_ods_bfi_staging(),
                         schema_ods=self.globalOdsBfiStaging.getSchema_ods(),
                         schema_bfi_stating=self.globalOdsBfiStaging.getLogin_ods_bfi_staging().getUserName(),
                         schema_bfi=self.globalOdsBfiStaging.getLogin_bfi().getUserName(),
                         schema_staging=self.globalOdsBfiStaging.getSchema_staging(),
                         template_kunde_subdirectory=self.globalOdsBfiStaging.getTemplate_kunde_subdirectory(),
                         output_path=self.globalOdsBfiStaging.getOutput_path(),
                         wirte2console=False,
                         do_initialize=False,
                         log_box=self.textEdit_Info
                         )
            worker.replace_tables()
            self.statusBar.showMessage("ODS Tabellen Incremental ersetzen beendet.", 10000)
        elif self.comboBox_Execute.currentIndex() == 2:
            self.statusBar.showMessage("Load Package und Steuerung wird anhand der Definition erstellt.")
            creator = LoadCreator()
            creator.setup(loginOdsBfi=self.globalOdsBfiStaging.getLogin_ods_bfi_staging(),
                         template_kunde_subdirectory=self.globalOdsBfiStaging.getTemplate_kunde_subdirectory(),
                         output_base_pfad=self.globalOdsBfiStaging.getOutput_path(),
                         staging_name=self.globalOdsBfiStaging.getSchema_staging(),
                         chk_schema_name=self.globalOdsBfiStaging.getSchema_chk(),
                         bfi_schema_name=self.globalOdsBfiStaging.getLogin_bfi().getUserName(),
                         wirte2console=False,
                         log_box=self.textEdit_Info
                         )
            creator.create_load()
            self.globalOdsBfiStaging.export_ods_bfi_table_definition()
            self.statusBar.showMessage("Load Package und Steuerung wurde anhand der Definition erstellt.", 10000)
        elif self.comboBox_Execute.currentIndex() == 3:
            self.statusBar.showMessage("Bearbeiten der Korrektur Tabelle.")
            CorrectionDialog = QtWidgets.QDialog()
            CorrectionDialog.setWindowModality(QtCore.Qt.ApplicationModal)
            ui = Ui_CorrectionDialog()
            ui.setupUi(CorrectionDialog)
            ui.init_user_data(globalOdsBfiStaging=self.globalOdsBfiStaging)
            ui.connect_user_signals()
            result = CorrectionDialog.exec_()
            self.statusBar.showMessage("Bearbeiten der Korrektur Tabelle.", 10000)
        elif self.comboBox_Execute.currentIndex() == 4:
            self.statusBar.showMessage("Exportieren der ODS_BFI Tabelle als Script.")
            self.globalOdsBfiStaging.export_ods_bfi_table_definition()
            self.statusBar.showMessage("Exportieren der ODS_BFI Tabelle als Script beendet.", 10000)

    def __cbo_template_changed(self):
        for index, text, user_data in self.globalOdsBfiStaging.getCbo_kunde_subdirectory_auswahl():
            if index == self.comboBox_Template.currentIndex():
                self.globalOdsBfiStaging.setTemplate_kunde_subdirectory(user_data)

    def __cbo_action_changed(self):
        for index, text, user_data in self.globalOdsBfiStaging.getCbo_action_auswahl():
            if index == self.comboBox_Execute.currentIndex():
                self.pushButton_Execute.setToolTip(user_data)

    def __update_parameters(self):
        self.globalOdsBfiStaging.setSchema_ods(self.lineEdit_SchemaOds.text())
        self.globalOdsBfiStaging.setSchema_staging(self.lineEdit_Staging.text())
        self.globalOdsBfiStaging.setSchema_chk(self.lineEdit_SchemaChk.text())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
