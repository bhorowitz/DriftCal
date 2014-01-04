""" Configuration Parameters for DriftCal """

# Ucac catalog position
ucac = "/lustre/scratch/client/hep/group/astro/scratch/daver/ucac4/access/u4test"

# Region of examination
min_ra = 180
max_ra = 210
min_dec = -6
max_dec = -2

#If looking for RR Lyrae, which B-R cut to use
BR_cut = 0.9

#columns to use from data (8 columns) 
#(ra, dec, r_mag, r_error, b_mag, b_error, fwhm_r, fwhm_b)
cols = (4,5,8,9,16,17,36,42)