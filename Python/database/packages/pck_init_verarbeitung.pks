create or replace package pck_init_verarbeitung is
  ---------------------  header  ----------------------------
  -- Name         :  pck_init_verarbeitung
  -- Projekt      :  BFI Release 3
  -- Beschreibung :  Aufbereitung fuer ODS_BFI
  --                 Initialisiert eine neue Verarbeitung oder im Falle eines Abbruchs
  --                 werden die alten Parameter mitgegeben.
  -- Autor        :  MMe
  -- Erstelldatum :  23.05.2017
  -- Auftrags-Nr. :  ??-?????
  --
  -- Skript-Name  :  $Id: pck_init_verarbeitung.pks 8964 2017-06-01 08:38:23Z U10938 $
  -- Revision
  -- Nr.          :  $Revision: 8964 $
  -- User         :  $Author: U10938 $
  -- Datum        :  $Date: 2017-06-01 10:38:23 +0200 (Do, 01 Jun 2017) $
  -- HeadURL      :  $HeadURL: http://10.10.10.66/svn/DWH_Repository/trunk/DWH_ALLGEMEIN/SYRIUS_R3_DWH/OdsBfiStaging/database/packages/pck_init_verarbeitung.pks $
  --
  -- Aenderungsnachweis :
  -- Ver. Datum       AendererIn  Auftrags-Nr  Aenderung
  -- 001  23.05.2017  MMe         ??-?????     Erstellt.
  ---------------------------------  Header End  -------------------------

  c_svn_revision_header   constant varchar2 (255) := '$Revision: 9222 $';

  type type_exclude_list_row is record
  (
    p_table_name   t_exclude_list.table_name%type
  , p_pkey         t_exclude_list.pkey_exclude%type
  );

  type type_exclude_list_tab is table of type_exclude_list_row;

  function fun_get_svn_revision
    return varchar2;

  function fun_init_verarbeitung (p_load_type in pck_def_enviorement_variables.t_load_type, p_verarbeitung in out nocopy t_verarbeitung%rowtype)
    return boolean;

  function tfn_get_exclude_list (p_table_name in t_korrektur.table_name%type, p_exclude_script in t_korrektur.script_exclude%type)
    return type_exclude_list_tab
    pipelined;
end pck_init_verarbeitung;
/
