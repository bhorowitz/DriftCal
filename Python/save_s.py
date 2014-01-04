import numpy
from math import *
import sys
import os
import numpy as np
import sqlite3 as sql
import time

import warnings
warnings.filterwarnings("ignore")

def ra_dec_match(l1,ind1,l2,ind2,acc):
    """
    Fast approximate matching routine for RA, DEC

    Takes list one, l1, with indices ind1 (ra_col,dec_col) and matches it to list two, l2,
    within accuracy, acc.
    
    returns matched list (match) with two columns of indicies from l1 and l2
    """
  #l1 = numpy.genfromtxt('out_cleaned')
    l1_dict = {}
  #ind1 = (1,2)
    l1s = l1.shape
    for i,line in enumerate(l1):
          ra_i = floor(line[ind1[0]]*100)
          dec_i =floor(line[ind1[1]]*100)
          if ra_i not in l1_dict:
              l1_dict[ra_i]={}
              if dec_i not in l1_dict[ra_i]:
                  l1_dict[ra_i][dec_i]=[]
                  line = numpy.append(line,i)
                  l1_dict[ra_i][dec_i].append(line)
    matched = []
    for z,line in enumerate(l2):
      ra_i = floor(line[ind1[0]]*100)
      dec_i =floor(line[ind1[1]]*100)
      for i in range(0,3):
          for j in range(0,3):
              if ra_i-1+i in l1_dict:
                  if dec_i-1+j in l1_dict[ra_i-1+i]:
                      for x in l1_dict[ra_i-1+i][dec_i-1+j]:
                          diff1 = abs(x[ind1[0]]-line[ind2[0]])
                          diff2 = abs(x[ind1[1]]-line[ind2[1]])
                          if diff1 < acc and diff2 < acc:
                              #print "yay", z, int(x[l1s[1]]), ra_i, dec_i
                              k = (int(x[l1s[1]]), z)
                              matched.append(k)
    return matched
       
def rms(ucac,pal):
	#Calculates ZP by finding matching stars in each catalog and looking at the subtraction
	b = []
	r = []

        matched = ra_dec_match(ucac,(0,1),pal,(0,1),0.0002)
        #print matched
        if matched.__len__() < 1:
            raise NameError('No Matched Fields')
        for l in matched:
         #   print ucac[l[0],3]-pal[l[1],4],ucac[l[0],2]-pal[l[1],2]
            r.append(ucac[l[0],2]-pal[l[1],2])
            b.append(ucac[l[0],3]-pal[l[1],4])

	# Transform to a numpy array
	r_n = np.array(r)
	b_n = np.array(b)
	#Take out very far out measurements (indicative of a miss-match
	#r_n = r_n[abs(r_n[:])<4.5]
	#b_n = b_n[abs(b_n[:])<4.5]
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

def calibrate(path,data,ln):
        ra_max = data[:,0].max()
        ra_min = data[:,0].min()
        dec_max = data[:,1].max()
        dec_min = data[:,1].min()
        rarange = int(ra_max-ra_min+1)
	if dec_min > max_dec:
		print "out of range", dec_min, max_dec
		sys.exit(1)
		#continue
	if dec_max < min_dec:
		print "out of range", dec_max, min_dec
		sys.exit(1)
	#continue
	if not rarange:
		sys.exit(1)

       
        dec = (dec_max- dec_min)/2 + dec_min
        decsize = dec_max - dec_min
                
        os.system('/lustre/scratch/client/hep/group/astro/scratch/daver/ucac4/access/u4test ' + str(ra_min+0.5) + ' ' + str(dec) + ' 1 ' + str(decsize) + ' /lustre/scratch/client/hep/group/astro/scratch/daver/ucac4/u4b')
        time.sleep(0.4)
        os.system('mv ucac4.txt ucac_temp')
        ucac = np.genfromtxt('ucac_temp', usecols=(1,2,29,30),invalid_raise=False)
        bool = (ucac[:,2] > 1) & (ucac[:,3]>1)
        ucac = ucac[bool]
        zp_r, zp_b, r_zp_err, b_zp_err, n_standards  = rms(ucac,data)
        if zp_r == 1:
            print "exception"
            return
        if n_standards < 6:
            print "exception"
            return
        zp_rr = []
        zp_bb = []
        n_standardss = []
        zp_rr.append(zp_r)
        zp_bb.append(zp_b)
        n_standardss.append(n_standards)
        data[:,2]=data[:,2]+zp_r
        #print pal[:,8].mean()
        data[:,4]=data[:,4]+zp_b
        print zp_b, zp_r, n_standards, r_zp_err, b_zp_err
        return data,zp_b, zp_r, n_standards


def __commit_db(cur, path, ln, cal_data, zp_b, zp_r, n_standards):
    for item in cal_data:
        item = [item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7]]
        item.append(zp_b)
        item.append(zp_r)
        item.append(n_standards)
        item.append(path)
        item.append(ln)
        #print item
        cur.execute('insert into calibrated values (?,?,?,?,?,?,?,?,?,?,?,?,?)',item)
    cur.commit()

def commit_db(cur, path, ln, cal_data, zp_b, zp_r, n_standards):
    for item in cal_data:
        item = [item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7]]
        item.append(zp_b)
        item.append(zp_r)
        item.append(n_standards)
        item.append(path)
        item.append(ln)
        line = str(item)
        line = line.replace("]","")
        line = line.replace("[","")
        line = line.replace(",","")
        with open("output4", "a") as myfile:
                myfile.write(str(line) + "\n")


cal_file = str(sys.argv[1])
#initalizing db
con = sql.connect(cal_file +'.db',isolation_level=None)
cur = con.cursor()
#cur.execute("CREATE TABLE calibrated (RA, DEC, B_MAG, B_ERR, R_MAG, R_ERR, SKY, OTHER, ZP_B, ZP_R, N_STANDARDS, PATH, LN)")

#parameters
min_ra = 0
max_ra = 3600
min_dec = -360
max_dec = 360
index = 100
BR_cut = 0.9


import time
tic = time.time()


paths = np.loadtxt(str(cal_file), dtype='str')


for path in paths:
 try:
    print path
    pathfile = file(str(path), 'r')
    data = numpy.zeros([8])
    for ln, line in enumerate(pathfile):
        if ln == 0:
            j = int(line[4])
        line = line.replace("\n","")
        spl = numpy.fromstring(line, dtype=float, sep=' ')
        spl = [spl[4],spl[5],spl[8],spl[9],spl[16],spl[17],spl[36],spl[42]]
        spl = numpy.array(spl, dtype='float')
        i = int(spl[0])
        if int(spl[0]) != j:
            if data.size > 8*8:
                try:
                    cal_data,zp_b, zp_r, n_standards = calibrate(path,data[1:],ln)
                    commit_db(cur, path, ln, cal_data, zp_b, zp_r, n_standards)
                except:
                    print "error with " + path
            data = numpy.zeros([8])
            j = i
        if spl[3]<0.1 and spl[3]>0 and spl[5]<0.1 and spl[5]>0 and spl[6]<5 and spl[6]>0.5 and spl[7]<5 and spl[7]>0.5:
            data = numpy.vstack((data,spl))
 except:
      print "trouble with " + path
      with open("bad_files", "a") as myfile:
          myfile.write(path + "\n")
                          
