# Cisco QOS SNMP For Zabbix
CISCO-CLASS-BASED-QOS on Zabbix

Monitor CISCO-CLASS-BASED-QOS-MIB counters under Zabbix. Monitor class-names counters under Zabbix.

Version: 0.1

Abstract: Cisco CISCO-CLASS-BASED-QOS-MIB is one of the most complex and not clear Cisco SNMP MIBs. This python script as final output produces correlation between Intrface Name, Interface QoS ID, Class-name, QOS Index ID, parent object.

Script written in python 2.7, tested on Linux Centos7.

Script Installation:
 Install Net-SNMP libraries
 
 Unix# yum install net-snmp.x86_64
 
 Unix# yum install net-snmp-devel.x86_64
 
 Unix# yum install gcc.x86_64
 
 Install Python:
 
 Unix# yum install epel-release
 
 Unix# yum install python.x86_64
 
 Unix# yum install python-devel
 
 Unix# yum install python2-pip
 
 Install EasySNMP:
 
 pip install easysnmp
 
 Copy Cisco.QOS.SNMP.For.Zabbix.py to your Zabbix external script directory /usr/lib/zabbix/externalscripts/
 
 

Many thx and credits github.com/peshovec for initial concept. https://github.com/peshovec/zabbix-cisco-classname
I wrote new script under Python. Features which were missing in peshovec script were: duplicated class names, direction of atached policy map, nested Service Polices (very common in implementation).

