create or replace package pck_load is
  ---------------------------------  Header  ----------------------------
  -- Name         :  pck_load
  -- Projekt      :  BFI Release 3
  -- Beschreibung :  Aufbereitung fuer ODS_BFI
  --
  -- Autor        :  MMe
  -- Erstelldatum :  23.05.2017
  -- Auftrags-Nr. :  ??-?????
  --
  -- Skript-Name  :  $Id: pck_load.pks 8964 2017-06-01 08:38:23Z U10938 $
  -- Revision
  -- Nr.          :  $Revision: 8964 $
  -- User         :  $Author: U10938 $
  -- Datum        :  $Date: 2017-06-01 10:38:23 +0200 (Do, 01 Jun 2017) $
  -- HeadURL      :  $HeadURL: http://10.10.10.66/svn/DWH_Repository/trunk/DWH_ALLGEMEIN/SYRIUS_R3_DWH/OdsBfiStaging/database/packages/pck_load.pks $
  --
  -- Aenderungsnachweis :
  -- Ver. Datum       AendererIn  Auftrags-Nr  Aenderung
  -- 001  23.05.2017  MMe         ??-?????     Erstellt.
  ---------------------------------  Header End  -------------------------

  c_svn_revision_header constant varchar2(255) := '$Revision: 9222 $';

  function fun_get_svn_revision return varchar2;

  function fun_run (p_mandant in varchar2, p_load_type in pck_def_enviorement_variables.t_load_type)
    return number;
end pck_load;
/