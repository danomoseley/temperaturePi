#!/usr/bin/perl
use LWP::UserAgent;
 
my $dir = '/home/pi/temperaturePi';
my $is_celsius = 0; #set to 1 if using Celsius
 
$modules = `cat /proc/modules`;
if ($modules =~ /w1_therm/ && $modules =~ /w1_gpio/)
{
    #modules installed
}
else
{
    $gpio = `sudo modprobe w1-gpio`;
    $therm = `sudo modprobe w1-therm`;
}
 
$output1 = "";
$attempts = 0;
while ($output1 !~ /YES/g && $attempts < 5)
{
    $output1 = `sudo cat /sys/bus/w1/devices/28-00043b6f76ff/w1_slave 2>&1`;
    $output2 = `sudo cat /sys/bus/w1/devices/28-00043c92ddff/w1_slave 2>&1`;
    $output3 = `sudo cat /sys/bus/w1/devices/28-00043c939cff/w1_slave 2>&1`;
    $output4 = `sudo cat /sys/bus/w1/devices/28-00043c93b8ff/w1_slave 2>&1`;
    $output5 = `sudo cat /sys/bus/w1/devices/28-00043c93b0ff/w1_slave 2>&1`;	
    $output6 = `sudo cat /sys/bus/w1/devices/28-00044a37deff/w1_slave 2>&1`;
    if($output1 =~ /No such file or directory/) {
        print "Could not find DS18B20\n";
        last;
    } elsif($output1 !~ /NO/g) {
        $output1 =~ /t=(-?\d+)/i;
        $temp1 = ($is_celsius) ? ($1 / 1000) : ($1 / 1000) * 9/5 + 32;
        $output2 =~ /t=(-?\d+)/i;
        $temp2 = ($is_celsius) ? ($1 / 1000) : ($1 / 1000) * 9/5 + 32;
        $output3 =~ /t=(-?\d+)/i;
        $temp3 = ($is_celsius) ? ($1 / 1000) : ($1 / 1000) * 9/5 + 32;
        $output4 =~ /t=(-?\d+)/i;
        $temp4 = ($is_celsius) ? ($1 / 1000) : ($1 / 1000) * 9/5 + 32;
        $output5 =~ /t=(-?\d+)/i;
        $temp5 = ($is_celsius) ? ($1 / 1000) : ($1 / 1000) * 9/5 + 32;
        $output6 =~ /t=(-?\d+)/i;
        $temp6 = ($is_celsius) ? ($1 / 1000) : ($1 / 1000) * 9/5 + 32;
        $rrd = `/usr/bin/rrdtool update $dir/temp.rrd N:$temp3:$temp2:$temp4:$temp1:$temp5:$temp6`;
    }
    $attempts++;
}

print "Outside:      $temp1\n";
print "Under stairs: $temp2\n";
print "Bedroom:      $temp3\n";
print "Living Room:  $temp5\n";
print "North Cellar: $temp4\n";
print "Kitchen Sink: $temp6\n";

