#!/usr/bin/perl

use strict;
use warnings;
use FileHandle;
use File::Basename;
use Math::Trig;
use Math::Complex;

# Project Squeaky Clean : May 14th, 2013
# Ben Horowitz
# Compares UCAC and Palomar Fields


my $steps = $ARGV[0];
my $field = $ARGV[1];
my $count = 0;
system("mkdir ./$field");
while ($count <= $steps) {
my $catfile = new FileHandle "< ./ucac_$field/$count" or die "Couldn't open :$!\n";

while(<$catfile>){
  if (/^#/) {
    next;
  }
  #default flag for r_t, maybe will make it not spit out error messages?
   my $r_t = 0;
  #ucac information
    my @line = split ' ', $_;
  my $rar = $line[1];
  my $decr = $line[2];
  my $B_t = $line[29];
  my $V_t = $line[30];
  my $g_t = $line[31];
  my $r_t = $line[32];
  my $i_t = $line[33];
my $inputfile = new FileHandle "< ./fields_$field/$count" or die "Couldn't open :$!\n";
 # print "$count $rar $decr \n";
  if ($decr<7){
    if($decr>2){
      if($rar>180){
	if($r_t > 1){
	  if($B_t > 1){
while (<$inputfile>) {
  #Palomar Data
  open ( OUT, ">> ./$field/$count.out");
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
 # print "$dec, $decr\n";
    my $r_res = abs($ra - $rar);
    my $dec_res = abs($dec - $decr);
 # matches stars
  if($r_res < 0.0002){
  #  print "good star?\n";
    if($dec_res <0.0002){
    #  print "yes!\n";
      my $dr = $r - $r_t;
      my $di = $i - $i_t;
      my $db = $b - $B_t;
  #    print "$dr $di $db \n";
      # Out: RA, DEC, Palomar R I BU, UCAC R I B, (V), Difference in R I B
      print OUT "$ra $dec $r $i $b $u $r_t $i_t $B_t V $dr $di $db\n";
  }}}}}}}}

}
$count++;
}
