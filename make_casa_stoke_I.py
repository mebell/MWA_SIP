
# Script to make the Stokes I beams after make_beam.py has been run.
# Note this has to be done outside the CASA pipe as make_beam.py does not place
# nice with CASA, it needs ephem to run which is difficult to install in CASA 4.2

obs_id = sys.argv[3]
XX_image = sys.argv[4]
YY_image = sys.argv[5]
XX_beam = sys.argv[6]
YY_beam = sys.argv[7]
XXYYimages=[XX_image,YY_image,XX_beam,YY_beam]
immath(imagename=XXYYimages,expr='((IM0/IM2)+(IM1/IM3))/2', outfile='temp_stokes_I.image')
outimage=obs_id+'_I.fits'
exportfits(fitsimage=outimage,imagename="temp_stokes_I.image",stokeslast=False,overwrite=True)
