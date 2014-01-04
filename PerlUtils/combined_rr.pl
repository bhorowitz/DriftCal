use strict;
use warnings;
use FileHandle;
use File::Basename;
use Math::Trig;
use Math::Complex;
use POSIX;

my $steps = 1;
my $fields = $ARGV[0];
my $catfile = new FileHandle "< ./$fields" or die "Couldn't open :$!\n"; 

while(<$catfile>){
  if (/^#/) {
    next;
  }
  #ucac information
    my @line = split ' ', $_;
  my $field = $line[0];

my $in = "./data/$field";

#Parameters

my $min_ra = 180;
my $max_ra = 210;
my $min_dec = 0;
my $max_dec = 30;
my $index = 100;

# squeaky_clean up Palomar
print "cleaning\n";
system("perl squeaky_clean.pl $in $field.clean");
print "dividing palomar fields\n";
#divide creates COORD file in home directory, has 4 columns: RA_Min, RA_Max, DEC_Min, Dec_max, Index
system("perl divide.pl $field.clean $field");
print "getting field parameters\n";
##gets input parameters

my $inputfile = new FileHandle "< COORD" or die "Couldn't open :$!\n";
while (<$inputfile>) {
  if (/^#/) {
    next;
  }
  my @line = split ' ', $_;
  glob $min_ra = $line[0];
  glob $max_ra = $line[1];
  glob $min_dec = $line[2];
  glob $max_dec = $line[3];
  glob $index = $line[4];
  print "Field $field Size: $min_ra, $max_ra, $min_dec, $max_dec \n";
}
my $dec = ($max_dec - $min_dec)/2 + $min_dec;
my $decsize = $max_dec -$min_dec;

#querries and divides up ucac fields
print "querrying ucac\n";
system("perl ucac_div.pl $min_ra $max_ra 1 $dec $decsize $index $field");
print "calibrating each frame\n";
system("perl frame_cal1.pl $index $field");
print "getting RMS \n";
system("perl RMS.pl $min_ra $index $field");
system("perl add_back.pl $field.clean $field.stats $field.cor $min_ra");
system("perl RR_Lc.pl $field.cor catalog_tot.dat $field.match $max_dec $min_dec");
print "done! \n";
}
# Divide up Palomar

# Move to ./fields/
# UCAC Querry
# Move UCAC to ./ucac/
# fram_cal1
# RMS it
