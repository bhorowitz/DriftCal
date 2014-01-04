#!/usr/bin/perl

use strict;
use warnings;
use FileHandle;
use File::Basename;

# Statistics package for finding median of the frames.

my $minra = $ARGV[0];
my $steps = $ARGV[1];
my $field = $ARGV[2];
my @column_R = ();

# R and B
my $count =0;
while ($count <= $steps) {
foreach my $target (glob "./$field/$count.out") {
	 my $inputfile = new FileHandle "< $target" or die "Couldn't open $target:$!\n";
	my @column_R= ();
	 my @column_B = ();
        while (<$inputfile>) {
	 if (/^#/) {
	    next;
	  }
	  chomp;
      		my @line = split ' ', $_;
      		my $mag = $line[10];
	  my $mag2 = $line[12];
		if ($mag != -1) {
			push @column_R, $mag;
			push @column_B, $mag2;
		}	
        }
		unless (scalar @column_R == 0)
	  {
	    #no clipping yet...
	    my $median_R = median(@column_R);
	    my $median_B = median(@column_B);
	    my $ra = $count + $minra;
	    open ( OUT, ">> $field.stats");
	    print OUT "$count $ra $median $median2\n";

	  }
       }
$count ++;
}

sub median {
    my @a = sort {$a <=> $b} @_;
    my $length = scalar @a;
    return undef unless $length;
    ($length % 2)
        ? $a[$length/2]
        : ($a[$length/2] + $a[$length/2-1]) / 2.0;
}

sub average{
        my($data) = @_;
        if (not @$data) {
                die("Empty array\n");
        }
        my $total = 0;
        foreach (@$data) {
                $total += $_;
        }
        my $average = $total / @$data;
        return $average;
}
sub stdev{
        my($data) = @_;
        if(@$data == 1){
                return 0;
        }
        my $average = &average($data);
        my $sqtotal = 0;
        foreach(@$data) {
                $sqtotal += ($average-$_) ** 2;
        }
        my $std = ($sqtotal / (@$data-1)) ** 0.5;
        return $std;
}
