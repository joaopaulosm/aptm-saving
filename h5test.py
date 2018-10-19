import h5py
import os
import sys
import time
import epics
import signal

# print('The FILENAME will be...')
# print(FILENAME)

# f = h5py.File(FILENAME,'w')
# f.attrs['file_name']        = FILENAME
# f.attrs['file_time']        = TIMESTAMP
# f.attrs['HDF5_Version']     = h5py.version.hdf5_version
# f.close()

# print('\n SUCCESS! \n')

# HDF5 file parameters
addr = os.getcwd() + '/'
#addr = '/media/sf_vboxshared/'
TIMESTAMP = time.strftime("%H:%M:%S")
TIMESTAMP1 = time.strftime("%Y-%m-%d-%H:%M:%S")
FILENAME = addr + 'aptm-exp' + TIMESTAMP1 + '.hdf5'

# EPICS environment configuration
os.environ['EPICS_CA_ADDR_LIST']='localhost'

# Global variables definitios
prefix = 'LOC:'
pvTriggered = False
pvTriggerName = prefix + 'AMC1:Profile-RB'

# PV Callback function
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
	jparc_trigger = epics.PV(pvTriggerName)
	jparc_trigger.add_callback(onChanges)

	# ESS APTM PVs creation
	get_amc1_fitAmp = epics.PV(prefix + 'AMC1:PeakAmplitudeR')
	get_amc1_fitMu = epics.PV(prefix + 'AMC1:PeakMuR')
	get_amc1_fitSigma = epics.PV(prefix + 'AMC1:PeakSigmaR')
	get_amc2_fitAmp = epics.PV(prefix + 'AMC1:PeakAmplitudeR')
	get_amc2_fitMu = epics.PV(prefix + 'AMC1:PeakMuR')
	get_amc2fitSigma = epics.PV(prefix + 'AMC1:PeakSigmaR')

	#J-PARC PVs creation


	# HDF5 file creation
	f=h5py.File(FILENAME,'w')
	f.attrs['file_name']        = FILENAME
	f.attrs['file_time']        = TIMESTAMP
	f.attrs['HDF5_Version']     = h5py.version.hdf5_version

	while True:
		
		if (pvTriggered == True):
			pvTriggered = False

			# Get PV values
			print('Reading PV values!')
			amc1_fitAmp = get_amc1_fitAmp.get(timeout=10)
			amc1_fitMu = get_amc1_fitMu.get(timeout=10)
			amc1_fitSigma = get_amc1_fitSigma.get(timeout=10)
			amc2_fitAmp = get_amc2_fitAmp.get(timeout=10)
			amc2_fitMu = get_amc2_fitMu.get(timeout=10)
			amc2_fitSigma = get_amc2fitSigma.get(timeout=10)

			print('Writing to HDF5!')

			my_grp=f.create_group(str(trgCounter))

			my_grp.create_dataset('dataset_amc1_fitAmp', data=amc1_fitAmp)
			my_grp.create_dataset('dataset_amc1_fitMu', data=amc1_fitMu)
			my_grp.create_dataset('dataset_amc1_fitSigma', data=amc1_fitSigma)
			my_grp.create_dataset('dataset_amc2_fitAmp', data=amc2_fitAmp)
			my_grp.create_dataset('dataset_amc2_fitMu', data=amc2_fitMu)
			my_grp.create_dataset('dataset_amc2_fitSigma', data=amc2_fitSigma)

			trgCounter = trgCounter + 1



		
		time.sleep(0.25)


if __name__ == '__main__':
    main()
