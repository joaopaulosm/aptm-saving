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
else:
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
			ess_pv_list.append(prefix + amc_name + ai_n + 'RangeR'


	# Connect to ALL PVS and check if they respond

	for pv in ess_pv_list:
		pvobj = epics.PV(pv, verbose=True, connection_timeout = 1.0)
		if (pv.status == 1):
			print('PV ' + pv + ' OK!')
		else:
			print('PV ' + pv + ' NOT CONNECTED!')




if __name__ == '__main__':
    main()