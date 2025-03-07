#!/bin/tclsh
#

load tclrega.so
load tclrpc.so


proc get_homematic_alarms { } {
  array set result [rega_script {

object oTmpArray = dom.GetObject(ID_SYSTEM_VARIABLES);
string sTmp;
string slist ="";
foreach(sTmp, oTmpArray.EnumIDs()) 
{
  object oTmp = dom.GetObject(sTmp);
  if ( (oTmp.ValueSubType() == istAlarm) && (oTmp.AlState() == asOncoming) )
  {
    string sTriggerDesc = "keine Beschreibung";
    string sLastTriggerOut= "unbekannt";   
    object oLastTriggerDP = dom.GetObject( oTmp.LastTriggerID() );
    if (oLastTriggerDP) 
    { 
      string sLastTriggerChannel = dom.GetObject(oLastTriggerDP.Channel()); 
      string sLastTriggerChHssType = dom.GetObject(sLastTriggerChannel).HssType();
      object oLastTriggerDevice = dom.GetObject(sLastTriggerChannel.Device());
      string sLastTriggerDeviceHssType = oLastTriggerDevice.HssType();
      string sLastTriggerDeviceSerial = oLastTriggerDevice.Address(); 
      ! sLastTriggerOut = sLastTriggerChannel.Name() #" ( Serial: "#sLastTriggerDeviceSerial #" Typ: "  #sLastTriggerDeviceHssType #" )" ;
      sLastTriggerOut = sLastTriggerChannel.Name();
    }
    string sTriggerDesc = oTmp.DPInfo();
    
    
    ! oTmp.Name()                                         Wasseralarm
    ! oTmp.AlCounter()                                    # Auslöungen
    ! oTmp.ValueName()                                    ausgelöst, nicht ausgelöst
    ! oTmp.Timestamp().ToString("%d.%m.%y %H:%M Uhr")     letzte Auslösung
    ! sLastTriggerOut                                     Wassermelder Aquarium (HmIP-SWD 001898A9A36CF2:1) 
    ! sTriggerDesc                                        DPInfo()

    WriteLine("ALARM_MSG;" # oTmp.Name() # ";" # sLastTriggerOut # ";" # oTmp.ValueName() # ";" # oTmp.Timestamp().ToString("%Y-%m-%d %H:%M:%S")  )

  }
}

  }]
  return $result(STDOUT)
}

puts "<<<homematic_alarms:sep(59)>>>"
puts [string trim [get_homematic_alarms]]


