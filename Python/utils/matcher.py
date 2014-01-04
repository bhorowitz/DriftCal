import numpy
from math import *
acc = 0.002
#l1 = numpy.genfromtxt('out_cleaned')
l1_dict = {}
ind1 = (1,2)
ind2 = (0,1)
l1 = numpy.genfromtxt("catalog_tot.dat")
#l1 = l1[1:10]
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

file2 = open("smallregion_candidates", "r")

for z,line in enumerate(file2):
      line = line.replace("\n","")
      spl = numpy.fromstring(line, dtype=float, sep=' ')
      ra_i = floor(spl[ind2[0]]*100)
      dec_i =floor(spl[ind2[1]]*100)
      for i in range(0,3):
          for j in range(0,3):
              if ra_i-1+i in l1_dict:
                  if dec_i-1+j in l1_dict[ra_i-1+i]:
                      for x in l1_dict[ra_i-1+i][dec_i-1+j]:
                          diff1 = abs(x[ind1[0]]-spl[ind2[0]])
                          diff2 = abs(x[ind1[1]]-spl[ind2[1]])
                          if diff1 < acc and diff2 < acc:
                              #print "yay", z, int(x[l1s[1]]), ra_i, dec_i
                              k = (int(x[l1s[1]]), z)
                              matched.append(k)
                              print x[ind1[0]], x[ind1[1]], line
