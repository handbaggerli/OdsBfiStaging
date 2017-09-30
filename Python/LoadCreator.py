# -*- coding: utf-8 -*-

import codecs
import os
import cx_Oracle as ora
import Sqls
import shutil
from PyQt5 import QtCore


class LoadCreator():

    def __init__(self, parent=None):
        pass

    def setup(self, loginOdsBfi, template_kunde_subdirectory, output_base_pfad, staging_name, chk_schema_name,
              bfi_schema_name, wirte2console, log_box):
        self.loginOdsBfi = loginOdsBfi
        self.template_kunde_subdirectory = template_kunde_subdirectory
        self.output_base_pfad = output_base_pfad
        self.staging_name = staging_name.upper()
        self.chk_schema_name = chk_schema_name.upper()
        self.bfi_schema_name = bfi_schema_name.upper()
        self.special_table_list = []
        self.__load_special_list()
        self.basic_tables = ["t_verarbeitung.tab_save", "t_steuerung.tab_save", "t_korrektur.tab_save", "t_ods_generate_tables.tab_save", "t_exclude_list.tab", "t_exclude_list_tmp.tab"]
        self.basic_packages = ["pck_def_enviorement_variables.pks", "pck_init_verarbeitung.pks",
                               "pck_init_verarbeitung.pkb", "pck_load.pks", "pck_load.pkb"]
        self.wirte2console = wirte2console
        self.log_box = log_box

    def run(self):
        self.create_load()

    def create_load(self):
        self.__print_debug_info(debug_info="Erstelle Ladepackage und Steuerung...")
        self.__create_basic_tables()
        self.__create_basic_packges()
        tables_in_load = self.__get_tables_from_databas()
        self.__create_package_headers(tables_in_load=tables_in_load)
        self.__create_package_bodies(tables_in_load=tables_in_load)
        self.__create_steuerung(tables_in_load=tables_in_load)
        self.__create_enviorement_variables(tables_in_load=tables_in_load)
        self.__create_load_module_aufruf(tables_in_load=tables_in_load)
        self.__print_debug_info(debug_info="Erstellung Ladepackage und Steuerung beendet.")

    def __load_special_list(self):
        list_base = os.path.join(os.getcwd(), 'database', 'config', 'table_list_special.txt')
        list_knd = os.path.join(os.getcwd(), 'database', 'config', self.template_kunde_subdirectory,
                                'table_list_special.txt')
        self.__read_table_list_special(filename=list_base)
        self.__read_table_list_special(filename=list_knd)

    def __read_table_list_special(self, filename):
        if not os.path.exists(filename):
            return
        with codecs.open(filename=filename, mode="r", encoding="utf-8") as f:
            for line in f:
                row_obj = line.split(",")
                if len(row_obj) > 1:
                    row_dic = {}
                    self.__remove_special_list(row_obj[0].strip())
                    row_dic['table_name'] = row_obj[0].strip()
                    row_dic['table_ladetyp'] = row_obj[1].strip()
                    row_dic['table_pruefen'] = row_obj[2].strip()
                    self.special_table_list.append(row_dic)

    def __remove_special_list(self, table_name):
        for element in self.special_table_list:
            if element['table_name'] == table_name:
                self.special_table_list.remove(element)

    def __get_tables_from_databas(self):
        table_list = []
        with ora.connect(self.loginOdsBfi.getUserName(), self.loginOdsBfi.getPassword(),
                           self.loginOdsBfi.getConnection()) as conn:
            cur = conn.cursor()
            cur.execute(Sqls.SELECT_ODS_BFI_TABLE_LIST4LOAD)
            for row in cur:
                table_list.append(row[0])

        return table_list

    def __create_steuerung(self, tables_in_load):
        self.__print_debug_info(debug_info="Erstelle Steuerung Datei.")

        filename = os.path.join(self.output_base_pfad, 'config', 'insert_ods_bfi_steuerung.sql')
        schritt_nr = 0
        os.makedirs(os.path.join(self.output_base_pfad, 'config'), exist_ok=True)
        base_command = "insert into t_steuerung (steuerung_id, table_name, schritt_nr, table_ladetyp, table_ladetyp_next, pruefen, kommand) values (sys_guid (), '{table_name}', {schritt_nr}, '{table_ladetyp}', '{table_ladetyp}', '{pruefen}', '{kommand}');\n"
        with codecs.open(filename=filename, mode="w", encoding="utf-8") as f:
            f.write("begin\n")
            f.write("delete t_steuerung;\n")
            f.write("commit;\n")
            f.write("----\n")

            for table in tables_in_load:
                schritt_nr += 1
                row_dic = {}
                row_dic['table_name'] = table
                row_dic['schritt_nr'] = schritt_nr
                row_dic['table_ladetyp'] = "INCR"
                row_dic['pruefen'] = "Y"
                row_dic['kommand'] = 'pck_tab_{0}.fun_run'.format(table.lower())
                self.__overwrite_steuerung_row(row_dic=row_dic)
                cmd = base_command.format(**row_dic)
                f.write(cmd)
            f.write("commit;\n")
            f.write("end;\n")
            f.write("/\n")

    def __overwrite_steuerung_row(self, row_dic):
        for element in self.special_table_list:
            if row_dic['table_name'] == element['table_name']:
                row_dic['table_ladetyp'] = element['table_ladetyp']
                row_dic['pruefen'] = element['table_pruefen']

    def __create_enviorement_variables(self, tables_in_load):
        self.__print_debug_info(debug_info="Erstelle Replacement fuer Enviorement Variables.")
        os.makedirs(os.path.join(self.output_base_pfad, 'source', 'replacements'), exist_ok=True)
        filename = os.path.join(self.output_base_pfad, 'source', 'replacements',
                                'pck_def_enviorement_variables__table_package_list.sql_replace')
        base_command = "c_{table}                  constant t_steuerung.kommand%type := 'pck_tab_{table}.fun_run';\n"
        with codecs.open(filename=filename, mode="w", encoding="utf-8") as f:
            for table in tables_in_load:
                f.write(base_command.format(table=table.lower()))

    def __create_load_module_aufruf(self, tables_in_load):
        self.__print_debug_info(debug_info="Erstelle Replacement fuer Load Modul Aufruf.")
        os.makedirs(os.path.join(self.output_base_pfad, 'source', 'replacements'), exist_ok=True)
        filename = os.path.join(self.output_base_pfad, 'source', 'replacements',
                                'pck_load__fun_modul_aufruf.sql_replace')
        base_command = "\t\twhen lower (pck_def_enviorement_variables.c_{table}) then\n\t\t\tl_return := pck_tab_{table}.fun_run (p_verarbeitung => p_verarbeitung, p_steuerung => p_steuerung);\n"

        with codecs.open(filename=filename, mode="w", encoding="utf-8") as f:
            for table in tables_in_load:
                f.write(base_command.format(table=table.lower()))

    def __create_basic_packges(self):
        self.__print_debug_info(debug_info="Erstelle Basis Packages fuer Verabeitungssteuerung.")
        base_path_source = os.path.join(os.getcwd(), 'database', 'packages')
        base_path_target = os.path.join(self.output_base_pfad, 'source', 'packages')
        os.makedirs(base_path_target, exist_ok=True)
        for package in self.basic_packages:
            shutil.copy(os.path.join(base_path_source, package), os.path.join(base_path_target, package))

    def __create_basic_tables(self):
        self.__print_debug_info(debug_info="Erstelle Basis Tabellen fuer Verabeitungssteuerung.")
        base_path_source = os.path.join(os.getcwd(), 'database', 'tables')
        base_path_target = os.path.join(self.output_base_pfad, 'source', 'tables')
        os.makedirs(base_path_target, exist_ok=True)
        for table in self.basic_tables:
            shutil.copy(os.path.join(base_path_source, table), os.path.join(base_path_target, table))

    def __create_package_headers(self, tables_in_load):
        self.__print_debug_info(debug_info="Erstelle Package Headers fuer alle  Tabellen.")
        base_path_source = os.path.join(os.getcwd(), 'database', 'packages', 'pck_tab_template.pks')
        base_path_target = os.path.join(self.output_base_pfad, 'source', 'packages')
        os.makedirs(base_path_target, exist_ok=True)
        package_base_text = ""

        with codecs.open(filename=base_path_source, mode="r", encoding="utf-8") as f_in:
            package_base_text = f_in.read()

        for table in tables_in_load:
            package_header_name = "pck_tab_{table_name}.pks".format(table_name=table.lower())
            with codecs.open(filename=os.path.join(base_path_target, package_header_name), mode="w",
                             encoding="utf-8") as f_out:
                package_text = package_base_text.format(table_name=table.lower())
                f_out.write(package_text)

    def __create_package_bodies(self, tables_in_load):
        self.__print_debug_info(debug_info="Erstelle Package Body fuer alle  Tabellen.")
        base_path_target = os.path.join(self.output_base_pfad, 'source', 'packages')
        os.makedirs(base_path_target, exist_ok=True)

        for table in tables_in_load:
            package_body_name = "pck_tab_{table_name}.pkb".format(table_name=table.lower())
            source_template = self.__get_packge_body_template(table=table.lower())
            with codecs.open(filename=source_template, mode="r", encoding="utf-8") as f_in:
                package_base_text = f_in.read()

            dic_replacement = {}
            dic_replacement['table_name'] = table.lower()
            dic_replacement['staging_schema'] = self.staging_name.lower()
            dic_replacement['bfi_schema'] = self.bfi_schema_name.lower()
            dic_replacement['select_column_list'] = self.__build_select_column_list(table_name=table.upper())
            dic_replacement['check_schema'] = self.chk_schema_name.lower()
            with codecs.open(filename=os.path.join(base_path_target, package_body_name), mode="w",
                             encoding="utf-8") as f_out:
                package_text = package_base_text.format(**dic_replacement)
                f_out.write(package_text)

    def __get_packge_body_template(self, table):
        package_name = "pck_tab_{table_name}.pkb".format(table_name=table)
        ## Kundenspezifisches Package
        package_path = os.path.join(os.getcwd(), 'database', 'packages', self.template_kunde_subdirectory, package_name)
        if os.path.exists(package_path):
            return package_path

        ## Generelles Spezifisches Package
        package_path = os.path.join(os.getcwd(), 'database', 'packages', package_name)
        if os.path.exists(package_path):
            return package_path

        ## Basis Template
        package_path = os.path.join(os.getcwd(), 'database', 'packages', 'pck_tab_template.pkb')
        return package_path

    def __build_select_column_list(self, table_name):
        select_column_list = ""
        offset = "  "

        with ora.connect(self.loginOdsBfi.getUserName(), self.loginOdsBfi.getPassword(),
                           self.loginOdsBfi.getConnection()) as conn:
            cur = conn.cursor()
            cur.execute(Sqls.SELECT_ODS_TABLE_COLUMNS, ODS_SCHEMA=self.loginOdsBfi.getUserName().upper(),
                        TABLE_NAME=table_name)
            for row in cur:
                select_column_list += "{offset} {column}\n".format(offset=offset, column=row[2].lower())
                offset = ", "

        return select_column_list

    def __print_debug_info(self, debug_info):
        if self.wirte2console:
            print(debug_info)
        else:
            self.log_box.append(debug_info)
            QtCore.QCoreApplication.processEvents()
