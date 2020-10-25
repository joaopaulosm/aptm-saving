import h5py
import os
import sys
import time
import epics
import signal

#####################################################
# Runtime definition
# _DEBUG == ESS or JPARC
#####################################################
_DEBUG = False
_USE_JPARC = True

# Destination folder
addr = os.getcwd() + '/'
#addr = '/media/sf_vboxshared/'

if (_DEBUG == True):
	addr = os.getcwd() + '/'
	#addr = '/media/sf_vboxshared/'
#else:
	#addr = path/to/ext/drive

# Timestamping configs
TIMESTAMP = time.strftime("%H:%M:%S")
TIMESTAMP1 = time.strftime("%Y-%m-%d-%H:%M:%S")
FILENAME = addr + 'aptm-exp' + TIMESTAMP1 + '.hdf5'

# EPICS environment configuration
if (_DEBUG == True):
	os.environ['EPICS_CA_ADDR_LIST']='localhost'
else:
	os.environ['EPICS_CA_ADDR_LIST']='10.41.16.16 10.41.17.16 10.41.18.16 10.41.16.17 10.41.17.17 10.41.18.17 10.41.19.17 10.41.70.1'

# Global variables definitios
if (_DEBUG == True):
	prefix = 'LOC:'
else:
	prefix = 'APTM1:'

pvTriggered = False
pvTriggerName = prefix + 'AMC1:Profile-RB'

# PV Callback function - just modify pvTriggered variable when it changes
def onChanges(pvname=None, value=None, char_value=None, **kw):
	global pvTriggered
	pvTriggered = True
	
# Main function
def main():
	global pvTriggered
	pvTriggered = False

	# Trigger counter
	trgCounter = 0

	# PV used as a trigger for data collection
	acq_trigger = epics.PV(pvTriggerName)
	acq_trigger.add_callback(onChanges)

	# ESS APTM PVs creation ######################################################################################
	ess_pv_list = []
	amc_list = ['AMC1:', 'AMC2:', 'AMC3:']
	amc_grid = ['AMC1:', 'AMC2:']
	ai_list  = ['AI1:','AI2:','AI3:','AI4:','AI5:','AI6:','AI7:','AI8:']
	ain_list = ['1:','2:','3:','4:','5:','6:','7:','8:']
	
	# Array Data PVs
	for amc_name in amc_list:
		for ai_n in ai_list:
			ess_pv_list.append(prefix + amc_name + ai_n + 'ArrayData')

	# Profile Data
	for amc_name in amc_grid:
		ess_pv_list.append(prefix + amc_name + 'Profile-RB')
		ess_pv_list.append(prefix + amc_name + 'ProfileFit-RB')

	# Fitting parameters
	for amc_name in amc_grid:
		ess_pv_list.append(prefix + amc_name + 'BackgroundR')
		ess_pv_list.append(prefix + amc_name + 'PeakAmplitudeR')
		ess_pv_list.append(prefix + amc_name + 'PeakMuR')
		ess_pv_list.append(prefix + amc_name + 'PeakAmplitudeR')
		ess_pv_list.append(prefix + amc_name + 'PeakSigmaR')
		ess_pv_list.append(prefix + amc_name + 'FNormR')
		ess_pv_list.append(prefix + amc_name + 'FitStatusR')

	# AMC Parameters
	for amc_name in amc_list:
		ess_pv_list.append(prefix + amc_name + 'TickValueR')
		ess_pv_list.append(prefix + amc_name + 'FSampR')
		ess_pv_list.append(prefix + amc_name + 'ArrayCounter_RBV')
		ess_pv_list.append(prefix + amc_name + 'ActualSamplesR')
		ess_pv_list.append(prefix + amc_name + 'TickValueR')
		for ai_n in ain_list:
			ess_pv_list.append(prefix + amc_name + ai_n + 'RangeR')

	# Motion PVs
	ess_pv_list.append('jparc:001-Err')
	ess_pv_list.append('jparc:001-ErrId')
	ess_pv_list.append('jparc:002-Err')
	ess_pv_list.append('jparc:002-ErrId')
	ess_pv_list.append('jparc:MCU-ErrMsg')
	ess_pv_list.append('jparc:ec0-s3-EL3314-AI1') 
	ess_pv_list.append('jparc:ec0-s3-EL3314-AI2') 
	ess_pv_list.append('jparc:MCU-ErrId')
	ess_pv_list.append('jparc:001.VAL')	
	ess_pv_list.append('jparc:001.RBV')  	
	ess_pv_list.append('jparc:002.VAL')	
	ess_pv_list.append('jparc:002.RBV')   

	# J-PARC PVs creation
	ess_pv_list.append('BT_SW:SCTD:VAL_ATT')
	ess_pv_list.append('BT_SW:PMEXT01H:VAL')
	ess_pv_list.append('BT_SW:PMEXT01V:VAL')
	ess_pv_list.append('BT_SW:PMEXT02H:VAL')
	ess_pv_list.append('BT_SW:PMEXT02V:VAL')
	ess_pv_list.append('BT_SW:PMFIX0DH:VAL')
	ess_pv_list.append('BT_SW:PMFIX0DV:VAL')
	ess_pv_list.append('bt3n:DSO6014L0:VPPC_H1:VAL')
	ess_pv_list.append('bt3n:DSO6014L1:VPPC_H1:VAL')
	ess_pv_list.append('bt3n:DSO6014L2:VPPC_H1:VAL')
	ess_pv_list.append('bt3n:DSO6014L3:VPPC_H1:VAL')
	ess_pv_list.append('bt3n:DSO6014L0:VPPC_H2:VAL')
	ess_pv_list.append('bt3n:DSO6014L1:VPPC_H2:VAL')
	ess_pv_list.append('bt3n:DSO6014L2:VPPC_H2:VAL')
	ess_pv_list.append('bt3n:DSO6014L3:VPPC_H2:VAL')
	ess_pv_list.append('bt3n:DSO6014L0:VPPC_V1:VAL')
	ess_pv_list.append('bt3n:DSO6014L1:VPPC_V1:VAL')
	ess_pv_list.append('bt3n:DSO6014L2:VPPC_V1:VAL')
	ess_pv_list.append('bt3n:DSO6014L3:VPPC_V1:VAL')
	ess_pv_list.append('bt3n:DSO6014L0:VPPC_V2:VAL')
	ess_pv_list.append('bt3n:DSO6014L1:VPPC_V2:VAL')
	ess_pv_list.append('bt3n:DSO6014L2:VPPC_V2:VAL')
	ess_pv_list.append('bt3n:DSO6014L3:VPPC_V2:VAL')

	max_str = 0
	for pv in ess_pv_list:
		if (len(pv) > max_str):
			max_str = len(pv)

	# Run through all PVs and try to connect ###################################### 
	for pv in ess_pv_list:
		time.sleep(0.1)
		pvobj = epics.PV(pv, verbose=False, connection_timeout = 5.0)
		msg_str = 'Trying to connect to ' + pv
		for i in range(0, (max_str-len(pv)+4)):
			msg_str += '.'
		result_str = str(pvobj.wait_for_connection(timeout=5.0))
		print(msg_str + result_str)


if __name__ == '__main__':
	main()



