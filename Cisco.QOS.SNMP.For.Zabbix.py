#!/usr/bin/env python

#User provides input data invoking script

import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('hostname')
parser.add_argument('-c', help='community string')

args = parser.parse_args()

hostname=(args.hostname)
####print hostname

community=(args.c)
####print community


#SNMP List of QoS enabled interfaces "cbQosIfIndex" MIB
### From that point Easy SNMP PIP package is used instead of PySNMP due to very simple interface ###

from easysnmp import Session

# Create an SNMP session to be used for all our requests
session = Session(hostname=hostname, community=community, version=2)


####Code Start####

#SNMP List of interfaces "IfDescr" MIB

snmp_session_querry = session.get('IF-MIB::ifNumber.0')
snmp_session_output = '{oid}.{oid_index} {snmp_type} = {value}'.format(oid=snmp_session_querry.oid, oid_index=snmp_session_querry.oid_index, snmp_type=snmp_session_querry.snmp_type, value=snmp_session_querry.value)
interface_counter_int = int(snmp_session_output.split()[3])
del snmp_session_querry, snmp_session_output

snmp_session_querry = session.bulkwalk('IF-MIB::ifDescr')
x=0
interface_list=[0]
for item in snmp_session_querry:
        interface_list[x] =  '{oid}.{oid_index} = {value}'.format(
        oid=item.oid,
        oid_index=item.oid_index,
        value=item.value
        )
        ####print interface_list[x]
	interface_list[x] = interface_list[x].rsplit('.')[1]
	interface_list.append(0)
        ####print interface_list[x]
	x +=1
del x					

#SNMP List of QoS enabled interfaces "cbQosIfIndex" MIB

qos_interface_list = session.bulkwalk('CISCO-CLASS-BASED-QOS-MIB::cbQosIfIndex')
x=0
qos_interface_list_final=[0]
for item in qos_interface_list:
	qos_interface_list_final[x] =  '{oid}.{oid_index} {snmp_type} = {value}'.format(
        oid=item.oid,
        oid_index=item.oid_index,
        snmp_type=item.snmp_type,
        value=item.value
	)
	####print qos_interface_list_final[x]
	qos_interface_list_final.append(0)
	x +=1


#SNMP List of policy map direction

qos_policy_direction = session.walk('CISCO-CLASS-BASED-QOS-MIB::cbQosPolicyDirection')
x=0
qos_policy_direction_final=[0]
for item in qos_policy_direction:
        qos_policy_direction_final[x] =  '{oid}.{oid_index} {snmp_type} = {value}'.format(
        oid=item.oid,
        oid_index=item.oid_index,
        snmp_type=item.snmp_type,
        value=item.value
        )
        ####print qos_policy_direction_final[x]
	qos_policy_direction_final.append(0)
        x +=1



#SNMP List of class-names

qos_class_name = session.bulkwalk('CISCO-CLASS-BASED-QOS-MIB::cbQosCMName')
x=0
qos_class_name_final=[0]
for item in qos_class_name:
        qos_class_name_final[x] =  '{oid}.{oid_index} {snmp_type} = {value}'.format(
        oid=item.oid,
        oid_index=item.oid_index,
        snmp_type=item.snmp_type,
        value=item.value
        )
        ####print qos_class_name_final[x]
        qos_class_name_final.append(0)
	x +=1


#Get lenght of lists required for further parsing

lenght_int_list=len(interface_list)-1
####print lenght_int_list
lenght_qos_int_list=len(qos_interface_list_final)-1
####print lenght_qos_int_list
lenght_qos_policy_direction=len(qos_policy_direction_final)-1
####print lenght_qos_policy_direction
z=0
#Correlate interface list with QoSIfIndex
interface_list_output=[0]
for n1 in range(0,lenght_int_list):
	temp1_int=interface_list[n1].split()
	temp2_int=len(temp1_int)
	for n2 in range(0,lenght_qos_int_list):
		temp1_qos=qos_interface_list_final[n2].split()
		temp2_qos=len(temp1_qos)
		#if interface_list[n1][:1] == qos_interface_list_final[n2][-1:]:
		if temp1_int[0] == temp1_qos[temp2_qos-1]:
			interface_list_output[z]='ID1: '+temp1_int[2]+' '+'ID2: '+temp1_qos[0][13:]
			####print interface_list_output[z]
			z=z+1
			interface_list_output.append(0)
		
del temp1_int, temp2_int, temp1_qos, temp2_qos, n1, n2

#Correlate interface list  + QoSIfIndex + direction
interface_list_output_len=len(interface_list_output)-1
for n1 in range(0,interface_list_output_len):
	temp1_int=interface_list_output[n1].split()
	temp2_int=len(temp1_int)
	for n2 in range (0,lenght_qos_policy_direction):
		temp1_direction=qos_policy_direction_final[n2].split()
		temp2_direction=len(temp1_direction)
		if temp1_int[3] == temp1_direction[0][21:]:
			if qos_policy_direction_final[n2][-1:] == '1':
				interface_list_output[n1]=interface_list_output[n1]+' ID3: Input'
			elif qos_policy_direction_final[n2][-1:] == '2':
				interface_list_output[n1]=interface_list_output[n1]+' ID3: Output'
	####print interface_list_output[n1]

del n1, n2, temp1_int, temp2_int, temp1_direction, temp2_direction

#Populate all QoSConfigIndexes to list variable for each pairs of interface/direction
interface_list_output_len=len(interface_list_output)-1
x=0
qos_config_index_final=[0]
for n1 in range (0,interface_list_output_len):
	int_index=interface_list_output[n1].split()
	int_index=int_index[3]
	qos_config_index = session.bulkwalk('CISCO-CLASS-BASED-QOS-MIB::cbQosConfigIndex.'+int_index)
	for item in qos_config_index:
        	qos_config_index_final[x] =  '{oid}.{oid_index} {snmp_type} = {value}'.format(
		oid=item.oid,
        	oid_index=item.oid_index,
        	snmp_type=item.snmp_type,
        	value=item.value
       		)
        	####print qos_config_index_final[x]
		qos_config_index_final.append(0)
		x +=1
del n1, int_index, x

#Correlate QoSConfigIndexes and Class names
qos_config_index_final_len=len(qos_config_index_final)-1
qos_class_name_final_len=len(qos_class_name_final)-1
for n1 in range (0,qos_config_index_final_len):
	temp_qos_config_index=qos_config_index_final[n1].split()
	for n2 in range (0,qos_class_name_final_len):
		temp_class_name=qos_class_name_final[n2].split()
#		print temp_qos_config_index[3]
#		print temp_class_name[0][12:]
		if temp_qos_config_index[3] == temp_class_name[0][12:]:
			qos_config_index_final[n1]=qos_config_index_final[n1]+' '+temp_class_name[3]
			break
####	print qos_config_index_final[n1]
del n1, n2, temp_qos_config_index, temp_class_name

for n1 in range (0,qos_config_index_final_len):
	qos_config_index_final_id=qos_config_index_final[n1].split()
	qos_config_index_final_id_len=len(qos_config_index_final_id)
	if qos_config_index_final_id_len == 4:
		qos_config_index_final[n1]='EMPTY.TAG'
####	print qos_config_index_final[n1]
	
qos_config_index_final2=[0]
n2=0
for n1 in range (0,qos_config_index_final_len):
	temp_qos_config_index=qos_config_index_final[n1].split()
	temp_qos_config_index_len=len(temp_qos_config_index)
	if temp_qos_config_index_len == 5:
		qos_config_index_final2[n2] = qos_config_index_final[n1]
		####print qos_config_index_final2[n2]
		qos_config_index_final2.append(0)
		n2 +=1
del n1, n2, temp_qos_config_index, temp_qos_config_index_len

qos_config_index_final2_len=len(qos_config_index_final2)-1
for n1 in range (0,qos_config_index_final2_len):
	for n2 in range (0,interface_list_output_len):
		temp_interface_list_output=interface_list_output[n2].split()
		if temp_interface_list_output[3] == qos_config_index_final2[n1].rsplit('.')[1]:
			qos_config_index_final2[n1]=interface_list_output[n2]+' ID4: '+qos_config_index_final2[n1].split()[4]+' ID5: '+qos_config_index_final2[n1].split()[0].rsplit('.')[2]
			break
del n1, n2,

#Feed QoSParentObjectIndex
qos_parent_list=[0]
n=0
temp_snmp = session.bulkwalk('CISCO-CLASS-BASED-QOS-MIB::cbQosParentObjectsIndex')
for item in temp_snmp:
	qos_parent_list[n] = '{oid}.{oid_index} {snmp_type} = {value}'.format(
        oid=item.oid,
        oid_index=item.oid_index,
        snmp_type=item.snmp_type,
        value=item.value
    	)
####	print qos_parent_list[n]
	qos_parent_list.append(0)
	n +=1	
#Assing parent ServicePolicy or Interface name for each object
for n1 in range(0,len(qos_config_index_final2)-1):
	for n2 in range (0,len(qos_parent_list)-1):
		if (qos_config_index_final2[n1].split()[3] == qos_parent_list[n2].rsplit('.')[1]) and (qos_config_index_final2[n1].split()[9] == qos_parent_list[n2].rsplit('.')[2].split()[0]):
			if (qos_parent_list[n2].rsplit('.')[2].split()[3] != qos_config_index_final2[n1].split()[3]):
				snmp_session_querry = session.get('CISCO-CLASS-BASED-QOS-MIB::cbQosConfigIndex.'+qos_config_index_final2[n1].split()[3]+'.'+qos_parent_list[n2].split()[3])
				snmp_session_output = '{oid}.{oid_index} {snmp_type} = {value}'.format(oid=snmp_session_querry.oid, oid_index=snmp_session_querry.oid_index, snmp_type=snmp_session_querry.snmp_type, value=snmp_session_querry.value)
				snmp_session_querry1 = session.get('CISCO-CLASS-BASED-QOS-MIB::cbQosPolicyMapName.''{value}'.format(value=snmp_session_querry.value))
				snmp_session_output1 = '{oid}.{oid_index} {snmp_type} = {value}'.format(oid=snmp_session_querry1.oid, oid_index=snmp_session_querry1.oid_index, snmp_type=snmp_session_querry1.snmp_type, value=snmp_session_querry1.value)
				snmp_session_output1 = snmp_session_output1.split()[3]
####				print snmp_session_output1
				qos_config_index_final2[n1]=qos_config_index_final2[n1]+' ID6: '+'Nested.by.ServicePolicy ' +'ID7: '+snmp_session_output1
									
			else:
				for n3 in range (0,len(interface_list_output)):
					if qos_parent_list[n2].split()[3] == interface_list_output[n3].split()[3]:
						qos_config_index_final2[n1]=qos_config_index_final2[n1]+' ID6: '+'Nested.by.Interface '+'ID7: '+interface_list_output[n3].split()[1]
						break
	####print qos_config_index_final2[n1]
del n1

#Prepare Final JSON format for Zabbix
		
for n1 in range(0,len(qos_config_index_final2)-1):
	qos_config_index_final2[n1]='{'+'"{#'+qos_config_index_final2[n1].split()[0][0:3]+'}":'+'"'+qos_config_index_final2[n1].split()[1]+'",'+'"{#'+qos_config_index_final2[n1].split()[2][0:3]+'}":'+'"'+qos_config_index_final2[n1].split()[3]+'",'+'"{#'+qos_config_index_final2[n1].split()[4][0:3]+'}":'+'"'+qos_config_index_final2[n1].split()[5]+'",'+'"{#'+qos_config_index_final2[n1].split()[6][0:3]+'}":'+'"'+qos_config_index_final2[n1].split()[7]+'",'+'"{#'+qos_config_index_final2[n1].split()[8][0:3]+'}":'+'"'+qos_config_index_final2[n1].split()[9]+'",'+'"{#'+qos_config_index_final2[n1].split()[10][0:3]+'}":'+'"'+qos_config_index_final2[n1].split()[11]+'",'+'"{#'+qos_config_index_final2[n1].split()[12][0:3]+'}":'+'"'+qos_config_index_final2[n1].split()[13]+'"},'
del n1

qos_config_index_final2.insert(0,'{"data":[')
qos_config_index_final2[len(qos_config_index_final2)-1]=']}'

temp1=len(qos_config_index_final2[len(qos_config_index_final2)-2])
qos_config_index_final2[len(qos_config_index_final2)-2]=qos_config_index_final2[len(qos_config_index_final2)-2][0:temp1-1]

for n1 in range(0,len(qos_config_index_final2)):
	print qos_config_index_final2[n1]
del n1
