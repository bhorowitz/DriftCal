use strict;
use warnings;
use FileHandle;
use File::Basename;
use Math::Trig;
use Math::Complex;
use POSIX;

# Ben Horowitz, Late Spring 2013
# Divides up Palomar Fields into slices.


my $in = $ARGV[0];
my $field = $ARGV[1];
my $index = 100;

#my $inputfile = new FileHandle "< $in" or die "Couldn't open :$!\n";

my @ra;
my @dec;

  system("mkdir ./fields_$field");
#my $in = $ARGV[0];
my $inputfile = new FileHandle "< $in" or die "Couldn't open :$!\n";
while (<$inputfile>) {
  if (/^#/) {
    next;
  }
  my @line = split ' ', $_;
  my $ran = $line[1];
  my $dec = $line[2];
  my $r = $line[3];
  my $i = $line[4];
  my $b = $line[5];
  my $u = $line[6];
  @ra = (@ra, $ran);
  @dec = (@dec, $dec);
  glob $index = floor(($ran - $ra[0]));
  open ( OUT, ">> ./fields_$field/$index") or die "Can't write to file  [$!]\n";;
  print OUT "$ran $dec $r $i $b $u \n";
}


@ra = sort @ra;
@dec = sort @dec;
open ( COORD, "> ./COORD");
print COORD "$ra[0] $ra[-1] $dec[0] $dec[-1] $index\n";
