# -*- coding: utf-8 -*-

import sys
from argparse import ArgumentParser

from PyQt5 import QtWidgets

from Ui_MainWindow import Ui_MainWindow
from DatabaseLogin import DatabaseLogin
from GlobalOdsBfiStaging import GlobalOdsBfiStaging
from OdsTableReplacer import OdsTableReplacer
from LoadCreator import LoadCreator
from time import sleep

# import damit Installer funktioniert. auch wenn diese hier nicht benoetigt werden.

from PyQt5 import QtCore, QtGui
import cx_Oracle
from subprocess import Popen, PIPE
import json
import os
from operator import itemgetter

import Sqls
from Ui_CorrectionDialog import Ui_CorrectionDialog
from Ui_LoginDialog import Ui_LoginDialog
from CorrectionTableModel import CorrectionTableModel


def get_parser():
    parser = ArgumentParser()
    parser.add_argument('--bfi_username', default=r"", help=r"Benutzername der BFI Datenbank Verbindung.")
    parser.add_argument('--bfi_password', default=r"", help=r"Passwort der BFI Datenbank Verbindung.")
    parser.add_argument('--bfi_connection', default=r"",
                        help=r"Connection der BFI Datenbank Verbindung.")

    parser.add_argument('--ods_bfi_username', default=r"",
                        help=r"Benutzername der ODS - BFI Datenbank Verbindung.")
    parser.add_argument('--ods_bfi_password', default=r"",
                        help=r"Passwort der ODS - BFI Datenbank Verbindung.")
    parser.add_argument('--ods_bfi_connection', default=r"",
                        help=r"Connection der ODS - BFI Datenbank Verbindung.")

    parser.add_argument('--script_output', default=r"",
                        help=r"Output Pfad wo die Scripte gespeichert werden.")
    parser.add_argument('--schema_ods', default=r"", help=r"Schemaname ODS.")
    parser.add_argument('--schema_chk', default=r"", help=r"Schemaname CHK.")
    parser.add_argument('--schema_staging', default=r"", help=r"Schemaname Staging.")
    parser.add_argument('--knd_template', default=r"", help=r"Name des Kunden Template Verzeichnis.")
    parser.add_argument('--hideGui', action='store_true', default=False,
                        help=r"Startet ODS Bfi Staging Builder ohne GUI.")
    parser.add_argument('--build_ods_bfi_tables_init', action='store_true', default=False,
                        help=r"Started den Task ODS BFI Staging Tabellen Initial erstellen.")
    parser.add_argument('--build_ods_bfi_tables_incr', action='store_true', default=False,
                        help=r"Started den Task ODS BFI Staging Tabellen Inkremental erstellen.")
    parser.add_argument('--build_load_packages', action='store_true', default=False,
                        help=r"Started den Task Ladepackages anhand der Tabellen erstellen.")
    return parser


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    login_bfi = DatabaseLogin(userName=args.bfi_username,
                              passWord=args.bfi_password,
                              connection=args.bfi_connection)

    login_ods_bfi_staging = DatabaseLogin(userName=args.ods_bfi_username,
                                          passWord=args.ods_bfi_password,
                                          connection=args.ods_bfi_connection)

    globalOdsBfiStaging = GlobalOdsBfiStaging(login_bfi=login_bfi,
                                              login_ods_bfi_staging=login_ods_bfi_staging,
                                              schema_ods=args.schema_ods,
                                              schema_staging=args.schema_staging,
                                              schema_chk=args.schema_chk,
                                              template_kunde_subdirectory=args.knd_template,
                                              output_path=args.script_output)

    if args.hideGui:
        if args.build_ods_bfi_tables_init:
            worker = OdsTableReplacer()
            worker.setup(bfi_login=globalOdsBfiStaging.getLogin_bfi(),
                         staging_login=globalOdsBfiStaging.getLogin_ods_bfi_staging(),
                         schema_ods=globalOdsBfiStaging.getSchema_ods(),
                         schema_bfi_stating=globalOdsBfiStaging.getLogin_ods_bfi_staging().getUserName(),
                         schema_bfi=globalOdsBfiStaging.getLogin_bfi().getUserName(),
                         schema_staging=globalOdsBfiStaging.getSchema_staging(),
                         template_kunde_subdirectory=globalOdsBfiStaging.getTemplate_kunde_subdirectory(),
                         output_path=globalOdsBfiStaging.getOutput_path(),
                         wirte2console=True,
                         do_initialize=True,
                         log_box=None
                         )
            worker.replace_tables()
        elif args.build_ods_bfi_tables_incr:
            worker = OdsTableReplacer()
            worker.setup(bfi_login=globalOdsBfiStaging.getLogin_bfi(),
                         staging_login=globalOdsBfiStaging.getLogin_ods_bfi_staging(),
                         schema_ods=globalOdsBfiStaging.getSchema_ods(),
                         schema_bfi_stating=globalOdsBfiStaging.getLogin_ods_bfi_staging().getUserName(),
                         schema_bfi=globalOdsBfiStaging.getLogin_bfi().getUserName(),
                         schema_staging=globalOdsBfiStaging.getSchema_staging(),
                         template_kunde_subdirectory=globalOdsBfiStaging.getTemplate_kunde_subdirectory(),
                         output_path=globalOdsBfiStaging.getOutput_path(),
                         wirte2console=True,
                         do_initialize=False,
                         log_box=None
                         )
            worker.replace_tables()

        if args.build_load_packages:
            creator = LoadCreator()
            creator.setup(loginOdsBfi=globalOdsBfiStaging.getLogin_ods_bfi_staging(),
                         template_kunde_subdirectory=globalOdsBfiStaging.getTemplate_kunde_subdirectory(),
                         output_base_pfad=globalOdsBfiStaging.getOutput_path(),
                         staging_name=globalOdsBfiStaging.getSchema_staging(),
                         chk_schema_name=globalOdsBfiStaging.getSchema_chk(),
                         bfi_schema_name=globalOdsBfiStaging.getLogin_bfi().getUserName(),
                         wirte2console=True,
                         log_box=None
                         )
            creator.create_load()

    else:
        # Default Option starts GUI
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        ui.init_user_data(globalOdsBfiStaging=globalOdsBfiStaging)
        ui.connect_user_signals()
        MainWindow.show()
        sys.exit(app.exec_())
