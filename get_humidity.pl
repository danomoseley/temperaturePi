#!/usr/bin/perl
use LWP::UserAgent;
 
my $dir = '/home/pi/temperaturePi';

$processes = `ps aux`;
if ($processes !~ /pigpiod/g) {
    $success = `sudo pigpiod`
}
 
$attempts = 0;
while ($attempts < 5) {
    $output = `$dir/DHTXXD -g14`;
    if($output =~ /^0/g)
    {
        $output =~ /(\d+\.\d+)\n/i;
        $humidity = $1;
        print "Living Room: $humidity%\n";
        $rrd = `/usr/bin/rrdtool update $dir/database/humidity.rrd N:$humidity`;
        last;
    }
    $attempts++;
}

