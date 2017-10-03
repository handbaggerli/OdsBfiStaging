create or replace package body pck_init_verarbeitung is
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
  -- Skript-Name  :  $Id: pck_init_verarbeitung.pkb 8964 2017-06-01 08:38:23Z U10938 $
  -- Revision
  -- Nr.          :  $Revision: 8964 $
  -- User         :  $Author: U10938 $
  -- Datum        :  $Date: 2017-06-01 10:38:23 +0200 (Do, 01 Jun 2017) $
  -- HeadURL      :  $HeadURL: http://10.10.10.66/svn/DWH_Repository/trunk/DWH_ALLGEMEIN/SYRIUS_R3_DWH/OdsBfiStaging/database/packages/pck_init_verarbeitung.pkb $
  --
  -- Aenderungsnachweis :
  -- Ver. Datum       AendererIn  Auftrags-Nr  Aenderung
  -- 001  23.05.2017  MMe         ??-?????     Erstellt.
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

  function fun_build_exception_list
    return boolean;

  function fun_check_abbruch (p_verarbeitung in out nocopy t_verarbeitung%rowtype, p_continue in out nocopy boolean)
    return boolean;

  function fun_initialize_new_load (p_load_type in pck_def_enviorement_variables.t_load_type, p_verarbeitung in out nocopy t_verarbeitung%rowtype)
    return boolean;

  function fun_init_verarbeitung (p_load_type in pck_def_enviorement_variables.t_load_type, p_verarbeitung in out nocopy t_verarbeitung%rowtype)
    return boolean is
    l_procname   varchar2 (60) := lower ($$plsql_unit) || '.fun_init_verarbeitung';
    l_return     boolean := true;
    l_continue   boolean := true;
  begin
    pck_all_log.prc_begin_module (p_name => l_procname);

    if l_return then
      l_return := fun_check_abbruch (p_verarbeitung => p_verarbeitung, p_continue => l_continue);
    end if;

    if l_return then
      l_return := fun_build_exception_list;
    end if;

    if     l_return
       and l_continue then
      l_return := fun_initialize_new_load (p_load_type => p_load_type, p_verarbeitung => p_verarbeitung);
    end if;

    if l_return then
      pck_all_log.prc_end_module (pck_all_log.c_status_ok);
    else
      pck_all_log.prc_end_module (pck_all_log.c_status_error);
    end if;

    return l_return;
  exception
    when others then
      pck_all_log.prc_error (p_meldung => l_procname || ' mit einem Fehler beendet. ->' || sqlerrm, p_sqlerrm => sqlerrm);
      pck_all_log.prc_end_module (pck_all_log.c_status_error);
      l_return := false;
      return l_return;
  end fun_init_verarbeitung;

  function tfn_get_exclude_list (p_table_name in t_korrektur.table_name%type, p_exclude_script in t_korrektur.script_exclude%type)
    return type_exclude_list_tab
    pipelined is
    l_row   type_exclude_list_row;

    type r_cursor is ref cursor;

    c1      r_cursor;
  begin
    l_row.p_table_name := p_table_name;

    open c1 for p_exclude_script;

    loop
      fetch c1
        into   l_row.p_pkey;

      exit when c1%notfound;
      pipe row (l_row);
    end loop;

    return;
  end tfn_get_exclude_list;

  function fun_check_abbruch (p_verarbeitung in out nocopy t_verarbeitung%rowtype, p_continue in out nocopy boolean)
    return boolean is
    l_procname   varchar2 (60) := lower ($$plsql_unit) || '.fun_check_abbruch';
    l_return     boolean := true;

    cursor c1 is
      select verarbeitung_id
           , entry_date_von
           , entry_date_bis
           , aktueller_scn
           , ladetyp
           , startzeit
           , endzeit
      from t_verarbeitung
      where     startzeit is not null
            and endzeit is null;

    type tab_type is table of c1%rowtype;

    l_tab        tab_type;
  begin
    pck_all_log.prc_begin_module (p_name => l_procname);
    pck_all_log.prc_begin_action (p_name => 'CHECK', p_beschreibung => 'Pruefen ob letzte Load erfolgreich war.');

    open c1;

    fetch c1
      bulk   collect into l_tab;

    close c1;

    if l_tab.count = 0 then
      p_continue := true;
    end if;

    for i in 1 .. l_tab.count loop
      p_continue := false;
      p_verarbeitung.verarbeitung_id := l_tab (i).verarbeitung_id;
      p_verarbeitung.entry_date_von := l_tab (i).entry_date_von;
      p_verarbeitung.entry_date_bis := l_tab (i).entry_date_bis;
      p_verarbeitung.aktueller_scn := l_tab (i).aktueller_scn;
      p_verarbeitung.ladetyp := l_tab (i).ladetyp;
      p_verarbeitung.startzeit := l_tab (i).startzeit;
      p_verarbeitung.endzeit := l_tab (i).endzeit;
    end loop;

    if l_return then
      pck_all_log.prc_end_action (pck_all_log.c_status_ok);
      pck_all_log.prc_end_module (pck_all_log.c_status_ok);
    else
      pck_all_log.prc_end_action (pck_all_log.c_status_error);
      pck_all_log.prc_end_module (pck_all_log.c_status_error);
    end if;

    return l_return;
  end fun_check_abbruch;

  -----

  function fun_build_exception_list
    return boolean is
    l_procname             varchar2 (60) := lower ($$plsql_unit) || '.fun_build_exception_list';
    l_return               boolean := true;

    cursor c_exclude_script is
      select korrektur_id
           , table_name
           , script_exclude
      from t_korrektur
      where     1 = 1
            and script_exclude is not null
             and length(script_exclude) > 5 ; ---> Not null scheint auf CLOB nicht immer korrekt zu funktionieren.

    type tab_exclude_script is table of c_exclude_script%rowtype;

    l_tab_exclude_script   tab_exclude_script;
  begin
    pck_all_log.prc_begin_module (p_name => l_procname);
    pck_all_log.prc_begin_action (p_name => 'INIT', p_beschreibung => 'Exception List wird aufgebaut.');

    execute immediate 'truncate table t_exclude_list_tmp';

    execute immediate 'truncate table t_exclude_list';

    open c_exclude_script;

    fetch c_exclude_script
      bulk   collect into l_tab_exclude_script;

    close c_exclude_script;

    for i in 1 .. l_tab_exclude_script.count loop
      insert into t_exclude_list_tmp
        select *
        from table (pck_init_verarbeitung.tfn_get_exclude_list (p_table_name => l_tab_exclude_script (i).table_name, p_exclude_script => l_tab_exclude_script (i).script_exclude));

      commit;
    end loop;

    -- Fix definierte Pkeys in einzelne Felder aufsplitten und in Temp abfüllen.
    insert into t_exclude_list_tmp
      with exclude_list as
             (select table_name
                   , pkey_exclude
                   , pkey_exclude as pkey_exclude_orig
              from t_korrektur
              where     1 = 1
                    and pkey_exclude is not null)
      select distinct table_name
                    , pkey_exclude
      from (select table_name
                 , pkey_exclude_orig
                 , trim (regexp_substr (excl.pkey_exclude
                                      , '[^,]+'
                                      , 1
                                      , levels.column_value
                                       )
                        )
                     as pkey_exclude
            from exclude_list excl
               , table (cast (multiset (select level
                                        from dual
                                        connect by level <= length (regexp_replace (excl.pkey_exclude, '[^,]+')) + 1
                                       ) as sys.odcinumberlist
                             )
                       ) levels);

    commit;

    insert into t_exclude_list
      select distinct table_name
                    , pkey_exclude
      from t_exclude_list_tmp
      order by table_name, pkey_exclude;

    commit;

    if l_return then
      pck_all_log.prc_end_action (pck_all_log.c_status_ok);
      pck_warte_schema.prc_gather_table_stats ('t_exclude_list');
      pck_all_log.prc_end_module (pck_all_log.c_status_ok);
    else
      pck_all_log.prc_end_action (pck_all_log.c_status_error);
      pck_all_log.prc_end_module (pck_all_log.c_status_error);
    end if;

    return l_return;
  exception
    when others then
      pck_all_log.prc_error (p_meldung => l_procname || ' mit einem Fehler beendet. ->' || sqlerrm, p_sqlerrm => sqlerrm);
      pck_all_log.prc_end_action (pck_all_log.c_status_error);
      pck_all_log.prc_end_module (pck_all_log.c_status_error);
      l_return := false;
      return l_return;
  end fun_build_exception_list;

  function fun_initialize_new_load (p_load_type in pck_def_enviorement_variables.t_load_type, p_verarbeitung in out nocopy t_verarbeitung%rowtype)
    return boolean is
    l_procname         varchar2 (60) := lower ($$plsql_unit) || '.fun_initialize_new_load';
    l_return           boolean := true;
    l_aktueller_scn    t_verarbeitung.aktueller_scn%type;
    l_entry_date_von   t_verarbeitung.entry_date_von%type;
    l_entry_date_bis   t_verarbeitung.entry_date_bis%type;

    cursor c_pps is
      select pkey
           , laden_von
           , laden_bis
           , laden_scn
           , status
      from &&check_schema..t_odstables_refresh
      order by laden_bis desc;

    type tab_pps is table of c_pps%rowtype;

    l_tab_pps          tab_pps;
  begin
    pck_all_log.prc_begin_module (p_name => l_procname);
    pck_all_log.prc_begin_action (p_name => 'INIT', p_beschreibung => 'Neuer Load wird initialisiert fuer Ladetyp ' || p_load_type || '.');

    select coalesce (max (entry_date_bis), to_timestamp ('01.01.1900 00:00:00.0000', 'dd.mm.yyyy hh24:mi:ss.ff'))
    into l_entry_date_von
    from t_verarbeitung
    where endzeit is not null;

    l_entry_date_von := l_entry_date_von - to_dsinterval ('0 00:00:10.0000');

    if p_load_type = pck_def_enviorement_variables.c_load_initial then
      execute immediate 'truncate table t_verarbeitung';

      l_entry_date_von := to_timestamp ('01.01.1900 00:00:00.0000', 'dd.mm.yyyy hh24:mi:ss.ff');
      l_entry_date_bis := systimestamp - to_dsinterval ('0 00:00:10.0000');

      select timestamp_to_scn (l_entry_date_bis)
      into l_aktueller_scn
      from dual;

      commit;
    elsif p_load_type = pck_def_enviorement_variables.c_load_pps then
      open c_pps;

      fetch c_pps
        bulk   collect into l_tab_pps;

      close c_pps;

      for i in 1 .. 1 loop
        l_entry_date_bis := l_tab_pps (1).laden_bis;
        l_aktueller_scn := l_tab_pps (1).laden_scn;
      end loop;
    elsif p_load_type = pck_def_enviorement_variables.c_load_manuell then
      l_entry_date_bis := systimestamp - to_dsinterval ('0 00:00:10.0000');

      select timestamp_to_scn (l_entry_date_bis)
      into l_aktueller_scn
      from dual;
    end if;

    p_verarbeitung.verarbeitung_id := sys_guid ();
    p_verarbeitung.entry_date_von := l_entry_date_von;
    p_verarbeitung.entry_date_bis := l_entry_date_bis;
    p_verarbeitung.aktueller_scn := l_aktueller_scn;
    p_verarbeitung.ladetyp := p_load_type;
    p_verarbeitung.startzeit := systimestamp;
    p_verarbeitung.endzeit := to_timestamp (null);

    insert into t_verarbeitung (verarbeitung_id
                              , entry_date_von
                              , entry_date_bis
                              , aktueller_scn
                              , ladetyp
                              , startzeit
                              , endzeit
                               )
    values (p_verarbeitung.verarbeitung_id
          , p_verarbeitung.entry_date_von
          , p_verarbeitung.entry_date_bis
          , p_verarbeitung.aktueller_scn
          , p_verarbeitung.ladetyp
          , p_verarbeitung.startzeit
          , p_verarbeitung.endzeit
           );

    commit;

    update t_steuerung
    set startzeit = null
      , endzeit = null
      , anz_rows_stg = null
      , sum_keys_stg = null
      , anz_rows_lokal = null
      , sum_keys_lokal = null
      , status = null;

    commit;

    if p_verarbeitung.entry_date_von < sysdate - 30 then
      update t_steuerung
      set table_ladetyp_next = pck_def_enviorement_variables.c_load_type_full;
    end if;

    ---
    if l_return then
      pck_all_log.prc_end_action (pck_all_log.c_status_ok);
      pck_all_log.prc_end_module (pck_all_log.c_status_ok);
    else
      pck_all_log.prc_end_action (pck_all_log.c_status_error);
      pck_all_log.prc_end_module (pck_all_log.c_status_error);
    end if;

    return l_return;
  end fun_initialize_new_load;
end pck_init_verarbeitung;
/
