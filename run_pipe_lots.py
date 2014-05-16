import os, sys
import re

################################################################################
# File to create and submit multiple job files for downloading and processing. #
################################################################################


def run_job(id, deps):
    print '#####################################################'
    ### Run the download job on the  "copy" que (see agruments in header of "template_download)
    os.system('cp template_download download.go') # Copy the template jobfile 
    job_file = open('download.go', 'a')
    print 'Writing appropriate download download file for observation ' 
    # Add the appropriate command. 
    job_file.write('python /home/562/meb562/SIP/get_data.py '+id)
    job_file.close()
    ####### Error Logs ########
    name = id.split('/')[-1]        # Define the output and error log names
    name = re.split("[\r\n]+",name)[0] # Get rid of the return carriage
    error_log = '/home/562/meb562/SIP/error_logs/'+name+'.download.error'
    output_log = '/home/562/meb562/SIP/error_logs/'+name+'.download.output'
    ######## Normal Que ########
    if len(deps)==0:       
       print 'Submitting download to qsub NORMAL'
       print 'Download command is = qsub -e '+error_log+' -o '+output_log+' download.go'
       download_command = 'qsub -e '+error_log+' -o '+output_log+' download.go'
       term_out=os.popen(download_command).read()
       term_out = re.split("[\r\n]+",term_out)[0] # Remove return carriage
       sub_jobs.append(term_out)
    ######### Dependency Que #########
    dep_string = ''
    if len(deps)>0:
       for k in range(len(deps)):
           dep_string = dep_string + deps[k]
           dep_string = dep_string + ':'     
       print 'Submitting download to qsub DEPENDENCY'
       download_command = 'qsub -W depend=afterok:'+dep_string+' -e '+error_log+' -o '+output_log+' download.go'
       print 'Download command is '+download_command
       term_out=os.popen(download_command).read()
       term_out = re.split("[\r\n]+",term_out)[0] # Remove return carriage
       sub_jobs.append(term_out)
    ### Run the processing on the "normal" que (see agruments in header of "template_jobfile)
    os.system('cp template_jobfile job_file.go') # Copy the template jobfile 
    job_file = open('job_file.go', 'a')
    print 'Will only exceute qsub job when download is complete' 
    # Add the appropriate command.  
    job_file.write('python /home/562/meb562/SIP/pre_proc_pipe.py '+id)
    job_file.close()
    # Submit the file to qsub.
    name = id.split('/')[-1]        # Define the output and error log names
    name = re.split("[\r\n]+",name)[0] # Get rid of the return carriage
    error_log = '/home/562/meb562/SIP/error_logs/'+name+'.proc.error'
    output_log = '/home/562/meb562/SIP/error_logs/'+name+'.proc.output'
    print 'Data reduction command is = qsub -W depend=afterok:'+term_out+' -e '+error_log+' -o '+output_log+' job_file.go'
    print 'Submitting jobfile'
    os.system('qsub -W depend=afterok:'+term_out+' -e '+error_log+' -o '+output_log+' job_file.go')
    print '#####################################################'
    return sub_jobs

# Work out which GPS ID / datafile we are going to work on 
id_file = open('obs_id_list.txt', 'r')

############################

sub_jobs = []
count = 0
for line in id_file:
    print count
    if count <= 28:
       run_job(line,deps = [])
    if count >=29 and count <=56:
       run_job(line,deps=sub_jobs)
    if count >=56 and count <= 84: 
       run_job(line,deps=sub_jobs[28:55])
    count = count + 1











   
     


