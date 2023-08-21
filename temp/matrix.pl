#!/usr/bin/perl
use strict;
use warnings;
use Time::HiRes qw(usleep);

my $width = $ARGV[0] || 80; # Number of columns (use a command-line argument or default to 80)
my @streams;

# Initialize the streams
for (my $i = 0; $i < $width; $i++) {
  $streams[$i] = {
    y => rand(25),
    length => 5 + int(rand(10)),
    speed => 1 + rand(3),
  };
}

while (1) {
  # Print each stream
  for my $stream (@streams) {
    my $y = int($stream->{y});
    for (my $i = 0; $i < 25; $i++) {
      if ($i >= $y && $i < $y + $stream->{length}) {
        print chr(0x30 + rand(10));
      } else {
        print " ";
      }
    }
    print "\n";

    $stream->{y} += $stream->{speed};
    if ($stream->{y} - $stream->{length} > 25) {
      $stream->{y} = 0;
      $stream->{length} = 5 + int(rand(10));
      $stream->{speed} = 1 + rand(3);
    }
  }

  # Sleep for a bit to make it visible
  usleep(50000);
  
  # Clear the screen
  print "\033[2J";
}

