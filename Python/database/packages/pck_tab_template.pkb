create or replace package body pck_tab_{table_name} is
  ---------------------------------  Header  ----------------------------
  -- Name         :  pck_tab_{table_name}
  -- Projekt      :  BFI Release 3
  -- Beschreibung :  Aufbereitung fuer ODS_BFI
  --              :  Aufbereitung fuer Tabelle {table_name}
  -- Template:    :  pck_tab_template.pks
  -- Autor        :  MMe
  -- Erstelldatum :  24.05.2017
  -- Auftrags-Nr. :  ??-?????
  --
  -- Skript-Name  :  $Id: pck_tab_template.pkb 9028 2017-06-21 10:58:07Z U10938 $
  -- Revision
  -- Nr.          :  $Revision: 9028 $
  -- User         :  $Author: U10938 $
  -- Datum        :  $Date: 2017-06-21 12:58:07 +0200 (Mi, 21 Jun 2017) $
  -- HeadURL      :  $HeadURL: http://10.10.10.66/svn/DWH_Repository/trunk/DWH_ALLGEMEIN/SYRIUS_R3_DWH/OdsBfiStaging/database/packages/pck_tab_template.pkb $
  --
  -- Aenderungsnachweis :
  -- Ver. Datum       AendererIn  Auftrags-Nr  Aenderung
  -- 001  24.05.2017  MMe         ??-?????     Erstellt.
  ---------------------------------  Header End  -------------------------
  c_svn_revision_body   constant varchar2 (255) := '$Revision: 9222 $';



    function fun_get_svn_revision
     return varchar2 is
     l_revision_header   varchar2 (40);
     l_revision_body     varchar2 (40);
    begin
     l_revision_header := trim (replace (replace (c_svn_revision_header, '$Revision:', ''), '$', ''));
     l_revision_body := trim (replace (replace (c_svn_revision_body, '$Revision:', ''), '$', ''));
     return l_revision_header || ';' || l_revision_body;
    end fun_get_svn_revision;


  function fun_delete_old_data (p_verarbeitung in out nocopy t_verarbeitung%rowtype, p_steuerung in out nocopy t_steuerung%rowtype)
    return boolean;

  function fun_insert_data (p_verarbeitung in out nocopy t_verarbeitung%rowtype, p_steuerung in out nocopy t_steuerung%rowtype)
    return boolean;

  function fun_check_data (p_verarbeitung in out nocopy t_verarbeitung%rowtype, p_steuerung in out nocopy t_steuerung%rowtype)
    return boolean;

  function fun_correct_data (p_verarbeitung in out nocopy t_verarbeitung%rowtype, p_steuerung in out nocopy t_steuerung%rowtype)
    return boolean;
    
  

  function fun_run (p_verarbeitung in out nocopy t_verarbeitung%rowtype, p_steuerung in out nocopy t_steuerung%rowtype)
    return boolean is
    l_return   boolean := true;
  begin
    if l_return then
      l_return := fun_delete_old_data (p_verarbeitung => p_verarbeitung, p_steuerung => p_steuerung);
    end if;

    if l_return then
      l_return := fun_insert_data (p_verarbeitung => p_verarbeitung, p_steuerung => p_steuerung);
    end if;

    if l_return then
      l_return := fun_check_data (p_verarbeitung => p_verarbeitung, p_steuerung => p_steuerung);
    end if;

    if l_return then
      l_return := fun_correct_data (p_verarbeitung => p_verarbeitung, p_steuerung => p_steuerung);
    end if;

    if l_return then
      p_steuerung.table_ladetyp_next := p_steuerung.table_ladetyp;
    end if; 

    return l_return;
  end fun_run;

  function fun_delete_old_data (p_verarbeitung in out nocopy t_verarbeitung%rowtype, p_steuerung in out nocopy t_steuerung%rowtype)
    return boolean is
    l_procname   varchar2 (60) := lower ($$plsql_unit) || '.fun_delete_old_data';
    l_return     boolean := true;
    l_rows       pls_integer;
  begin
    pck_all_log.prc_begin_module (p_name => l_procname);
    pck_all_log.prc_begin_action (p_name => 'VORGAENGIGE DATEN LOESCHEN', p_beschreibung => p_steuerung.table_name || '.');

    if p_steuerung.table_ladetyp_next = pck_def_enviorement_variables.c_load_type_full then
      execute immediate 'truncate table {table_name}';

      pck_warte_constraint_info.prc_drop_all ('{table_name}');
    else
      delete {table_name}
      where pkey in (select pkey
                     from {staging_schema}.{table_name} as of scn (p_verarbeitung.aktueller_scn)
                     where entry_date >= p_verarbeitung.entry_date_von);

      l_rows := sql%rowcount;
      commit;
      pck_all_log.prc_add_delete (p_rows => l_rows);
    end if;

    if l_return then
      pck_all_log.prc_end_action (pck_all_log.c_status_ok);
      pck_all_log.prc_end_module (pck_all_log.c_status_ok);
    else
      pck_all_log.prc_end_action (pck_all_log.c_status_error);
      pck_all_log.prc_end_module (pck_all_log.c_status_error);
    end if;

    return l_return;
  end fun_delete_old_data;

  function fun_insert_data (p_verarbeitung in out nocopy t_verarbeitung%rowtype, p_steuerung in out nocopy t_steuerung%rowtype)
    return boolean is
    l_procname         varchar2 (60) := lower ($$plsql_unit) || '.fun_insert_data';
    l_return           boolean := true;
    l_rows             number;
    l_entry_date_von   t_verarbeitung.entry_date_von%type;
    l_entry_date_bis   t_verarbeitung.entry_date_bis%type;
  begin
    pck_all_log.prc_begin_module (p_name => l_procname);
    pck_all_log.prc_begin_action (p_name => 'LADE TABELLE', p_beschreibung => p_steuerung.table_name || '.');

    l_entry_date_von := p_verarbeitung.entry_date_von;
    l_entry_date_bis := p_verarbeitung.entry_date_bis;

    if p_steuerung.table_ladetyp_next = pck_def_enviorement_variables.c_load_type_full then
      l_entry_date_von := to_timestamp ('01.01.1900 00:00:00.000', 'dd.mm.yyyy hh24:mi:ss.ff');
    end if;

    insert /*+ append */
          into {table_name}
      select {select_column_list}
      from {staging_schema}.{table_name} as of scn (p_verarbeitung.aktueller_scn)
      where     1 = 1
            and entry_date between l_entry_date_von and l_entry_date_bis;

    l_rows := sql%rowcount;
    commit;
    pck_all_log.prc_add_insert (p_rows => l_rows);

    if l_return then
      pck_all_log.prc_end_action (pck_all_log.c_status_ok);

      if p_steuerung.table_ladetyp_next = pck_def_enviorement_variables.c_load_type_full then
        pck_warte_constraint_info.prc_create_all ('{table_name}');
        pck_ods_statistcs.prc_gather_table_stats ('{table_name}');        
      end if;

      pck_all_log.prc_end_module (pck_all_log.c_status_ok);
    else
      pck_all_log.prc_end_action (pck_all_log.c_status_error);
      pck_all_log.prc_end_module (pck_all_log.c_status_error);
    end if;

    return l_return;
  end fun_insert_data;

  function fun_check_data (p_verarbeitung in out nocopy t_verarbeitung%rowtype, p_steuerung in out nocopy t_steuerung%rowtype)
    return boolean is
    l_procname   varchar2 (60) := lower ($$plsql_unit) || '.fun_check_data';
    l_return     boolean := true;
    l_rows       pls_integer;
  begin
    pck_all_log.prc_begin_module (p_name => l_procname);
    pck_all_log.prc_begin_action (p_name => 'PRUEFE TABELLE', p_beschreibung => p_steuerung.table_name || '.');

    if p_steuerung.pruefen = pck_def_enviorement_variables.c_pruefen_yes then
      select coalesce(count (*), 0)
           , coalesce(sum (pkey), 0)
      into p_steuerung.anz_rows_stg
         , p_steuerung.sum_keys_stg
      from {staging_schema}.{table_name} as of scn (p_verarbeitung.aktueller_scn)
      where     1 = 1
            and pkey not in (select pkey_exclude
                             from t_exclude_list
                             where upper(table_name) = upper('{table_name}'));

      select coalesce(count (*), 0)
           , coalesce(sum (pkey), 0)
      into p_steuerung.anz_rows_lokal
         , p_steuerung.sum_keys_lokal
      from {table_name}
      where     1 = 1
            and pkey not in (select pkey_exclude
                             from t_exclude_list
                             where upper(table_name) = upper('{table_name}'));
    else
      p_steuerung.anz_rows_stg := 0;
      p_steuerung.sum_keys_stg := 0;
      p_steuerung.anz_rows_lokal := 0;
      p_steuerung.sum_keys_lokal := 0;
    end if;
    

    if     p_steuerung.anz_rows_stg = p_steuerung.anz_rows_lokal
       and p_steuerung.sum_keys_stg = p_steuerung.sum_keys_lokal then
      p_steuerung.status := pck_def_enviorement_variables.c_status_ok;

      if p_steuerung.table_ladetyp_next = pck_def_enviorement_variables.c_load_type_full then
        p_steuerung.rows_last_analyzed := p_steuerung.anz_rows_lokal;
      end if; 
    else
      p_steuerung.status := pck_def_enviorement_variables.c_status_error;
      l_return := false;
    end if;


    if l_return then
      pck_all_log.prc_end_action (pck_all_log.c_status_ok);
      
      if p_steuerung.table_ladetyp = pck_def_enviorement_variables.c_load_type_incr
        and (coalesce(p_steuerung.anz_rows_lokal, 1) / coalesce(replace(p_steuerung.rows_last_analyzed, 0, 1), 1)) > 1.1 then
        pck_ods_statistcs.prc_gather_table_stats ('{table_name}');    
      end if; 
      
      pck_all_log.prc_end_module (pck_all_log.c_status_ok);
    else
      pck_all_log.prc_end_action (pck_all_log.c_status_error);
      pck_all_log.prc_end_module (pck_all_log.c_status_error);
    end if;

    return l_return;
  end fun_check_data;

  function fun_correct_data (p_verarbeitung in out nocopy t_verarbeitung%rowtype, p_steuerung in out nocopy t_steuerung%rowtype)
    return boolean is
    l_procname   varchar2 (60) := lower ($$plsql_unit) || '.fun_correct_data';
    l_return     boolean := true;
    l_rows       pls_integer;

    cursor c1 is
      select korrektur_id
           , table_name
           , korrektur_sequenz
           , korrektur_ladetyp
           , script
      from t_korrektur
      where     1 = 1
            and upper (table_name) = upper (p_steuerung.table_name)
            and korrektur_ladetyp in (pck_def_enviorement_variables.c_korrektur_ladetyp_incr, p_steuerung.table_ladetyp_next)
      order by korrektur_sequenz;

    type tab_type is table of c1%rowtype;

    l_tab        tab_type;
  begin
    pck_all_log.prc_begin_module (p_name => l_procname);
    pck_all_log.prc_begin_action (p_name => 'AUTOKORREKTUR TABELLE', p_beschreibung => p_steuerung.table_name || '.');

    open c1;

    fetch c1
      bulk   collect into l_tab;

    close c1;

    for i in 1 .. l_tab.count loop
      execute immediate l_tab (i).script;

      l_rows := sql%rowcount;
      commit;
      pck_all_log.prc_add_update (p_rows => l_rows);
    end loop;

    if l_return then
      pck_all_log.prc_end_action (pck_all_log.c_status_ok);

      pck_all_log.prc_end_module (pck_all_log.c_status_ok);
    else
      pck_all_log.prc_end_action (pck_all_log.c_status_error);
      pck_all_log.prc_end_module (pck_all_log.c_status_error);
    end if;

    return l_return;
  end fun_correct_data;
end pck_tab_{table_name};
/