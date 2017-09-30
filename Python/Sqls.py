# -*- coding: utf-8 -*-

DROP_T_ODS_GENERATE_TABLES = r"""drop table t_ods_generate_tables purge;"""

CREATE_T_ODS_GENERATE_TABLES = r"""
create table t_ods_generate_tables
(
  ods_tables_id   raw (16) not null primary key
, table_name      varchar2 (30) not null
, column_id       number not null
, column_name     varchar2 (30) not null
, data_type       varchar2 (30)
, column_used     varchar2 (1)
);
"""

SELECT_KORREKTUR_TABLE_EXISTS = r"""
select count(*) from user_tables where table_name = 'T_KORREKTUR'
"""

SELECT_ODS_SYNONYMS = r"""
select synonym_name
      , table_name
from user_synonyms
where table_owner = :ODS_SCHEMA
order by synonym_name
"""

SELECT_INVALIDE_PACKAGES = r"""
select object_name
           , object_type
           , status
      from user_objects
      where     object_type in ('PACKAGE', 'PACKAGE BODY')
            and status != 'VALID'
      order by object_type, object_name
"""

CMD_COMPILE_ALL = r"""
begin
    DBMS_UTILITY.COMPILE_SCHEMA( '{0}', FALSE );
end;
/
"""

DROP_SYNONYM = r"""DROP SYNONYM {0};"""

SELECT_ODS_TABLE_COLUMNS = r"""
select table_name
      , column_id
      , column_name
      , data_type
      , data_length
      , data_precision
      , data_scale
      , nullable
from all_tab_columns
where     1 = 1
      and owner = :ODS_SCHEMA
      and table_name = :TABLE_NAME
order by column_id
"""

INSERT_T_ODS_GENERATE_TABLES = r"""
INSERT INTO T_ODS_GENERATE_TABLES VALUES (SYS_GUID(), :TABLE_NAME, :COLUMN_ID, :COLUMN_NAME, :DATA_TYPE, :COLUMN_USED)
"""

DELETE_T_ODS_GENERATE_TABLE = r"""
DELETE T_ODS_GENERATE_TABLES WHERE TABLE_NAME = :TABLE_NAME
"""

SELECT_ODS_GENERAED_COLUMNS = r"""
select ods_tables_id
      , table_name
      , column_id
      , column_name
      , data_type
      , column_used
from t_ods_generate_tables
where     1 = 1
      and table_name = :TABLE_NAME
      and column_used = 'Y'
order by column_id
"""

SELECT_ALL_ODS_GENERAED_COLUMNS = r"""
select cast(ods_tables_id as varchar2(32)) as ods_tables_id
      , table_name
      , column_id
      , column_name
      , data_type
      , column_used
from t_ods_generate_tables
where     1 = 1
order by table_name, column_id
"""


SELECT_ODS_GENERATED_TABLES = r"""
select table_name
from t_ods_generate_tables
group by table_name
order by table_name
"""

UPDATE_ODS_GENERAED_COLUMNS = r"""
update t_ods_generate_tables set column_used = :COLUMN_USED where table_name = :TABLE_NAME and column_id = :COLUMN_ID
"""

SELECT_ODS_BFI_TABLE_LIST4LOAD = r"""
select table_name
from user_tables
where 1 = 1
and substr(table_name,1,2) != 'T_'
order by table_name
"""

SELECT_ODS_BFI_TABLE_LIST_WITH_SCRIPT = r"""
select distinct table_name
from t_korrektur
where 1 = 1
order by table_name
"""

SELECT_KORREKTUR_TABLE_LIST = r"""
select cast(korrektur_id as varchar2(32)) as korrektur_id
      , table_name
      , korrektur_sequenz
      , korrektur_ladetyp
      , script
      , pkey_exclude
      , script_exclude
from t_korrektur
order by table_name, korrektur_sequenz
"""

DELETE_KORREKTUR_TABLE_ROW = r"""
delete t_korrektur where korrektur_id = :KORREKTUR_ID
"""

INSERT_KORREKTUR_TABLE_ROW = r"""
insert into t_korrektur values (sys_guid(), :TABLE_NAME, :KORREKTUR_SEQUENZ, :KORREKTUR_LADETYP, :SCRIPT, :PKEY_EXCLUDE, :SCRIPT_EXCLUDE )
"""

INSERT_KORREKTUR_TABLE_IMPORT = r"""
insert into t_korrektur values (:KORREKTUR_ID, :TABLE_NAME, :KORREKTUR_SEQUENZ, :KORREKTUR_LADETYP, :SCRIPT, :PKEY_EXCLUDE, :SCRIPT_EXCLUDE)
"""

TRUNCATE_KORREKTUR_TABLE = r"""
truncate table t_korrektur
"""

UPDATE_KORREKTUR_TABLE_ROW = r"""
update t_korrektur
 set table_name = :TABLE_NAME
 , korrektur_sequenz = :KORREKTUR_SEQUENZ
 , korrektur_ladetyp = :KORREKTUR_LADETYP
 , script = :SCRIPT
 , pkey_exclude = :PKEY_EXCLUDE
 , script_exclude = :SCRIPT_EXCLUDE
 where korrektur_id = :KORREKTUR_ID
"""
