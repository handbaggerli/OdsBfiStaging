# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\GitRepos\OdsBfiStaging\GuiBuilder\OdsBfiStaging\correctiondialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from GlobalOdsBfiStaging import GlobalOdsBfiStaging
from DatabaseLogin import DatabaseLogin
from CorrectionTableModel import CorrectionTableModel


class Ui_CorrectionDialog(object):
    def setupUi(self, CorrectionDialog):
        CorrectionDialog.setObjectName("CorrectionDialog")
        CorrectionDialog.resize(693, 592)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("database-refresh.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        CorrectionDialog.setWindowIcon(icon)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(CorrectionDialog)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(CorrectionDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(CorrectionDialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(CorrectionDialog)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(CorrectionDialog)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(CorrectionDialog)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.label_6 = QtWidgets.QLabel(CorrectionDialog)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.label_7 = QtWidgets.QLabel(CorrectionDialog)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.comboBox_Table = QtWidgets.QComboBox(CorrectionDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_Table.sizePolicy().hasHeightForWidth())
        self.comboBox_Table.setSizePolicy(sizePolicy)
        self.comboBox_Table.setObjectName("comboBox_Table")
        self.verticalLayout_3.addWidget(self.comboBox_Table)
        self.comboBox_Action = QtWidgets.QComboBox(CorrectionDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_Action.sizePolicy().hasHeightForWidth())
        self.comboBox_Action.setSizePolicy(sizePolicy)
        self.comboBox_Action.setObjectName("comboBox_Action")
        self.verticalLayout_3.addWidget(self.comboBox_Action)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.checkBox_FilterTable = QtWidgets.QCheckBox(CorrectionDialog)
        self.checkBox_FilterTable.setObjectName("checkBox_FilterTable")
        self.verticalLayout_2.addWidget(self.checkBox_FilterTable)
        self.pushButton_Execute = QtWidgets.QPushButton(CorrectionDialog)
        self.pushButton_Execute.setObjectName("pushButton_Execute")
        self.verticalLayout_2.addWidget(self.pushButton_Execute)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.comboBox_CorrectionType = QtWidgets.QComboBox(CorrectionDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_CorrectionType.sizePolicy().hasHeightForWidth())
        self.comboBox_CorrectionType.setSizePolicy(sizePolicy)
        self.comboBox_CorrectionType.setObjectName("comboBox_CorrectionType")
        self.verticalLayout_4.addWidget(self.comboBox_CorrectionType)
        self.spinBox_Sequenz = QtWidgets.QSpinBox(CorrectionDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_Sequenz.sizePolicy().hasHeightForWidth())
        self.spinBox_Sequenz.setSizePolicy(sizePolicy)
        self.spinBox_Sequenz.setObjectName("spinBox_Sequenz")
        self.verticalLayout_4.addWidget(self.spinBox_Sequenz)
        self.lineEdit_Script = QtWidgets.QLineEdit(CorrectionDialog)
        self.lineEdit_Script.setObjectName("lineEdit_Script")
        self.verticalLayout_4.addWidget(self.lineEdit_Script)
        self.lineEdit_PkeysExclude = QtWidgets.QLineEdit(CorrectionDialog)
        self.lineEdit_PkeysExclude.setObjectName("lineEdit_PkeysExclude")
        self.verticalLayout_4.addWidget(self.lineEdit_PkeysExclude)
        self.lineEdit_ScriptExclude = QtWidgets.QLineEdit(CorrectionDialog)
        self.lineEdit_ScriptExclude.setObjectName("lineEdit_ScriptExclude")
        self.verticalLayout_4.addWidget(self.lineEdit_ScriptExclude)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.tableView_Korrektur = QtWidgets.QTableView(CorrectionDialog)
        self.tableView_Korrektur.setObjectName("tableView_Korrektur")
        self.verticalLayout_5.addWidget(self.tableView_Korrektur)
        self.buttonBox = QtWidgets.QDialogButtonBox(CorrectionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_5.addWidget(self.buttonBox)

        self.retranslateUi(CorrectionDialog)
        self.buttonBox.accepted.connect(CorrectionDialog.accept)
        self.buttonBox.rejected.connect(CorrectionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CorrectionDialog)

    def retranslateUi(self, CorrectionDialog):
        _translate = QtCore.QCoreApplication.translate
        CorrectionDialog.setWindowTitle(_translate("CorrectionDialog", "Korrektur Tabelle Bearbeiten"))
        self.label.setText(_translate("CorrectionDialog", "Tabelle:"))
        self.label_2.setText(_translate("CorrectionDialog", "Aktion:"))
        self.label_3.setText(_translate("CorrectionDialog", "Korrektur Ladetyp:"))
        self.label_4.setText(_translate("CorrectionDialog", "Korrektur Sequenz:"))
        self.label_5.setText(_translate("CorrectionDialog", "Script:"))
        self.label_6.setText(_translate("CorrectionDialog", "Pkeys Exclude:"))
        self.label_7.setText(_translate("CorrectionDialog", "Script Exclude:"))
        self.checkBox_FilterTable.setText(_translate("CorrectionDialog", "Nur Tabellen mit Korrektur"))
        self.pushButton_Execute.setText(_translate("CorrectionDialog", "Execute"))

    ########################################################################################################

    def init_user_data(self, globalOdsBfiStaging):
        self.globalOdsBfiStaging = globalOdsBfiStaging
        for index, data in self.globalOdsBfiStaging.getCbo_corr_load_type():
            self.comboBox_CorrectionType.addItem(data, userData=index)
        for index, data, toolTip in self.globalOdsBfiStaging.getCbo_corr_action():
            self.comboBox_Action.addItem(data, userData=[index, toolTip])
            if index == 0:
                self.pushButton_Execute.setToolTip(toolTip)
        self.checkBox_FilterTable.setChecked(False)
        self.comboBox_Table.clear()
        for ods_table in self.globalOdsBfiStaging.getAllUsedOdsTables():
            self.comboBox_Table.addItem(ods_table)

        self.__refresh_correction_table()

    def connect_user_signals(self):
        self.comboBox_Action.currentIndexChanged.connect(self.__cbo_action_changed)
        self.checkBox_FilterTable.clicked.connect(self.__checkBox_FilterTable_changed)
        self.tableView_Korrektur.clicked.connect(self.__tableView_Korrektur_clicked)
        self.comboBox_Table.currentIndexChanged.connect(self.__clear_selection)
        self.pushButton_Execute.clicked.connect(self.__pushButton_Execute_clicked)

    def __cbo_action_changed(self):
        self.__clear_selection()
        for index, data, toolTip in self.globalOdsBfiStaging.getCbo_corr_action():
            if self.comboBox_Action.currentIndex() == index:
                self.pushButton_Execute.setToolTip(toolTip)

    def __checkBox_FilterTable_changed(self):
        self.__clear_selection()
        self.comboBox_Table.clear()
        if self.checkBox_FilterTable.isChecked():
            for ods_table in self.globalOdsBfiStaging.getAllUsedOdsTablesWithScript():
                self.comboBox_Table.addItem(ods_table)
        else:
            for ods_table in self.globalOdsBfiStaging.getAllUsedOdsTables():
                self.comboBox_Table.addItem(ods_table)

    def __tableView_Korrektur_clicked(self):
        model = self.tableView_Korrektur.model()
        row = self.tableView_Korrektur.currentIndex().row()
        self.curr_korrektur_id = model.arraydata[row][0]
        for korrektur_id, table_name, sequenz, ladetyp, script, pkeys_exclude, script_exclude in self.globalOdsBfiStaging.getCorrectTableData():
            if self.curr_korrektur_id == korrektur_id:
                self.comboBox_Table.setCurrentText(table_name)
                self.spinBox_Sequenz.setValue(sequenz)
                self.comboBox_CorrectionType.setCurrentText(ladetyp)
                self.lineEdit_Script.setText(script)
                self.lineEdit_PkeysExclude.setText(pkeys_exclude)
                self.lineEdit_ScriptExclude.setText(script_exclude)

    def __clear_selection(self):
        self.curr_korrektur_id = ""
        self.lineEdit_Script.setText("")
        self.spinBox_Sequenz.setValue(1)
        self.comboBox_CorrectionType.setCurrentIndex(0)
        self.lineEdit_ScriptExclude.setText("")
        self.lineEdit_PkeysExclude.setText("")

    def __pushButton_Execute_clicked(self):
        if self.comboBox_Action.currentIndex() == 0:
            self.__insert_new_element()
        elif self.comboBox_Action.currentIndex() == 1:
            self.__update_element()
        elif self.comboBox_Action.currentIndex() == 2:
            self.__delete_element()
        elif self.comboBox_Action.currentIndex() == 3:
            self.__export_to_file()
        elif self.comboBox_Action.currentIndex() == 4:
            self.__load_from_file()

    def __insert_new_element(self):
        self.globalOdsBfiStaging.insertCorrectTableRow(
            table_name=self.comboBox_Table.currentText(),
            sequenz=self.spinBox_Sequenz.value(),
            load_type=self.comboBox_CorrectionType.currentText(),
            script=self.lineEdit_Script.text(),
            pkey_exclude=self.lineEdit_PkeysExclude.text(),
            script_exclude=self.lineEdit_ScriptExclude.text()
        )
        self.__refresh_correction_table()
        self.__clear_selection()

    def __update_element(self):
        if len(self.curr_korrektur_id) == 0:
            self.__insert_new_element()
        else:
            self.globalOdsBfiStaging.updateCorrectTableRow(korrektur_id=self.curr_korrektur_id,
                                                           table_name=self.comboBox_Table.currentText(),
                                                           sequenz=self.spinBox_Sequenz.value(),
                                                           load_type=self.comboBox_CorrectionType.currentText(),
                                                           script=self.lineEdit_Script.text(),
                                                           pkey_exclude=self.lineEdit_PkeysExclude.text(),
                                                           script_exclude=self.lineEdit_ScriptExclude.text()
                                                           )
        self.__refresh_correction_table()
        self.__clear_selection()

    def __delete_element(self):
        if len(self.curr_korrektur_id) > 0:
            self.globalOdsBfiStaging.deleteCorrectTableRow(korrektur_id=self.curr_korrektur_id)
        self.__refresh_correction_table()
        self.__clear_selection()

    def __refresh_correction_table(self):
        model = CorrectionTableModel(header=self.globalOdsBfiStaging.getCorrect_table_header(),
                                     data=self.globalOdsBfiStaging.getCorrectTableData())
        self.tableView_Korrektur.setModel(model)
        self.tableView_Korrektur.resizeColumnsToContents()
        self.curr_korrektur_id = ""

    def __export_to_file(self):
        fileName = QtWidgets.QFileDialog.getSaveFileName()
        if len(fileName[0]) > 0:
            self.globalOdsBfiStaging.export_to_file(filename=fileName[0])
        self.__refresh_correction_table()
        self.__clear_selection()

    def __load_from_file(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName()
        if len(fileName[0]) > 0:
            self.globalOdsBfiStaging.import_from_file(filename=fileName[0])
        self.__refresh_correction_table()
        self.__clear_selection()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    login_bfi = DatabaseLogin(userName="BFI200",
                              passWord="BFI200_INTE",
                              connection="shp_dwh_inte200r3")

    login_ods_bfi_staging = DatabaseLogin(userName="ods_bfi200",
                                          passWord="$INTEOB200$",
                                          connection="shp_dwh_inte200r3")

    globalOdsBfiStaging = GlobalOdsBfiStaging(login_bfi=login_bfi,
                                              login_ods_bfi_staging=login_ods_bfi_staging,
                                              schema_ods="ODS200",
                                              schema_staging="ase20001_staging",
                                              schema_chk="CHK200",
                                              template_kunde_subdirectory="KND200",
                                              output_path=r"d:/install/ods_bfi200")

    CorrectionDialog = QtWidgets.QDialog()
    ui = Ui_CorrectionDialog()
    ui.setupUi(CorrectionDialog)
    ui.init_user_data(globalOdsBfiStaging=globalOdsBfiStaging)
    ui.connect_user_signals()
    CorrectionDialog.show()
    sys.exit(app.exec_())
