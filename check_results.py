import os
import re
import glob

"Script to check the correct number of images have been made by the SIP"


results_dir = '/short/ek6/meb562/SIP_results/MWA_SIP_out/'

id_file = open('obs_id_list.txt', 'r')

completed = 0
count = 0

bad_obs = []
bad_obs_files = []

for obs_id in id_file:
    obs_id = re.split("[\r\n]+",obs_id)[0] 
    os.chdir(results_dir)
    n_files = len(glob.glob('*'+obs_id+'*'))
    if n_files == 15: 
       completed +=1
    else:
       bad_obs.append(obs_id)
       bad_obs_files.append(n_files)
    count +=1

print '______________________________'
print 'Completed files: '+str(completed)+'/'+str(count)
print '______________________________'
if completed == count:
   print "All obs ids succesfully reduced"
else:
   print 'Failed obs ids:'
   for i in range(len(bad_obs)):
       print str(bad_obs[i])+' '+str(bad_obs_files[i])+'/15'

print "Files to re-reduce:"
for i in range(len(bad_obs)):
       print str(bad_obs[i])
