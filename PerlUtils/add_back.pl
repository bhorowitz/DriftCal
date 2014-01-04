#!/usr/bin/perl

use strict;
use warnings;
use FileHandle;
use File::Basename;
use Math::Trig;
use Math::Complex;
use POSIX;

# Project Squeaky Clean : August 16, 2012
# Ben Horowitz
# Takes an input file, removes all non-relevant signals


my $in = $ARGV[0]; #cleaned
my $stats = $ARGV[1]; #stats
my $tot = $ARGV[2]; #corrected_data
my $min_ra = $ARGV[3];

my $inputfile = new FileHandle "< $in" or die "Couldn't open :$!\n";

open ( OUT, "> $tot");

while (<$inputfile>) {
  if (/^#/) {
    next;
  }
    my @line = split ' ', $_;
    my $x = $line[0];
    my $ra = $line[1];
  my $dec = $line[2];
  my $r = $line[3];
  my $i = $line[4];
  my $b = $line[5];
  my $u = $line[6];
  my $match = floor($ra - $min_ra);
  my $statsfile = new FileHandle "< $stats" or die "Couldn't Open StatsFile";
  while (<$statsfile>){
  if (/^#/) {
    next;
  }
    my @line = split ' ', $_;
    my $x1 = $line[0];
    my $ra1 = $line[1];
    my $r_cor = $line[2];
    my $b_cor = $line[3];
  if($x1 eq $match){
    print "matched!\n";
    my $new_r = $r - $r_cor;
    my $new_b = $b - $b_cor;
    print OUT "$ra $dec $new_r $new_b\n";
  }
}
}


