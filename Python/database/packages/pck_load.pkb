create or replace package body pck_load is
  ---------------------------------  Header  ----------------------------
  -- Name         :  pck_load
  -- Projekt      :  BFI Release 3
  -- Beschreibung :  Aufbereitung fuer ODS_BFI
  --
  -- Autor        :  MMe
  -- Erstelldatum :  23.05.2017
  -- Auftrags-Nr. :  ??-?????
  --
  -- Skript-Name  :  $Id: pck_load.pkb 8964 2017-06-01 08:38:23Z U10938 $
  -- Revision
  -- Nr.          :  $Revision: 8964 $
  -- User         :  $Author: U10938 $
  -- Datum        :  $Date: 2017-06-01 10:38:23 +0200 (Do, 01 Jun 2017) $
  -- HeadURL      :  $HeadURL: http://10.10.10.66/svn/DWH_Repository/trunk/DWH_ALLGEMEIN/SYRIUS_R3_DWH/OdsBfiStaging/database/packages/pck_load.pkb $
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


  function fun_verarbeitung (p_verarbeitung in out nocopy t_verarbeitung%rowtype)
    return boolean;

  procedure prc_update_steuerung (p_steuerung in out nocopy t_steuerung%rowtype);

  function fun_modul_aufruf (p_verarbeitung in out nocopy t_verarbeitung%rowtype, p_steuerung in out nocopy t_steuerung%rowtype)
    return boolean;

  function fun_run (p_mandant in varchar2, p_load_type in pck_def_enviorement_variables.t_load_type)
    return number is
    l_log_id         number;
    l_procname       varchar2 (60) := lower ($$plsql_unit) || '.fun_run';
    l_return         boolean := true;
    l_applikation    varchar2 (60) := 'ODS BFI AUFBEREITUNG';
    l_verarbeitung   t_verarbeitung%rowtype;
  begin
    execute immediate 'alter session set nls_numeric_characters = ''.,'' ';

    execute immediate 'alter session set nls_timestamp_format = ''dd.mm.yyyy hh24:mi:ss.ff'' ';

    execute immediate 'alter session set nls_timestamp_tz_format = ''dd.mm.yyyy hh24:mi:ss.ff'' ';

    execute immediate 'alter session set nls_date_format = ''dd.mm.yyyy hh24:mi:ss'' ';

    execute immediate 'alter session set skip_unusable_indexes = true';

    execute immediate 'alter session enable parallel dml';

    execute immediate 'alter session set query_rewrite_integrity = trusted';

    execute immediate 'alter session set ddl_lock_timeout = 1800';

    execute immediate 'alter session set time_zone = dbtimezone';

    l_log_id := pck_all_log.fun_begin_job (p_applikation => l_applikation, p_mandant => all_lib.fun_get_mandant (p_mandant), p_beschreibung => 'Aufbereitung fuer das ODS BFI Schema');
    pck_all_log.prc_begin_module (p_name => l_procname);

    if l_return then
      l_return := pck_init_verarbeitung.fun_init_verarbeitung (p_load_type => p_load_type, p_verarbeitung => l_verarbeitung);
    end if;

    if l_return then
      l_return := fun_verarbeitung (p_verarbeitung => l_verarbeitung);
    end if;

    if l_return then
      pck_all_log.prc_end_module (pck_all_log.c_status_ok);
      pck_all_log.prc_end_job (pck_all_log.c_status_ok);
      return 0;
    else
      pck_all_log.prc_error (p_meldung => l_procname || ' mit einem Fehler beendet. ->' || sqlerrm, p_sqlerrm => sqlerrm);
      pck_all_log.prc_end_module (pck_all_log.c_status_error);
      pck_all_log.prc_end_job (pck_all_log.c_status_error);
      raise_application_error (-20100, l_applikation || ' mit Fehlern beendet');
    end if;

    return 0;
  exception
    when others then
      pck_all_log.prc_error (p_meldung => l_procname || ' mit einem Fehler beendet. ->' || sqlerrm, p_sqlerrm => sqlerrm);
      pck_all_log.prc_end_module (pck_all_log.c_status_error);
      pck_all_log.prc_end_job (pck_all_log.c_status_error);
      commit;
      return -99;
  end fun_run;

  function fun_verarbeitung (p_verarbeitung in out nocopy t_verarbeitung%rowtype)
    return boolean is
    l_procname        varchar2 (60) := lower ($$plsql_unit) || '.fun_verarbeitung';
    l_return          boolean := true;

    cursor c_steuerung is
      select steuerung_id
           , table_name
		   , schritt_nr
           , table_ladetyp
           , table_ladetyp_next
           , pruefen
           , kommand
           , startzeit
           , endzeit
           , anz_rows_stg
           , sum_keys_stg
           , anz_rows_lokal
           , sum_keys_lokal
		   , rows_last_analyzed
           , status
      from t_steuerung
      where     1 = 1
            and endzeit is null
			and schritt_nr > 0
      order by schritt_nr;

    type tab_steuerung_type is table of c_steuerung%rowtype;

    l_tab_steuerung   tab_steuerung_type;
  begin
    pck_all_log.prc_begin_module (p_name => l_procname);
    pck_all_log.prc_begin_action (p_name => 'STEUERUNG', p_beschreibung => 'Steuerung wird initialisiert.');

    open c_steuerung;

    fetch c_steuerung
      bulk   collect into l_tab_steuerung;

    close c_steuerung;

    for i in 1 .. l_tab_steuerung.count loop
      if l_return then
        l_tab_steuerung (i).startzeit := systimestamp;
        prc_update_steuerung (p_steuerung => l_tab_steuerung (i));

        l_return := fun_modul_aufruf (p_verarbeitung => p_verarbeitung, p_steuerung => l_tab_steuerung (i));

        if l_return then
          l_tab_steuerung (i).endzeit := systimestamp;
          prc_update_steuerung (p_steuerung => l_tab_steuerung (i));
        end if;
      end if;
    end loop;

    if l_return then
      update t_verarbeitung
      set endzeit = systimestamp
      where verarbeitung_id = p_verarbeitung.verarbeitung_id;
    end if;

    commit;

    if l_return then
      pck_all_log.prc_end_action (pck_all_log.c_status_ok);
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

      commit;
      return l_return;
  end fun_verarbeitung;

  procedure prc_update_steuerung (p_steuerung in out nocopy t_steuerung%rowtype) is
  begin
    update t_steuerung
    set table_ladetyp_next = p_steuerung.table_ladetyp_next
      , startzeit = p_steuerung.startzeit
      , endzeit = p_steuerung.endzeit
      , anz_rows_stg = p_steuerung.anz_rows_stg
      , sum_keys_stg = p_steuerung.sum_keys_stg
      , anz_rows_lokal = p_steuerung.anz_rows_lokal
      , sum_keys_lokal = p_steuerung.sum_keys_lokal
      , rows_last_analyzed = p_steuerung.rows_last_analyzed
      , status = p_steuerung.status
    where steuerung_id = p_steuerung.steuerung_id;

    commit;
  end prc_update_steuerung;

  function fun_modul_aufruf (p_verarbeitung in out nocopy t_verarbeitung%rowtype, p_steuerung in out nocopy t_steuerung%rowtype)
    return boolean is
    l_procname   varchar2 (60) := lower ($$plsql_unit) || '.fun_modul_aufruf';
    l_return     boolean := true;
  begin
    pck_all_log.prc_begin_module (p_name => l_procname);
    pck_all_log.prc_begin_action (p_name => 'AUFRUF MODUL', p_beschreibung => 'Abarbeiten eines Modules. Modul ' || p_steuerung.table_name || '.');

    case lower (p_steuerung.kommand)
    /*{pck_load__fun_modul_aufruf}*/
      when lower (pck_def_enviorement_variables.c_adresse) then
        l_return := pck_tab_adresse.fun_run (p_verarbeitung => p_verarbeitung, p_steuerung => p_steuerung);
      when lower (pck_def_enviorement_variables.c_code) then
        l_return := pck_tab_code.fun_run (p_verarbeitung => p_verarbeitung, p_steuerung => p_steuerung);
      else
        pck_all_log.prc_error (p_meldung => p_steuerung.table_name || ' ist nicht implementiert.', p_sqlerrm => p_steuerung.table_name || ' ist nicht implementiert.');
        l_return := false;
    end case;

    if l_return then
      pck_all_log.prc_end_action (pck_all_log.c_status_ok);
      pck_all_log.prc_end_module (pck_all_log.c_status_ok);
    else
      pck_all_log.prc_end_action (pck_all_log.c_status_error);
      pck_all_log.prc_end_module (pck_all_log.c_status_error);
    end if;

    return l_return;
  end fun_modul_aufruf;
end pck_load;
/