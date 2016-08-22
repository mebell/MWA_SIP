import os, sys
import re
import glob

####################################################

# Code to run Aegean on all of the Stokes I images. It will skip files that have already been done.  

id_file = []

for f in glob.glob('/short/ek6/meb562/SIP_results/MWA_SIP_out/mwats/*_W_bm_1.0_SC_I.fits'):
    f = f.split('mwats/')[1]
    f_check = f.replace('.fits', '_comp.fits')
    f = f.split('_')[0]
    file_path = '/short/ek6/meb562/SIP_results/MWA_SIP_out/mwats/'+f_check
    if os.path.exists(file_path):
       pass;
    else:
        id_file.append(f)

total = len(id_file)
print total
n = 0
e = 100
for l in range(25):
    print '______________'
    print n, e
    ids = id_file[n:e]
    print ids
    error_log  = str(l)+'.error'
    output_log = str(l)+'.output'
    os.system('cp template_jobfile job_file.go') # Copy the template jobfile 
    for line in ids:
	    name = line.split('/')[-1]         # Define the output and error log names
	    name = re.split("[\r\n]+",name)[0] # Get rid of the return carriage
	    print name
            job_file = open('job_file.go', 'a')
            job_file.write('python /short/ek6/MWA_Code/Aegean/BANE.py '+name+'_W_bm_1.0_SC_I.fits')
            job_file.write('\n')
            job_file.write('python /short/ek6/MWA_Code/Aegean/aegean.py --island --maxsummits=5 --autoload '+name+'_W_bm_1.0_SC_I.fits --table '+name+'_W_bm_1.0_SC_I.fits')
            job_file.write('\n')
            job_file.close()   
    n = n+100
    e = e+100
    os.system('qsub -e '+error_log+' -o '+output_log+' job_file.go')
    
    


