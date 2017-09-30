# -*- coding: utf-8 -*-
import Sqls
import cx_Oracle as ora
import os
from enum import Enum, unique
import codecs

from PyQt5 import QtCore

from DatabaseLogin import DatabaseLogin


@unique
class EColumnUsed(Enum):
    yes = "Y"
    no = "N"


@unique
class EDataType(Enum):
    varchar2 = "VARCHAR2"
    char = "CHAR"
    number = "NUMBER"
    date = "DATE"
    timestamp9 = "TIMESTAMP(9)"
    timestamp6 = "TIMESTAMP(6)"
    clob = "CLOB"
    blob = "BLOB"


class OdsTableReplacer():
    def __init__(self, parent=None):
        pass

    def setup(self, bfi_login, staging_login, schema_ods, schema_bfi_stating, schema_bfi, schema_staging,
              template_kunde_subdirectory, output_path, wirte2console, do_initialize, log_box):
        self.bfi_login = DatabaseLogin(userName=bfi_login.getUserName(), passWord=bfi_login.getPassword(),
                                       connection=bfi_login.getConnection())
        self.staging_login = DatabaseLogin(userName=staging_login.getUserName(), passWord=staging_login.getPassword(),
                                           connection=staging_login.getConnection())
        self.schema_ods = schema_ods.upper()
        self.schema_bfi_stating = schema_bfi_stating.upper()
        self.schema_bfi = schema_bfi.upper()
        self.schema_staging = schema_staging.upper()
        self.template_kunde_subdirectory = template_kunde_subdirectory
        self.output_path = output_path
        self.wirte2console = wirte2console
        self.do_initialize = do_initialize
        self.log_box = log_box

    def run(self):
        self.replace_tables()

    def replace_tables(self):
        if self.do_initialize:
            self.__recreate_generate_table()
        synonym_list = []
        with ora.connect(self.bfi_login.getUserName(), self.bfi_login.getPassword(),
                         self.bfi_login.getConnection()) as conn:
            cur = conn.cursor()
            cur.execute(Sqls.SELECT_ODS_SYNONYMS, ODS_SCHEMA=self.schema_ods)
            self.__print_debug_info(debug_info="Starte Synonyme mit Tabellen zu ersetzten.")
            for row in cur:
                synonym_list.append(row[0])
            conn.commit()

        for element in synonym_list:
            self.__print_debug_info(debug_info="Starte Replacement fuer Element {0}:".format(element))
            self.bfi_login.runSqlPlus(sql_command=Sqls.DROP_SYNONYM.format(element))
            if not self.__compile_valide():
                self.__create_ods_table(synonym=element)
                if self.__compile_valide():
                    self.__reduce_columns(table_name=element)
                    if not self.__compile_valide():
                        self.__print_debug_info(debug_info="Fehler bei der Synonym Erstellung. Programm wird beendet!")
                        return
                else:
                    self.__print_debug_info(debug_info="Fehler bei der Synonym Erstellung. Programm wird beendet!")
                    return
        self.__print_debug_info(debug_info="Synonyme mit Tabellen zu ersetzten beendet.")

    def __recreate_generate_table(self):
        self.staging_login.runSqlPlus(sql_command=Sqls.DROP_T_ODS_GENERATE_TABLES)
        self.staging_login.runSqlPlus(sql_command=Sqls.CREATE_T_ODS_GENERATE_TABLES)

    def __compile_valide(self):
        has_compiled = True
        sql_compile_all = Sqls.CMD_COMPILE_ALL.format(self.schema_bfi)
        self.bfi_login.runSqlPlus(sql_command=sql_compile_all)

        with ora.connect(self.bfi_login.getUserName(), self.bfi_login.getPassword(),
                         self.bfi_login.getConnection()) as conn:
            cur = conn.cursor()
            cur.execute(Sqls.SELECT_INVALIDE_PACKAGES)
            for row in cur:
                has_compiled = False
        return has_compiled

    def __create_ods_table(self, synonym):
        with ora.connect(self.bfi_login.getUserName(), self.bfi_login.getPassword(),
                         self.bfi_login.getConnection()) as conn_select:
            cur_select = conn_select.cursor()

            with ora.connect(self.staging_login.getUserName(), self.staging_login.getPassword(),
                             self.staging_login.getConnection()) as conn_delete:
                cur_delete = conn_delete.cursor()
                cur_delete.execute(Sqls.DELETE_T_ODS_GENERATE_TABLE, TABLE_NAME=synonym)
                conn_delete.commit()

            with ora.connect(self.staging_login.getUserName(), self.staging_login.getPassword(),
                             self.staging_login.getConnection()) as conn_insert:
                cur_insert = conn_insert.cursor()
                cur_select.execute(Sqls.SELECT_ODS_TABLE_COLUMNS, ODS_SCHEMA=self.schema_ods, TABLE_NAME=synonym)
                for row in cur_select:
                    data_type, column_used = self.__parse_data_type(data_type=row[3], data_length=row[4],
                                                                    data_precision=row[5],
                                                                    data_scale=row[6], nullable=row[7])
                    cur_insert.execute(Sqls.INSERT_T_ODS_GENERATE_TABLES, TABLE_NAME=row[0], COLUMN_ID=int(row[1]),
                                       COLUMN_NAME=row[2],
                                       DATA_TYPE=data_type, COLUMN_USED=column_used)
                    conn_insert.commit()
        pseudo_sql = "drop table {0} purge;".format(synonym)
        self.staging_login.runSqlPlus(sql_command=pseudo_sql)
        pseudo_sql = "create table {0} as select * from {1}.{0} where 1 = 2;".format(synonym, self.schema_staging)
        self.staging_login.runSqlPlus(sql_command=pseudo_sql)
        self.__create_synonym_grant(synonym=synonym)

    def __create_synonym_grant(self, synonym):
        pseudo_sql = "grant select on {0} to {1} with grant option;".format(synonym, self.schema_bfi)
        self.staging_login.runSqlPlus(sql_command=pseudo_sql)
        pseudo_sql = "create or replace synonym {0} for {1}.{0};".format(synonym, self.schema_bfi_stating)
        self.bfi_login.runSqlPlus(sql_command=pseudo_sql)

    def __parse_data_type(self, data_type, data_length, data_precision, data_scale, nullable):
        parsed_data_type = ""
        column_used = EColumnUsed.yes.value

        if data_type == EDataType.number.value:
            parsed_data_type = EDataType.number.value + "({0}, {1})".format(int(data_precision), int(data_scale))
        elif data_type == EDataType.varchar2.value or data_type == EDataType.char.value:
            parsed_data_type = EDataType.varchar2.value + "({0})".format(int(data_length))
        elif data_type == EDataType.date.value or data_type == EDataType.timestamp6.value or data_type == EDataType.timestamp9.value:
            parsed_data_type = data_type
        elif data_type == EDataType.clob.value or data_type == EDataType.blob.value:
            parsed_data_type = data_type
            column_used = EColumnUsed.no.value

        if nullable == "N":
            parsed_data_type += " NOT NULL"

        return parsed_data_type, column_used

    def __reduce_columns(self, table_name):
        with ora.connect(self.staging_login.getUserName(), self.staging_login.getPassword(),
                         self.staging_login.getConnection()) as conn:
            cur = conn.cursor()
            cur.execute(Sqls.SELECT_ODS_GENERAED_COLUMNS, TABLE_NAME=table_name)
            for row in cur:
                if not row[3] == "PKEY":
                    reduce_ok = self.__reduce_column(table_name=table_name, column_name=row[3])
                    if reduce_ok:
                        self.__update_reduce(table_name=table_name, column_id=row[2])

            # Aufruf fuer Pseudocolumn, wenn letzte Column noch benoetigt wird.
            self.__reduce_column(table_name=table_name, column_name="PSEUDO_COLUMN_4_CHECK")

    def __reduce_column(self, table_name, column_name):
        self.__print_debug_info(debug_info=" - Reduziere Column {0}.{1}".format(table_name, column_name))
        offset = ""
        has_pkey = False
        has_boid = False
        l_col_count = 0
        output_path = os.path.join(self.output_path, "source", "tables")
        os.makedirs(output_path, exist_ok=True)
        file_name = os.path.join(output_path, table_name.lower() + ".tab_save")
        sql_commands = "drop table {0} cascade constraint purge;\n\n".format(table_name.lower())
        sql_commands += "create table {0}\n(\n".format(table_name.lower())

        with ora.connect(self.staging_login.getUserName(), self.staging_login.getPassword(),
                         self.staging_login.getConnection()) as conn:
            cur = conn.cursor()
            cur.execute(Sqls.SELECT_ODS_GENERAED_COLUMNS, TABLE_NAME=table_name)
            for row in cur:
                l_col_count += 1
                if row[3] == "PKEY":
                    has_pkey = True
                if row[3] == "BOID":
                    has_boid = True
                if row[3] == column_name:
                    pass
                else:
                    sql_commands += "{0} {1}\t{2}\n".format(offset, str(row[3]).lower(), str(row[4]).lower())
                    offset = ","

        sql_commands += ")\n  compress\n nologging\n parallel;\n\n"

        sql_commands += "\nbegin\n  pck_warte_constraint_info.prc_define_delete(p_table => '{0}');\nend;\n/\n".format(
            table_name.lower())

        if has_pkey:
            sql_commands += "\nbegin\n"
            sql_commands += " pck_warte_constraint_info.prc_define_primary_key(p_table => '{0}', p_column => 'pkey');\n".format(
                table_name.lower())
            sql_commands += "end;\n/\n\n"
        if has_boid and l_col_count > 9:
            sql_commands += "\nbegin\n"
            sql_commands += " pck_warte_constraint_info.prc_define_index (p_table => '{0}'\n".format(table_name.lower())
            sql_commands += "     , p_column => 'boid'\n"
            sql_commands += "     , p_index_type => pck_warte_constraint_info.c_index_type_lix);\n"
            sql_commands += "end;\n/\n\n"

        sql_commands += self.__get_defined_indexes(table_name=table_name.lower())

        sql_commands += "\n\n/*{" + table_name.lower() + "__special_indexes}*/"

        self.__write2File(file_name=file_name, text=sql_commands)
        self.staging_login.runSqlPlus(sql_command="@" + file_name)
        self.__create_synonym_grant(synonym=table_name)

        return self.__compile_valide()

    def __update_reduce(self, table_name, column_id):
        with ora.connect(self.staging_login.getUserName(), self.staging_login.getPassword(),
                         self.staging_login.getConnection()) as conn:
            cur = conn.cursor()
            cur.execute(Sqls.UPDATE_ODS_GENERAED_COLUMNS, COLUMN_USED=EColumnUsed.no.value, TABLE_NAME=table_name,
                        COLUMN_ID=column_id)
            conn.commit()

    def __write2File(self, file_name, text):
        with open(file_name, "w") as f:
            f.write(text)

    def __get_defined_indexes(self, table_name):
        index_script = "\n"
        file_name = os.path.join(os.getcwd(), 'database', 'indexes', self.template_kunde_subdirectory,
                                 '{table_name}.txt'.format(table_name=table_name))
        if not os.path.exists(file_name):
            file_name = os.path.join(os.getcwd(), 'database', 'indexes',
                                     '{table_name}.txt'.format(table_name=table_name))
        if os.path.exists(file_name):
            with codecs.open(filename=file_name, mode="r", encoding="utf-8") as f_in:
                index_script = f_in.read()

        return index_script

    def __print_debug_info(self, debug_info):
        if self.wirte2console:
            print(debug_info)
        else:
            self.log_box.append(debug_info)
            QtCore.QCoreApplication.processEvents()
