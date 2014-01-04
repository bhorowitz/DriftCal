use strict;
use warnings;
use FileHandle;
use File::Basename;
use Math::Trig;
use Math::Complex;
use POSIX;

# Project UCAC : Late Spring 2013
# Ben Horowitz
# Querries UCAC catalog... Run in Bulldog Omega (or Bulldog P?)



my $minra = $ARGV[0];
my $maxra = $ARGV[1];
my $ss = 1;
my $dec = $ARGV[3];
my $decsize = $ARGV[4];
my $index = $ARGV[5];
my $field = $ARGV[6];

my $i = $minra;

my $count = 0;
system("mkdir ucac_$field");
while ($count <= $index) {
	system("/lustre/scratch/client/hep/group/astro/scratch/daver/ucac4/access/u4test $i $dec $ss $decsize /lustre/scratch/client/hep/group/astro/scratch/daver/ucac4/u4b");
	my $j = floor($i - $minra);
	system("cp ucac4.txt ./ucac_$field/$j");
	$count ++;
	$i = $i + $ss;
}
