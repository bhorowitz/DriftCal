import numpy as np
import os
import csv
import sys
import re
import conf

#initial timing
import time
tic = time.time()

"""

NAME
   DriftCal

PURPOSE
   Calibrate Palamar fields (or any drift-scan fields) dynamically to UCAC standards.

RUN COMMANDS
   python PalPy.py [PATH FILE] [PLOT OPTIONS (or nothing)]

USER INPUTS
   A PATH FILE with a column of locations of drift-scan files. Assumes data is formatted like Palamar.

OUTPUTS
   A .np file of calibrated data. Can easily be adjusted to output CSV file. Optional plotting routines.

LOG
   September 14, 2013: Operational
   September 15, 2013: Plotting Routines

CONTACT
   Benjamin Horowitz (benjamin.a.horowitz@yale.edu, horowitz.ben@gmail.com)

"""
#Supresses warning messages when reading in UCAC data. All fatal errors will still be displayed.
import warnings
warnings.filterwarnings("ignore")

def cand(cal_file, cal_data, BR_cut):
	f_cand = file('./calibrated_' + cal_file + '/candidates', 'a')
	print cal_data[2,2],cal_data[2,4]
	bool = (cal_data[:,2]>12) & (cal_data[:,2]<20.5) & (cal_data[:,4]-cal_data[:,2]<BR_cut) & (cal_data[:,4]-cal_data[:,2]>0)
	cand = cal_data[bool]
        np.savetxt(f_cand, cand)
	print "size", cand.shape
	f_cand.close()
	
def rms(ucac,pal):
	#Calculates ZP by finding matching stars in each catalog and looking at the subtraction
	b = []
	r = []
#	print "in"
	for ucac_ra,ucac_dec,ucac_r,ucac_b in ucac:
		#print ucac_ra,ucac_dec
		for line in pal:
			radif = abs(line[0] - ucac_ra)
			decdif = abs(line[1] - ucac_dec)
			if radif < 0.0003:
				if decdif<0.0003:
					# Append subtraction to intiated arrays
					r.append((line[2]-ucac_r))
					b.append((line[4]-ucac_b))
	# Transform to a numpy array
	r_n = np.array(r)
	b_n = np.array(b)
	#Take out very far out measurements (indicative of a miss-match
	r_n = r_n[abs(r_n[:])<4.5]
	b_n = b_n[abs(b_n[:])<4.5]
	#Compute mean for zp purposes
	r_zp = r_n.mean()
	b_zp = b_n.mean()
	r_zp_err = np.std(r_n)
	b_zp_err = np.std(b_n)
	n_standards = r_n.size
	if r_n.size > 0:
		return r_zp, b_zp, r_zp_err, b_zp_err, n_standards
	else:
		return 1,1,1,1,1

#Path file, either relative to run path or relative to root
cal_file = str(sys.argv[1])

try:
	plot_option = str(sys.argv[2])
except:
	print "No plot options."

#parameters
min_ra = conf.min_ra
max_ra = conf.max_ra
min_dec = conf.min_dec
max_dec = conf.max_dec
BR_cut = conf.BR_cut

paths = np.loadtxt(str(cal_file), dtype='str')
#path = str(paths)
print cal_file, path
os.system('mkdir ./calibrated_' + cal_file)
#setting up folder structures
f_cand = file('./calibrated_' + cal_file + '/candidates', 'a')
f = open('./calibrated_' + cal_file + '/poor_files', 'a')
map = open('./calibrated_' + cal_file + '/map_file', 'a')

for i,path in enumerate(paths):
	
	print path
	words = re.split('/',path)
	#pa = words[2]
	pa = words[2] + "." +str(j)
	os.system('mkdir ./calibrated_' + cal_file + '/cal_' + pa) 
	os.system('mkdir ./calibrated_' + cal_file + '/ucac_' + pa)
	bad_field = open('./calibrated_'+cal_file+'/cal_' + pa + '/bad_fields', 'w')
	good_field = open('./calibrated_'+cal_file+'/cal_' + pa + '/good_fields', 'w')
	#try:
	#raw_data = np.loadtxt(path, dtype = 'str') # import data
	raw_data = np.genfromtxt(path, usecols = conf.cols)
	#except:
		#print "File to Large! Bad data file, " + path
		#f.write(path + '\n')
		#continue			
        raw_dat = np.array(raw_data[:,0:8], dtype = 'f') # clean data
        #Original Perl Cuts: if (0.1 > $instmag_err_R > 0 && 0.1 > $instmag_err_B > 0 && 5.0 > $fwhm_R > 1.5 && 5.0 > $fwhm_B > 1.5 && $minor_R > 0.5 && $minor_B > 0.5 && $major_R > 0.8 && $major_B > 0.8 && 25 > $b > 10 && 25 > $r > 10 && $ra<210
	print raw_dat[4000]
        raw_dat_bolean = (raw_dat[:,3]<0.4) & (raw_dat[:,3]>0) & (raw_dat[:,5]<0.4) & (raw_dat[:,5]>0) & (raw_dat[:,6]<7) & (raw_dat[:,6]>0.2) & (raw_dat[:,7]<10) & (raw_dat[:,7]>0.2) #Quality cuts on data
        clean_dat = raw_dat[raw_dat_bolean]
	print raw_data.shape, clean_dat.shape
	if clean_dat.shape[0]<2:
		print "Bad data file, " + path
		f.write(path + '\n')
		#sys.exit(1)
		continue
        ra_max = clean_dat[:,0].max()
        ra_min = clean_dat[:,0].min()
        dec_max = clean_dat[:,1].max()
        dec_min = clean_dat[:,1].min()
        rarange = int(ra_max-ra_min+1)
	if dec_min > max_dec:
		print "out of range", dec_min, max_dec
		continue
	if dec_max < min_dec:
		print "out of range", dec_max, min_dec
		continue
	if not rarange:
		continue
	map.write(path + " " + str(ra_max) + " " + str(ra_min) + " " + str(dec_max) + " " +  str(dec_min) + '\n')
        b = np.zeros([8])
        bins = [b] * rarange
	cal_data = np.zeros([8])
	zp_rr = []
	zp_bb = []
	n_standardss = []
        for x in clean_dat:
	       # print x[4]-min_ra, x[4]-ra_min
                bins[int(x[0]-ra_min)]= np.vstack((bins[int(x[0]-ra_min)],x))
        for k in range(0,rarange):
	  try:
            bins[k] = np.delete(bins[k], (0), axis=0)
            if bins[k].size>23:
	        
	        pal = bins[k]
                p_maxra = pal[:,0].max()
                p_minra = pal[:,0].min()
                p_maxdec = pal[:,1].max()
                p_mindec = pal[:,1].min()
                dec = (p_maxdec - p_mindec)/2 + p_mindec
                decsize = p_maxdec - p_mindec
                os.system(conf.ucac + ' ' + str(p_minra+0.5) + ' ' + str(dec) + ' 1 ' + str(decsize) + ' ' + conf.ucac2)
                os.system('cp ucac4.txt ./calibrated_' + cal_file + '/ucac_' +pa +'/' + str(k))
		ucac = np.genfromtxt('./calibrated_' + cal_file + '/ucac_' + pa +'/' + str(k), usecols=(1,2,29,30),invalid_raise=False)
		#print ucac[:,0].max(), ucac[:,0].min(), p_maxra, p_minra
		#print ucac[:,1].max(), ucac[:,1].min(), p_maxdec, p_mindec
		bool = (ucac[:,2] > 1) & (ucac[:,3]>1)
		ucac = ucac[bool]
		zp_r, zp_b, r_zp_err, b_zp_err, n_standards  = rms(ucac,pal)
		if zp_r == 1 or n_standards < 6:
			bad_field.write(str(k) + " " + str(p_maxra) + " " + str(p_minra) + " " +str(p_maxdec) + " " + str(p_mindec) + ' 0 \n')
			continue
		good_field.write(str(k) + " " + str(p_maxra) + " " + str(p_minra) + " " +str(p_maxdec) + " " + str(p_mindec) + " " + str(n_standards) + " " + str(zp_r) +" " + str(r_zp_err) + " " + str(zp_b) + " " + str(b_zp_err) + '\n')
		zp_rr.append(zp_r)
		zp_bb.append(zp_b)
		n_standardss.append(n_standards)
		pal[:,2]=pal[:,2]-zp_r
		#print pal[:,8].mean()
		pal[:,4]=pal[:,4]-zp_b
		cal_data = np.vstack((cal_data,pal))
	  except:
		  bad_field.write(str(k) + " " + str(p_maxra) + " " + str(p_minra) + " " +str(p_maxdec) +" " + str(p_mindec) + '\n')
		  continue
	toc = time.time()
	cal_data = np.array(cal_data)
#	Saves a lot of output.
	np.save('./calibrated_'+cal_file + '/cal_' +pa,cal_data)
	np.save('./calibrated_'+cal_file + '/zp_r_' +pa,zp_rr)
	np.save('./calibrated_'+cal_file + '/zp_nstandards_' +pa,n_standardss)
	print "pre"
	if cal_data.size > 100:
		cand(cal_file, cal_data, BR_cut)
#	np.save('./calibrated_' + cal_file + '/cal_'+pa + './' + pa, cal_data)
	print toc-tic
	print "test"
