#!/usr/bin/perl

use strict;
use warnings;
use FileHandle;
use File::Basename;
use Math::Trig;
use Math::Complex;

# RR Lyrae Matching: May, 2013
# Ben Horowitz
# Used to look through a given file to find matches in the RR Lyrae catalog. 
#IMPORTANT: There is currently a dec cut-off to quicken the program. This should either be changed/eliminated if you are looking at a given sky area.


my $in = $ARGV[0]; #File to find RR Lyrae's in
my $cat = $ARGV[1]; #Catalog of all RR Lyrae
my $out = $ARGV[2]; #Output
my $max = $ARGV[3];
my $min = $ARGV[4];

my $catfile = new FileHandle "< $cat" or die "Couldn't open :$!\n"; #Catalog of RR Lyraes



while(<$catfile>){
  if (/^#/) {
    next;
  }
    my @line = split ' ', $_;
    my $rar = $line[1];
    my $decr = $line[2];
    my $inputfile = new FileHandle "< $in" or die "Couldn't open :$!\n";
  # Dec Ranges can/should be changed for file
    if ($decr<$max){
      if($decr>$min){
        if($rar>180){
          print "star $rar $decr\n";
          while (<$inputfile>) {
            open ( OUT, ">> $out");
            if (/^#/) {
              next;
            }
            my @line = split ' ', $_;
            my $ra = $line[0];
            my $dec = $line[1];
            my $r =  $line[2];
            my $i =  $line[3];
            my $b =  $line[4];
            my $u =  $line[5];

            my $r_res = abs($ra - $rar);
            my $dec_res = abs($dec - $decr);
            print "r_res, dec_res \n";
	    # Currently a very wide cut, can be restricted further if comparison file has good astrometry
            if($r_res < 0.003){
            if($dec_res <0.003){
              print "match found\n"; #quick tool to inspect to see if multiple stars are found. if they are, restrict further.
              print OUT "$ra $dec $r $i $b $u \n";
            }
          }
        }
      }
    }
  }

}

