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
_DEBUG = True
_USE_JPARC = False

# Destination folder
if (_DEBUG == True):
	# addr = os.getcwd() + '/'
	addr = '/home/joaopaulomartins/hdftest'
	#addr = '/media/sf_vboxshared/'
else:
	#addr = path/to/ext/drive
	pass

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

# Creating HDF5 file
f=h5py.File(FILENAME,'w')
f.attrs['file_name']        = FILENAME
f.attrs['file_time']        = TIMESTAMP
f.attrs['HDF5_Version']     = h5py.version.hdf5_version

def signal_handler(sig, frame):
        global f
        print('Closing the HDF5 file ...')
        f.close()
        sys.exit(0)

# PV Callback function - just modify pvTriggered variable when it changes
def onChanges(pvname=None, value=None, char_value=None, **kw):
    global pvTriggered
    pvTriggered = True
    
# Main function
def main():
	global pvTriggered
	global f
	pvTriggered = False

	signal.signal(signal.SIGINT, signal_handler)

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
	# for amc_name in amc_list:
	# 	for ai_n in ai_list:
	# 		ess_pv_list.append(prefix + amc_name + ai_n + 'ArrayData')

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
	# for amc_name in amc_list:
	# 	ess_pv_list.append(prefix + amc_name + 'TickValueR')
	# 	ess_pv_list.append(prefix + amc_name + 'FSampR')
	# 	ess_pv_list.append(prefix + amc_name + 'ArrayCounter_RBV')
	# 	ess_pv_list.append(prefix + amc_name + 'ActualSamplesR')
	# 	ess_pv_list.append(prefix + amc_name + 'TickValueR')
	# 	for ai_n in ain_list:
	# 		ess_pv_list.append(prefix + amc_name + ai_n + 'RangeR')

	# Motor Positions

	# J-PARC PVs creation
	# ess_pv_list.append('BT_SW:SCTD:VAL_ATT')
	# ess_pv_list.append('BT_SW:PMEXT01H:VAL')
	# ess_pv_list.append('BT_SW:PMEXT01V:VAL')
	# ess_pv_list.append('BT_SW:PMEXT02H:VAL')
	# ess_pv_list.append('BT_SW:PMEXT02V:VAL')
	# ess_pv_list.append('BT_SW:PMFIX0DH:VAL')
	# ess_pv_list.append('BT_SW:PMFIX0DV:VAL')
	# ess_pv_list.append('bt3n:DSO6014L0:VPPC_H1:VAL')
	# ess_pv_list.append('bt3n:DSO6014L1:VPPC_H1:VAL')
	# ess_pv_list.append('bt3n:DSO6014L2:VPPC_H1:VAL')
	# ess_pv_list.append('bt3n:DSO6014L3:VPPC_H1:VAL')
	# ess_pv_list.append('bt3n:DSO6014L0:VPPC_H2:VAL')
	# ess_pv_list.append('bt3n:DSO6014L1:VPPC_H2:VAL')
	# ess_pv_list.append('bt3n:DSO6014L2:VPPC_H2:VAL')
	# ess_pv_list.append('bt3n:DSO6014L3:VPPC_H2:VAL')
	# ess_pv_list.append('bt3n:DSO6014L0:VPPC_V1:VAL')
	# ess_pv_list.append('bt3n:DSO6014L1:VPPC_V1:VAL')
	# ess_pv_list.append('bt3n:DSO6014L2:VPPC_V1:VAL')
	# ess_pv_list.append('bt3n:DSO6014L3:VPPC_V1:VAL')
	# ess_pv_list.append('bt3n:DSO6014L0:VPPC_V2:VAL')
	# ess_pv_list.append('bt3n:DSO6014L1:VPPC_V2:VAL')
	# ess_pv_list.append('bt3n:DSO6014L2:VPPC_V2:VAL')
	# ess_pv_list.append('bt3n:DSO6014L3:VPPC_V2:VAL')

	# HDF5 file creation
	# f=h5py.File(FILENAME,'w')
	# f.attrs['file_name']        = FILENAME
	# f.attrs['file_time']        = TIMESTAMP
	# f.attrs['HDF5_Version']     = h5py.version.hdf5_version

	# Channel access connections
	# based on http://cars9.uchicago.edu/software/python/pyepics3/advanced.html

	# Create objects
	pvdata = {} # dictionary to hold chid 
	pvdatadict = {} # dictionary to hold collected data
	
	for name in ess_pv_list:
		chid = epics.ca.create_channel(name, connect=False, auto_cb=False) # note 1
		pvdata[name] = (chid, None)

	# Connect to PVs
	for name, data in pvdata.items():
		epics.ca.connect_channel(data[0])
	epics.ca.poll()

	while True:
		
		# Check if trigger occured
		if (pvTriggered == True):
			
			# reset the trigger event to catch the next on
			pvTriggered = False

			# Get PV values
			for name, data in pvdata.items():
				epics.ca.get(data[0], wait=False)  # note 2

			epics.ca.poll()
			
			for name, data in pvdata.items():
				val = epics.ca.get_complete(data[0])
				pvdatadict[name] = val

			print(time.strftime("[%Y/%m/%d %H:%M:%S]") + ' .... Saving collected data | ' + str(trgCounter))
			f=h5py.File(FILENAME,'a')
			my_grp=f.create_group(str(trgCounter))

			for name, data in pvdata.items():
				my_grp.create_dataset(name, data=pvdatadict[name])
				print(name + ' = ' + str(pvdatadict[name]))

			trgCounter = trgCounter + 1
			f.close()

		
		time.sleep(0.25)


if __name__ == '__main__':
    main()
