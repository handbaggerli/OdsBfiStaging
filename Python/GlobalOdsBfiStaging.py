# -*- coding: utf-8 -*-
__author__ = 'U10938'

import cx_Oracle as ora
import Sqls
import os
import json


class GlobalOdsBfiStaging():
    def __init__(self, login_bfi, login_ods_bfi_staging, schema_ods, schema_staging, schema_chk,
                 template_kunde_subdirectory, output_path):
        self.login_bfi = login_bfi
        self.login_ods_bfi_staging = login_ods_bfi_staging
        self.schema_ods = schema_ods
        self.schema_staging = schema_staging
        self.schema_chk = schema_chk
        self.template_kunde_subdirectory = template_kunde_subdirectory
        self.output_path = output_path
        self.cbo_kunde_subdirectory_auswahl = []
        self.cbo_kunde_subdirectory_auswahl.append([0, "EGK (KND031)", "KND031"])
        self.cbo_kunde_subdirectory_auswahl.append([1, "INNOVA (KND038)", "KND038"])
        self.cbo_kunde_subdirectory_auswahl.append([2, "AQUILANA (KND108)", "KND108"])
        self.cbo_kunde_subdirectory_auswahl.append([3, "OEKK (KND200)", "KND200"])
        self.cbo_kunde_subdirectory_auswahl.append([4, "SWICA (KND300)", "KND300"])
        self.cbo_kunde_subdirectory_auswahl.append([5, "CONCORDIA (KND517)", "KND517"])
        self.cbo_kunde_subdirectory_auswahl.append([6, "SOLIDA (KND525)", "KND525"])
        self.cbo_kunde_subdirectory_auswahl.append([7, "AXA (KND925)", "KND925"])
        self.cbo_action_auswahl = []
        self.cbo_action_auswahl.append([0, "ODS BFI Staging Tabellen Initial erstellen.",
                                        "Löscht sämtliche Objekte bis auf die Korrekturtabelle und generiert einen neuen Load."])
        self.cbo_action_auswahl.append([1, "ODS BFI Staging Tabellen Inkremental erstellen.",
                                        "Sucht sich das erste Synonym in BFI Schema welches auf das ODS Schema zeigt und erstellt von diesem Punkt an den Load."])
        self.cbo_action_auswahl.append([2, "Ladepackages anhand der Tabellen erstellen.",
                                        "Erstellt Ladepackages anhand der Struktur im Schema ODS_BFI. Die ersetzten ODS Tabellen muessen installiert sein."])
        self.cbo_action_auswahl.append(
            [3, "Korrekturtabelle bearbeiten.", "Öffnet das Fenster für die Korrekturtabelle zu berabeiten."])
        self.cbo_action_auswahl.append([4, "Definition der ODS - BFI Tabellen exportieren.",
                                        "Eportiert die Tabelle T_ODS_GENERATE_TABLE für den Import als SQL Script."])
        self.cbo_corr_load_type = []
        self.cbo_corr_load_type.append([0, "FULL"])
        self.cbo_corr_load_type.append([1, "INCR"])
        self.cbo_corr_action = []
        self.cbo_corr_action.append([0, "Korrekturscript hinzufuegen", "Fügt ein neues Korrekturscript hinzug."])
        self.cbo_corr_action.append([1, "Speichern", "Speichert die Veränderung."])
        self.cbo_corr_action.append([2, "Loeschen", "Löscht den selektierten Datensatz."])
        self.cbo_corr_action.append(
            [3, "Export Korrekturtabelle", "Exportiert die Korrekturtabelle in ein JSONL File."])
        self.cbo_corr_action.append(
            [4, "Import Korrekturtabelle", "Importiert die Korrekturtabelle von einem JSONL File."])

        self.correct_table_header = ["Korrektur ID", "Table Name", "Sequenz", "Ladetyp", "Script", "Pkeys Exclude", "Script Exclude"]

    def getCbo_kunde_subdirectory_auswahl(self):
        return self.cbo_kunde_subdirectory_auswahl

    def getCbo_action_auswahl(self):
        return self.cbo_action_auswahl;

    def getCbo_corr_load_type(self):
        return self.cbo_corr_load_type

    def getCbo_corr_action(self):
        return self.cbo_corr_action

    def getTemplate_kunde_subdirectory(self):
        return self.template_kunde_subdirectory

    def setTemplate_kunde_subdirectory(self, template_kunde_subdirectory):
        self.template_kunde_subdirectory = template_kunde_subdirectory

    def getLogin_bfi(self):
        return self.login_bfi

    def getLogin_ods_bfi_staging(self):
        return self.login_ods_bfi_staging

    def getOutput_path(self):
        return self.output_path

    def setOutput_path(self, output_path):
        self.output_path = output_path

    def getSchema_ods(self):
        return self.schema_ods

    def setSchema_ods(self, schema_ods):
        self.schema_ods = schema_ods

    def getSchema_staging(self):
        return self.schema_staging

    def setSchema_staging(self, schema_staging):
        self.schema_staging = schema_staging

    def getSchema_chk(self):
        return self.schema_chk

    def setSchema_chk(self, schema_chk):
        self.schema_chk = schema_chk

    def getCorrect_table_header(self):
        return self.correct_table_header

    def getAllUsedOdsTables(self):
        ods_tables = []
        conn = ora.connect(self.login_ods_bfi_staging.getUserName(), self.login_ods_bfi_staging.getPassword(),
                           self.login_ods_bfi_staging.getConnection())
        cur = conn.cursor()
        cur.execute(Sqls.SELECT_ODS_BFI_TABLE_LIST4LOAD)
        for row in cur:
            ods_tables.append(row[0])
        conn.close()
        return ods_tables

    def getAllUsedOdsTablesWithScript(self):
        ods_tables = []
        with ora.connect(self.login_ods_bfi_staging.getUserName(), self.login_ods_bfi_staging.getPassword(),
                         self.login_ods_bfi_staging.getConnection()) as conn:
            cur = conn.cursor()
            cur.execute(Sqls.SELECT_ODS_BFI_TABLE_LIST_WITH_SCRIPT)
            for row in cur:
                ods_tables.append(row[0])
        return ods_tables

    def getCorrectTableData(self):
        table_data = []
        with ora.connect(self.login_ods_bfi_staging.getUserName(), self.login_ods_bfi_staging.getPassword(),
                         self.login_ods_bfi_staging.getConnection()) as conn:
            cur = conn.cursor()
            cur.execute(Sqls.SELECT_KORREKTUR_TABLE_LIST)
            for row in cur:
                table_data.append([row[0], row[1], row[2], row[3], str(row[4]), row[5], str(row[6])])
        return table_data

    def insertCorrectTableRow(self, table_name, sequenz, load_type, script, pkey_exclude, script_exclude):
        if script_exclude == "None":
            script_exclude = ""
        with ora.connect(self.login_ods_bfi_staging.getUserName(), self.login_ods_bfi_staging.getPassword(),
                         self.login_ods_bfi_staging.getConnection()) as conn:
            cur = conn.cursor()
            cur.execute(Sqls.INSERT_KORREKTUR_TABLE_ROW, TABLE_NAME=table_name,
                        KORREKTUR_SEQUENZ=sequenz,
                        KORREKTUR_LADETYP=load_type,
                        SCRIPT=script,
                        PKEY_EXCLUDE=pkey_exclude,
                        SCRIPT_EXCLUDE=script_exclude)
            conn.commit()

    def updateCorrectTableRow(self, korrektur_id, table_name, sequenz, load_type, script, pkey_exclude, script_exclude):
        if script_exclude == "None":
            script_exclude = ""
        with ora.connect(self.login_ods_bfi_staging.getUserName(), self.login_ods_bfi_staging.getPassword(),
                         self.login_ods_bfi_staging.getConnection()) as conn:
            cur = conn.cursor()
            cur.execute(Sqls.UPDATE_KORREKTUR_TABLE_ROW, TABLE_NAME=table_name,
                        KORREKTUR_SEQUENZ=sequenz,
                        KORREKTUR_LADETYP=load_type,
                        SCRIPT=script,
                        PKEY_EXCLUDE=pkey_exclude,
                        SCRIPT_EXCLUDE=script_exclude,
                        KORREKTUR_ID=korrektur_id
                        )
            conn.commit()

    def deleteCorrectTableRow(self, korrektur_id):
        with ora.connect(self.login_ods_bfi_staging.getUserName(), self.login_ods_bfi_staging.getPassword(),
                         self.login_ods_bfi_staging.getConnection()) as conn:
            cur = conn.cursor()
            cur.execute(Sqls.DELETE_KORREKTUR_TABLE_ROW,
                        KORREKTUR_ID=korrektur_id
                        )
            conn.commit()

    def export_to_file(self, filename):
        file, extension = os.path.splitext(filename)
        if extension is not ".jsonl":
            filename = file + ".jsonl"
        with open(filename, "w") as f:
            for korrektur_id, table_name, korrektur_sequenz, korrektur_ladetyp, script, pkey_exclude, script_exclude in self.getCorrectTableData():
                dic_data = {}
                dic_data["korrektur_id"] = korrektur_id
                dic_data["table_name"] = table_name
                dic_data["korrektur_sequenz"] = korrektur_sequenz
                dic_data["korrektur_ladetyp"] = korrektur_ladetyp
                dic_data["script"] = script
                dic_data["pkey_exclude"] = pkey_exclude
                dic_data["script_exclude"] = script_exclude
                f.write(json.dumps(dic_data) + "\n")

    def import_from_file(self, filename):
        element_list = []
        with open(filename, "r") as f:
            for line in f:
                dic_data = json.loads(line)
                if dic_data["script_exclude"] == "None":
                    dic_data["script_exclude"] = ""
                element_list.append([dic_data["korrektur_id"], dic_data["table_name"],
                                     dic_data["korrektur_sequenz"], dic_data["korrektur_ladetyp"],
                                     dic_data["script"], dic_data["pkey_exclude"], dic_data["script_exclude"]])

        with ora.connect(self.login_ods_bfi_staging.getUserName(), self.login_ods_bfi_staging.getPassword(),
                         self.login_ods_bfi_staging.getConnection()) as conn:
            cur = conn.cursor()
            cur.execute(Sqls.TRUNCATE_KORREKTUR_TABLE)
            for korrektur_id, table_name, korrektur_sequenz, korrektur_ladetyp, script, pkey_exclude, script_exclude in element_list:
                cur.execute(Sqls.INSERT_KORREKTUR_TABLE_IMPORT, KORREKTUR_ID=korrektur_id, TABLE_NAME=table_name,
                            KORREKTUR_SEQUENZ=korrektur_sequenz, KORREKTUR_LADETYP=korrektur_ladetyp,
                            SCRIPT=script, PKEY_EXCLUDE=pkey_exclude, SCRIPT_EXCLUDE=script_exclude)
            conn.commit()

    def export_ods_bfi_table_definition(self):
        filename = os.path.join(self.getOutput_path(), "config", "insert_t_ods_generate_tables.sql_not_execute")
        table_list = []
        row_list = []
        with ora.connect(self.login_ods_bfi_staging.getUserName(), self.login_ods_bfi_staging.getPassword(),
                         self.login_ods_bfi_staging.getConnection()) as conn:
            cur = conn.cursor()
            cur.execute(Sqls.SELECT_ODS_GENERATED_TABLES)
            for row in cur:
                table_list.append(row[0])
            cur.execute(Sqls.SELECT_ALL_ODS_GENERAED_COLUMNS)
            for row in cur:
                row_list.append([row[0], row[1], int(row[2]), row[3], row[4], row[5]])

        with open(filename, "w") as f:
            for table in table_list:
                f.write("delete t_ods_generate_tables where table_name = '{table}';\n".format(table=table))
            for ods_tablel_id, table_name, column_id, column_name, data_type, column_used in row_list:
                ins_str = (
                    "insert into t_ods_generate_tables values ('{ods_tablel_id}'"
                    ", '{table_name}', {column_id}, '{column_name}'"
                    ", '{data_type}', '{column_used}');\n"
                )
                f.write(ins_str.format(ods_tablel_id=ods_tablel_id,
                                       table_name=table_name,
                                       column_id=column_id,
                                       column_name=column_name,
                                       data_type=data_type,
                                       column_used=column_used))
            f.write("commit;\n")


