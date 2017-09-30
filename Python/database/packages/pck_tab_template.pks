create or replace package pck_tab_{table_name} is
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
  -- Skript-Name  :  $Id: pck_tab_template.pks 8964 2017-06-01 08:38:23Z U10938 $
  -- Revision
  -- Nr.          :  $Revision: 8964 $
  -- User         :  $Author: U10938 $
  -- Datum        :  $Date: 2017-06-01 10:38:23 +0200 (Do, 01 Jun 2017) $
  -- HeadURL      :  $HeadURL: http://10.10.10.66/svn/DWH_Repository/trunk/DWH_ALLGEMEIN/SYRIUS_R3_DWH/OdsBfiStaging/database/packages/pck_tab_template.pks $
  --
  -- Aenderungsnachweis :
  -- Ver. Datum       AendererIn  Auftrags-Nr  Aenderung
  -- 001  24.05.2017  MMe         ??-?????     Erstellt.
  ---------------------------------  Header End  -------------------------

  c_svn_revision_header constant varchar2(255) := '$Revision: 9222 $';

  function fun_get_svn_revision return varchar2;


  function fun_run (p_verarbeitung in out nocopy t_verarbeitung%rowtype, p_steuerung in out nocopy t_steuerung%rowtype)
    return boolean;
end pck_tab_{table_name};
/