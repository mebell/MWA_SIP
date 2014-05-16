import os, sys
import re

################################################################################
# File to create and submit multiple job files for downloading and processing. #
################################################################################

# Work out which GPS ID / datafile we are going to work on 
id_file = open('obs_id_list.txt', 'r')

for line in id_file:
    ### Run the download job on the  "copy" que (see agruments in header of "template_download)
    os.system('cp template_download download.go') # Copy the template jobfile 
    job_file = open('download.go', 'a')
    print 'Writing appropriate download job file for observation '+line 
    # Add the appropriate command. 
    #job_file.write('/short/ek6/CASA/casapy-34.0.19988-002-64b/casapy -c /home/562/meb562/SIP/SIP_128T_parallel.py '+line)
    job_file.write('python /home/562/meb562/SIP/get_data.py '+line)
    job_file.close()
    # Submit the file to qsub.
    name = line.split('/')[-1]        # Define the output and error log names
    name = re.split("[\r\n]+",name)[0] # Get rid of the return carriage
    error_log = '/home/562/meb562/SIP/error_logs/'+name+'.download.error'
    output_log = '/home/562/meb562/SIP/error_logs/'+name+'.download.output'
    print 'Qsub command is = qsub -e '+error_log+' -o '+output_log+' download.go'
    download_command = 'qsub -e '+error_log+' -o '+output_log+' download.go'
    term_out=os.popen(download_command).read()
    term_out = re.split("[\r\n]+",term_out)[0] # Remove return carriage
    ### Run the processing on the "normal" que (see agruments in header of "template_jobfile)
    os.system('cp template_jobfile job_file.go') # Copy the template jobfile 
    job_file = open('job_file.go', 'a')
    print 'Writing appropriate job file for observation '+line
    print 'Will only exceute qsub job when download is complete' 
    # Add the appropriate command.  
    job_file.write('python /home/562/meb562/SIP/pre_proc_pipe.py '+line)
    #job_file.write('/short/ek6/CASA/casapy-34.0.19988-002-64b/casapy -c /home/562/meb562/SIP/SIP_128T_parallel.py '+line)
    job_file.close()
    # Submit the file to qsub.
    name = line.split('/')[-1]        # Define the output and error log names
    name = re.split("[\r\n]+",name)[0] # Get rid of the return carriage
    error_log = '/home/562/meb562/SIP/error_logs/'+name+'.proc.error'
    output_log = '/home/562/meb562/SIP/error_logs/'+name+'.proc.output'
    print 'Qsub command is = qsub -W depend=afterok:'+term_out+' -e '+error_log+' -o '+output_log+' job_file.go'
    os.system('qsub -W depend=afterok:'+term_out+' -e '+error_log+' -o '+output_log+' job_file.go')




