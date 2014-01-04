#!/usr/bin/perl

use strict;
use warnings;
use FileHandle;
use File::Basename;
use Math::Trig;
use Math::Complex;

# Project Squeaky Clean : August 16, 2012
# Ben Horowitz
# Takes an input file, removes all non-relevant signals


my $in = $ARGV[0];
my $out = $ARGV[1];

my $inputfile = new FileHandle "< $in" or die "Couldn't open :$!\n";

open ( OUT, "> $out");

while (<$inputfile>) {
  if (/^#/) {
    next;
  }
    my @line = split ' ', $_;
    my $x1 = $line[0];
    my $x2 = $line[4];
  my $x3 = $line[5];
  my $r = $line[8];
  my $i = $line[12];
  my $b = $line[16];
  my $u = $line[20];
  my $instmag_err_R = $line[9];
  my $instmag_err_B = $line[17];
  my $fwhm_R = $line[36];
  my $fwhm_B = $line[42];
  my $minor_R = $line[35];
  my $minor_B = $line[41];
  my $major_R = $line[34];
  my $major_B = $line[40];

  if (0.1 > $instmag_err_R > 0 && 0.1 > $instmag_err_B > 0 && 5.0 > $fwhm_R > 1.5 && 5.0 > $fwhm_B > 1.5 && $minor_R > 0.5 && $minor_B > 0.5 && $major_R > 0.8 && $major_B > 0.8 && 25 > $b > 10 && 25 > $r > 10 && $ra<210){
    print OUT "$x1 $x2 $x3 $r $i $b $u \n";
  }}

