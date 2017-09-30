create or replace package pck_def_enviorement_variables is
  ---------------------  header  ----------------------------
  -- Name         :  pck_def_enviorement_variables
  -- Projekt      :  BFI Release 3
  -- Beschreibung :  Aufbereitung fuer ODS_BFI
  --                 Package fuer Parameter
  -- Autor        :  MMe
  -- Erstelldatum :  23.05.2017
  -- Auftrags-Nr. :  ??-?????
  --
  -- Skript-Name  :  $Id: pck_def_enviorement_variables.pks 8964 2017-06-01 08:38:23Z U10938 $
  -- Revision
  -- Nr.          :  $Revision: 8964 $
  -- User         :  $Author: U10938 $
  -- Datum        :  $Date: 2017-06-01 10:38:23 +0200 (Do, 01 Jun 2017) $
  -- HeadURL      :  $HeadURL: http://10.10.10.66/svn/DWH_Repository/trunk/DWH_ALLGEMEIN/SYRIUS_R3_DWH/OdsBfiStaging/database/packages/pck_def_enviorement_variables.pks $
  --
  -- Aenderungsnachweis :
  -- Ver. Datum       AendererIn  Auftrags-Nr  Aenderung
  -- 001  23.05.2017  MMe         ??-?????     Erstellt.
  ---------------------------------  Header End  -------------------------

  subtype t_load_type is t_verarbeitung.ladetyp%type;

  c_load_initial             constant t_load_type := 'INITIAL'; --- Alle Verarbeitungen und Tabellen werden INITIAL (FULL) geladen und der aktuelle SCN erstellt.
  c_load_pps                 constant t_load_type := 'PPS'; --- Es wird aus der Schema CHKXXX der SCN vom letzten ODS Load gelesen und mit diesem geladen (ODS_BFIXXX synchron mit ODSXXX).
  c_load_manuell             constant t_load_type := 'MANUELL'; --- Es wird ein neuer (aktueller) SCN generiert und normal geladen (systimestamp - 10 Sekunden).

  subtype t_table_load_type is t_steuerung.table_ladetyp%type;

  c_load_type_full           constant t_table_load_type := 'FULL'; --- Tabelle wird immer FULL geladen. Noetig fuer alle Tabelle ohne PKEY Column! 
  c_load_type_incr           constant t_table_load_type := 'INCR'; --- Tabelle wird wenn moeglich INCREMENTELL geladen. 

  subtype t_table_status is t_steuerung.status%type;

  c_status_ok                constant t_table_status := 'OK'; --- Tabellenstatus OK
  c_status_error             constant t_table_status := 'ERROR'; --- Tabellenstatus Error.

  subtype t_table_pruefen is t_steuerung.pruefen%type;

  c_pruefen_yes              constant t_table_pruefen := 'Y'; --- Tabelle durchlauft die Inventur.
  c_pruefen_no               constant t_table_pruefen := 'N'; --- Tabelle bekommt Dummy Inventur.

  subtype t_korrektur_ladedtyp is t_korrektur.korrektur_ladetyp%type;

  c_korrektur_ladetyp_full   constant t_korrektur_ladedtyp := 'FULL'; --- Korrektur Scipt wird nur im FULL LOAD Modus ausgefuehrt.
  c_korrektur_ladetyp_incr   constant t_korrektur_ladedtyp := 'INCR'; --- Korrektur Script wird immer ausgefuert.
  ----------------------------------------------------------------------------------------------------------------------------------------------
  
  --- Liste aller Tabellen und Packages fuer den LOAD
  
  /*{pck_def_enviorement_variables__table_package_list}*/
  
end pck_def_enviorement_variables;
/