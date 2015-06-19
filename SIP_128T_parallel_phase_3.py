import numpy
import os,os.path,sys
import math
from datetime import datetime, date, time, timedelta
#import logging
import shutil
from threading import current_thread
import traceback
import tempfile
import time
import re
import pyfits
import glob

from mwapy import fits_utils as FU
try:
   from mwapy.pb import mwapb
except:
   pass;
   print 'mwa pb module did not import' 

import mwapy


############################################
##### Configuration-dependent path ########
#Parset files path(s)

loc_parset_file    = '/home/562/meb562/MWA_SIP/locs_parset.txt'
parset_file    = '/home/562/meb562/MWA_SIP/parset.txt'

######## Read parameter set file ###########

def read_parset(parset_file):
    """
     Read the parameter file defined in parset file path and return args
    """
    print 'Reading parameter set file'
    f = open(parset_file,'r')
    config_dict = {}
    for line in f:
        if line[0] == '#':
            pass;
        else:
            items = line.split('=', 1)
            config_dict[items[0]] = eval(items[1])
    return config_dict

############### autocal ##################

def autocal(vis, cal):
    '''
    Function to automatically calibrate the data. This function will use setjy or you can define a cl file to calibrate off
    '''
    params = read_parset(parset_file)
    refant  = params['refant']
    bsolint = params['bsolint']
    cal_uvrange = params['cal_uvrange']
    cal_loc = cal
    cal_method = params['cal_method']
    minsnr  = params['minsnr']  
    calflux = params['calflux']
    calspex = params['calspex']
    calfreq = params['calfreq']
    print 'Calibrating with settings: ref antenna = '+str(refant)+' , bsolint = '+str(bsolint)+', uvrange = '+str(cal_uvrange)+', minsnr = '+str(minsnr)+' (funtion:autocal)'
    caltable='temp'
    #clearcal(vis)
    if   cal_method == 1:
            print 'Using setjy method (function:autocal)'
            setjy(vis=vis,fluxdensity=calflux, spix=calspex, reffreq=calfreq, field='0')
            bcal=caltable+'.bcal'
            if os.path.exists(bcal):
               rmtables(bcal)
            bandpass(vis=vis,caltable=bcal,solint=bsolint,refant=refant,bandtype='B',append=False,selectdata=True,uvrange=cal_uvrange,minsnr=minsnr)
            applycal(vis=vis,selectdata=False,gaintable=bcal)
    elif cal_method == 2:
            print 'Using cl method (function:autocal)'
            im.open(vis,usescratch=True)
            im.ft(complist=cal_loc)
            im.close()
            bcal=caltable+'.bcal'
            if os.path.exists(bcal):
               rmtables(bcal)
            bandpass(vis=vis,caltable=bcal,solint=bsolint,refant=refant,bandtype='B',append=False,selectdata=True,uvrange=cal_uvrange,minsnr=minsnr)
            applycal(vis=vis,selectdata=False,gaintable=bcal)
    elif cal_method == 3:
            print 'Using copy solutions method (function:autocal)'
            applycal(vis=vis,selectdata=False,gaintable=cal_loc)
                        
######## Funtions for setting image sizes #########

def getBaselineLengths(msFile='', sort=True):
    " A function to retrieve baseline lengths."
    tb.open(msFile+'/ANTENNA')
    names = tb.getcol('NAME')
    positions = numpy.transpose(tb.getcol('POSITION'))
    tb.close()
    UVDist = []
    for i in range(len(names)):
      for j in range(i,len(names)):
          if (i != j):
             dist =  ((positions[i][0]-positions[j][0])**2 +
                     (positions[i][1]-positions[j][1])**2 +
                     (positions[i][2]-positions[j][2])**2)**0.5
             UVDist.append(dist)
    return(UVDist)

def getCell_Image_size(msFile):
    tb.open(msFile + '/SPECTRAL_WINDOW')
    refFreq = tb.getcol('REF_FREQUENCY')[0]
    max_baseline =  max(getBaselineLengths(msFile))
    res_radians = (3e8/refFreq)/(max_baseline) # in radians
    res_arcmin = (res_radians*(180/pi))*60 # in arcmin
    cell_size = res_arcmin/5 #  We want 5 pixels per beam. 
    print "Using optimised cell size of "+str(cell_size)
    imsize_deg = 25*(refFreq/150e6) #FWHM in degrees
    Fudge = 1.0 ###### Increase/decrease to image larger/smaller times the FWHM
    imsize_pixels = int(Fudge*((imsize_deg*60)/cell_size))
    print "Using optimised image size of "+str(imsize_pixels)+' pixels'
    return cell_size, imsize_pixels

############################################
################ WSClean ###################

def WSClean(obs_id, clean_thresh):
        print "Running WSClean"
        params  = read_parset(parset_file)
        locs = read_parset(loc_parset_file)
        wniter = params['wniter']
        wsize = params['wsize']
        wscale = params['wscale']
        if clean_thresh == None:
           wthreshold = params['wthreshold']
           print "Using parset clean threhold"
        else: 
           wthreshold = clean_thresh
           print "Using dynamic clean threshold"
        wbriggs = params['wbriggs']
        dotwoimages = params['dotwoimages']
        wbriggs2 = params['wbriggs2']
        doFullimage = params['doFullimage']
        do_W_subbands = params['do_W_subbands']
        wsclean_build = locs['wsclean_build']
        doSelfcal = params['doSelfcal']
        print 'Running WSClean'
        wbriggs = float(wbriggs) 
        wbriggs2 = float(wbriggs2)
        # Name the selfcal images
        if doSelfcal: 
		if wbriggs < 0:
		       wbriggs = str(wbriggs)
		       briggs_name = wbriggs.split('-')[1]
		       name = obs_id+'_W_bm_'+str(briggs_name)+"_SC"
		else:
		       name = obs_id+'_W_bp_'+str(wbriggs)+"_SC"
        # Name the non self-cal images
        else: 
		if wbriggs < 0:
		       wbriggs = str(wbriggs)
		       briggs_name = wbriggs.split('-')[1]
		       name = obs_id+'_W_bm'+str(briggs_name)
		else:
		       name = obs_id+'_W_bp'+str(wbriggs)
		############################################
        print "File name = "+name
        ###########################################
        locs = read_parset(loc_parset_file)
        anoko_build = locs['anoko_build']
        if doFullimage:
           os.system(wsclean_build+'/wsclean -joinpolarizations -pol xx,xy,yx,yy -mgain 0.95 -weight briggs '+str(wbriggs)+' -absmem 57 -name '+name+' -size '+str(wsize)+' '+str(wsize)+'  -scale '+str(wscale)+' -niter '+str(wniter)+' -threshold '+str(wthreshold)+' '+str(obs_id)+'.ms')
           os.system(anoko_build+'/beam -2014i -proto '+name+'-XX-image.fits -ms '+str(obs_id)+'.ms')
           ######### Make the full images 
	   os.system(anoko_build+'/pbcorrect '+name+' image.fits beam stokes')
	   os.system('mv stokes-I.fits '+name+'_I.fits')
	   os.system('mv stokes-Q.fits '+name+'_Q.fits')
	   os.system('mv stokes-U.fits '+name+'_U.fits')
	   os.system('mv stokes-V.fits '+name+'_V.fits')
	   ######## Rename the XX and YY files 
           old_name_X = name+'-XX-image.fits'
           old_name_Y = name+'-YY-image.fits'
	   new_name_X = old_name_X.replace('-XX-image.fits','_XX.fits')
	   new_name_Y = old_name_Y.replace('-YY-image.fits','_YY.fits')
	   os.system('mv '+old_name_X+' '+new_name_X)
	   os.system('mv '+old_name_Y+' '+new_name_Y)
        ##############################################################
        if dotwoimages: # Repeat the imaging with different briggs weighting
           if wbriggs2 < 0:
               wbriggs = str(wbriggs)
               briggs_name = wbriggs.split('-')[1]
               name = obs_id+'_W_bm'+str(wbriggs2)
           else:
               name = obs_id+'_W_bp'+str(wbriggs2)
           os.system(wsclean_build+'/wsclean -joinpolarizations -pol xx,xy,yx,yy -mgain 0.95 -weight briggs '+str(wbriggs2)+' -absmem 57 -name '+name+' -size '+str(wsize)+' '+str(wsize)+'  -scale '+str(wscale)+' -niter '+str(wniter)+' -threshold '+str(wthreshold)+' '+str(obs_id)+'.ms')
           os.system(anoko_build+'/beam -2014i -proto '+name+'-XX-image.fits -ms '+str(obs_id)+'.ms')
           ######### Make the full images 
           os.system(anoko_build+'/pbcorrect '+name+' image.fits beam stokes')
           os.system('mv stokes-I.fits '+name+'_I.fits')
           os.system('mv stokes-Q.fits '+name+'_Q.fits')
           os.system('mv stokes-U.fits '+name+'_U.fits')
           os.system('mv stokes-V.fits '+name+'_V.fits')
           ######## Rename the XX and YY files 
           old_name_X = name+'-XX-image.fits'
           old_name_Y = name+'-YY-image.fits'
           new_name_X = old_name_X.replace('-XX-image.fits','_XX.fits')
           new_name_Y = old_name_Y.replace('-YY-image.fits','_YY.fits')
           os.system('mv '+old_name_X+' '+new_name_X)
           os.system('mv '+old_name_Y+' '+new_name_Y)
        ##################################################################
        # Do the subbands
        if do_W_subbands:
           os.system(wsclean_build+'/wsclean -joinpolarizations -pol xx,xy,yx,yy -channelsout 32 -mgain 0.95 -weight briggs '+str(wbriggs)+' -absmem 57 -name '+name+' -size '+str(wsize)+' '+str(wsize)+'  -scale '+str(wscale)+' -niter '+str(wniter)+' -threshold '+str(wthreshold)+' '+str(obs_id)+'.ms')
           for band in range(31): 
		   if band <=32:
		       subname = name+'-000'+str(band) 
		       os.system(anoko_build+'/beam -2014i -proto '+subname+'-XX-image.fits -ms '+str(obs_id)+'.ms')
		       os.system(anoko_build+'/pbcorrect '+subname+' image.fits beam stokes') 
		       os.system('mv stokes-I.fits '+subname+'_I.fits')
		       os.system('mv stokes-Q.fits '+subname+'_Q.fits')
		       os.system('mv stokes-U.fits '+subname+'_U.fits')
		       os.system('mv stokes-V.fits '+subname+'_V.fits')
		   else:      
		       subname = name+'-MFS'
		       os.system(anoko_build+'/beam -2014i -proto '+subname+'-XX-image.fits -ms '+str(obs_id)+'.ms')        
		       os.system(anoko_build+'/pbcorrect '+subname+' image.fits beam stokes')
		       os.system('mv stokes-I.fits '+subname+'_I.fits')
		       os.system('mv stokes-Q.fits '+subname+'_Q.fits')
		       os.system('mv stokes-U.fits '+subname+'_U.fits')
		       os.system('mv stokes-V.fits '+subname+'_V.fits')           
		   os.system('rm  *beam-*')

 #############################################################################
        

def selfcal(obs_id):
        print 'Doing Selfcal WSClean method'
        params  = read_parset(parset_file)
        locs = read_parset(loc_parset_file)
        wniter = params['wniter']
        wsize = params['wsize']
        wscale = params['wscale']
        wthreshold = params['wthreshold']
        wbriggs = params['wbriggs']
        wsclean_build = locs['wsclean_build']
        print 'Running WSClean'
        wbriggs = float(wbriggs)
        if wbriggs < 0:
               wbriggs = str(wbriggs)
               briggs_name = wbriggs.split('-')[1]
               name = obs_id+'_W_bm'+str(briggs_name)
        else:
               name = obs_id+'_W_bp'+str(wbriggs)
        locs = read_parset(loc_parset_file)
        anoko_build = locs['anoko_build']
        # Do a shallow first Clean to get a model. 
        os.system(anoko_build+'/wsclean -absmem 57 -weight uniform -size 3072 3072 -scale 0.0150deg -niter 4000 -gain 0.1 -mgain 0.85 -name '+str(obs_id)+'_selfcal -pol xx,xy,yx,yy -joinpolarizations -stopnegative '+str(obs_id)+'.ms')
        # Get the beam files
        os.system('beam -2014i -name beam-'+str(obs_id)+'_selfcal -proto '+str(obs_id)+'_selfcal-XX-image.fits -ms '+str(obs_id)+'.ms')
        # Correct the image
        os.system('pbcorrect '+str(obs_id)+'_selfcal model.fits beam-'+str(obs_id)+'_selfcal '+str(obs_id)+'_selfcal')
        # Remove the polarsiation images
        os.system('rm *selfcal-Q.fits')
        os.system('rm *selfcal-U.fits')
        os.system('rm *selfcal-V.fits')  
        # Uncorrect the model image to get a model
        os.system('pbcorrect -uncorrect '+str(obs_id)+'_selfcal model.fits beam-'+str(obs_id)+'_selfcal '+str(obs_id)+'_selfcal')
        # Use the WSClean predict option
        os.system('wsclean -absmem 57 -weight uniform -size 3072 3072 -scale 0.0150deg -predict -name '+str(obs_id)+'_selfcal -pol xx,xy,yx,yy '+str(obs_id)+'.ms')
        # Calibrate
        os.system('calibrate -minuv 60 -datacolumn CORRECTED_DATA -a 0.001 0.0001 '+str(obs_id)+'.ms '+str(obs_id)+'_selfcal.cal')
        # Apply the solutions 
        os.system('applysolutions -datacolumn CORRECTED_DATA -copy '+str(obs_id)+'.ms '+str(obs_id)+'_selfcal.cal')

########## Find the RMS of an image using the inter-quartile range ##########

def mes_RMS(fitsimage):
    os.system('rm -rf preview.image')
    importfits(fitsimage=fitsimage, imagename="preview.image")
    ia.open('preview.image')
    my_output=imstat('preview.image', box='998,874,2180,2124')
    quartile=my_output['quartile']
    ia.calcmask(mask='(preview.image < '+str(quartile[0])+')',name='msk')
    ia.done()
    my_output=imstat('preview.image', box='998,874,2180,2124')
    foundrms=my_output['rms']
    return foundrms
       
############ Run the code ##################
print '---------------------------------'
print 'MWA 128T Standard Imaging Pipeline'
print '---------------------------------'

##### Get all the paths #####
obspath = sys.argv[3]
filename = obspath.split('/')[-1]
obsid = filename.split('.')[0]
cal = sys.argv[4]

params = read_parset(parset_file) # Get the parameter set file 

locs = read_parset(loc_parset_file) # Read the locations files
out_dir = locs['results_dir']
print 'Output directory is '+out_dir

job_path = os.path.dirname(obspath)
os.chdir(job_path)
print "Job path = " +job_path
print 'Currently in dir '+os.getcwd()
print 'Processing '+obspath

######### Clean up ##########
os.system('rm -rf '+job_path+'/*.bcal')
os.system('rm -rf '+job_path+'/*.residual')
os.system('rm -rf '+job_path+'/*.psf')
os.system('rm -rf '+job_path+'/*.model')
os.system('rm -rf '+job_path+'/*.flux')
os.system('rm -rf '+job_path+'/*.last')
os.system('rm -rf '+job_path+'/*.fits')
os.system('rm -rf '+job_path+'/*.log')
os.system('rm -rf '+job_path+'/*.image')
os.system('rm -rf '+job_path+'/*.beam')

#### Cut out short baselines ####
doSplit = params['doSplit']
split_uv_range = params['split_uv_range']
if doSplit:
   print 'Splitting out baslines with range:'
   print split_uv_range
   os.system('rm -rf temp.ms')
   os.system('mv '+obspath+' temp.ms')
   split(vis='temp.ms', outputvis=obspath, uvrange=split_uv_range, keepflags=True, datacolumn ='data')
   os.system('rm -rf temp.ms')

# Flag one half of the array for ionospheric studies
doFlagEast=params['doFlagEast']
doFlagWest=params['doFlagWest']

if doFlagEast:
   flagdata(vis=obspath, selectdata=True, antenna="0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,57,58,59,60,61,64,65,66,67,68,69,70,71,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,121")
if doFlagWest:
   flagdata(vis=obspath, selectdata=True, antenna="0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,34,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,66,67,68,69,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,93,114,120,121,122,123,124,125,126,127")

#### Apply the cal ####
autocal(obspath, cal)
print "Calibration finished"

#### Image ####
doWSClean = params['doWSClean']
doSelfcal = params['doSelfcal']
if doWSClean:
   WSClean(obsid, clean_thresh=None)
if doSelfcal:
   selfcal(obsid)
   # Get the clean threshold from the lightly cleaned image
   XX_YY_RMSs = []
   XX_image = str(obsid)+'_selfcal-XX-image.fits'
   YY_image = str(obsid)+'_selfcal-YY-image.fits'
   XX_YY_RMSs.append(mes_RMS(fitsimage=XX_image)[0])
   XX_YY_RMSs.append(mes_RMS(fitsimage=YY_image)[0])
   print "XX and YY lightly cleaned image RMS':"
   print XX_YY_RMSs
   # Use the max RMS of the polarsiations for CLEANing
   best_threshold = max(XX_YY_RMSs)*3
   print "Using clean threshold = "+str(best_threshold)
   WSClean(obsid, clean_thresh=best_threshold)
   #WSClean(obsid, clean_thresh=None)
############################################











