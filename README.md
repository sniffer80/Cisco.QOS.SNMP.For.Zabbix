# Cisco QOS SNMP For Zabbix
CISCO-CLASS-BASED-QOS on Zabbix

Monitor CISCO-CLASS-BASED-QOS-MIB counters under Zabbix. Monitor class-names counters under Zabbix.

Version: 0.1

Abstract: Cisco CISCO-CLASS-BASED-QOS-MIB is one of the most complex and not clear Cisco SNMP MIBs. This python script as final output produces in JSON format correlation between Intrface Name, Interface QoS ID, Class-name, QOS Config Index ID, parent object. Output is takeen by Zabbix Template (discovery rule) as input to produce final counters as "items".

Script written in python 2.7, tested on Linux Centos7.

SNMP version testes "2c".


## Script Installation:

 ### Install Net-SNMP libraries:
 
  Unix# yum install net-snmp.x86_64
 
  Unix# yum install net-snmp-devel.x86_64
 
  Unix# yum install gcc.x86_64
 
 
 ### Install Python:
 
  Unix# yum install epel-release
 
  Unix# yum install python.x86_64
 
  Unix# yum install python-devel
 
  Unix# yum install python2-pip
 
 
### Install EasySNMP:
 
  pip install easysnmp
 

### Download and install CISCO-CLASS-BASED-QOS-MIB:
 
  Download ftp://ftp.cisco.com/pub/mibs/v2/CISCO-CLASS-BASED-QOS-MIB.my
  
  Put downloaded MIB file in SNMP-NET MIB direcotries, keep in mind to change extension from .my to .txt. You can check your NET-SNMP directories by executing "net-snmp-config --default-  mibdirs" command
  
 Check if MIB is installed properly by invoking any SNMP querry to object withing MIB. For example: "snmpbulkwalk -v 2c -c comm_str x.x.x.x cbQosConfigIndex"
 
  It may turns out that you also need to download parent MIB for proper working of CISCO-CLASS-BASED-QOS-MIB. Then repeat steps for rest of parent MIBs http://snmp.cloudapps.cisco.com/Support/SNMP/do/BrowseMIB.do?local=en&step=2&mibName=CISCO-CLASS-BASED-QOS-MIB
 
 
### Install scripts on Zabbix:

 Copy Cisco.QOS.SNMP.For.Zabbix.py to your Zabbix external script directory /usr/lib/zabbix/externalscripts/

 Import Cisco.QOS.SNMP.For.Zabbix.xml to Zabbix Templates Configuration/Templates
 
 Attach Template to Host and wait ~2min for results. You can build nice graphs based on produced items.

## Credits
Many thx and credits github.com/peshovec for initial concept. https://github.com/peshovec/zabbix-cisco-classname
I wrote new script under Python. Features which were missing in peshovec script were: duplicated class names, direction of flow for atached policy map, nested Service Polices (very common in implementation).

