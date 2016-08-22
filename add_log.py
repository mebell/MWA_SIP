import glob
import os
import pyfits
import sys

# This code adds the raijin log files into the fits headers. 

results_dir = '/short/ek6/meb562/SIP_results/MWA_SIP_out/'
log_location = '/home/562/meb562/MWA_SIP/error_logs/'

for image in glob.glob(results_dir+'/*_I.fits'):
           print '_____________________________'
           print image
           obs_id = image.split('/')[6] 
           obs_id = obs_id[0:10]
           hdulist = pyfits.open(image, mode='update')
           head = hdulist[0].header
           if len(head) <= 200: # If the header is less than 200 then it hasn't had the history added. Then add it !
              print 'Adding header'
              logs = [obs_id+'.download.output', obs_id+'.download.error', obs_id+'.proc.output',obs_id+'.proc.error' ]
              for f in logs:
                log = log_location+f
                if os.path.isfile(log): 
		   with open(log) as addit:
			print f
			head['HISTORY'] = f
			hdulist.flush()
			for line in addit:
			    if (line[0:6] == "Author"):
			       pass;
                            elif (line[0:7] == "Written"):
                               pass;
			    else:
			       line = line.split('\n')[0]
			       head['HISTORY'] = line
	                hdulist.flush()
                else: 
                   pass;
              hdulist.close() 
           else: 
                print 'Header added - skipping'
